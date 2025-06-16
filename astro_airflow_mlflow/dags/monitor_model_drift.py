"""
DAG for monitoring model performance metrics over time to detect data drift or concept drift
This DAG fetches metrics from all past MLflow runs, analyzes trends, and alerts on significant changes
"""

import os
import pandas as pd
import numpy as np
import mlflow
from mlflow.tracking import MlflowClient
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from airflow import DAG
from airflow.decorators import task
from dotenv import load_dotenv
from src import src_logger as logger
from src.constants import *
from src.config.configuration import ConfigurationManager
from src.utils.common import create_directories

# Load environment variables from .env file
load_dotenv()

# MLflow configuration
ml_flow_config = {
    "uri": os.getenv('MLFLOW_TRACKING_URI'),
    "experiment_name": os.getenv('MLFLOW_EXPERIMENT_NAME')
}

# Model details
REGISTERED_MODEL_NAME = "Best_XGBoost_Model"
METRICS_TO_MONITOR = ['test_f1_score', 'test_accuracy', 'train_f1_score', 'train_accuracy']

# Drift detection thresholds
DRIFT_THRESHOLD = 0.05  # 5% change is considered significant
TREND_WINDOW = 5  # Number of recent runs to consider for trend analysis

logger.info("📊 Model Drift Monitoring Configuration:")
logger.info(f"  MLFlow URI: {ml_flow_config['uri']}")
logger.info(f"  MLFlow Experiment Name: {ml_flow_config['experiment_name']}")
logger.info(f"  Registered Model Name: {REGISTERED_MODEL_NAME}")
logger.info(f"  Metrics to Monitor: {METRICS_TO_MONITOR}")
logger.info(f"  Drift Threshold: {DRIFT_THRESHOLD}")
logger.info(f"  Trend Window: {TREND_WINDOW}")

# Define the default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
with DAG(
    dag_id='monitor_model_drift',
    description='Monitor model performance metrics over time to detect data drift or concept drift',
    default_args=default_args,
    schedule='@weekly',  # Run weekly, adjust as needed
    catchup=False
) as dag:

    @task
    def initialize_configuration():
        """Initialize configuration manager and return config"""
        logger.info("Initializing configuration for model drift monitoring")
        config_manager = ConfigurationManager(
            config_file_path=CONFIG_FILE_PATH,
            params_file_path=PARAMS_FILE_PATH,
            schema_file_path=SCHEMA_FILE_PATH
        )
        
        # Get model trainer config for relevant paths
        model_config = config_manager.get_model_trainer_config()
        
        logger.info("Configuration initialized successfully")
        return {
            'artifacts_dir': str(model_config.root_dir),
            'target_column': model_config.target_column,
            'model_name': model_config.model_name
        }

    @task
    def fetch_mlflow_metrics(config):
        """
        Fetch metrics from all past MLflow runs for the registered model
        """
        logger.info("Starting to fetch metrics from MLflow")
        
        # Set MLflow tracking URI
        if ml_flow_config['uri'] is None:
            logger.error("❌ MLFlow tracking URI is not set in environment variables")
            raise ValueError("MLFlow tracking URI is required")
        
        mlflow.set_tracking_uri(ml_flow_config['uri'])
        logger.info(f"✅ MLFlow tracking URI set to: {ml_flow_config['uri']}")
        
        # Create MLflow client
        client = MlflowClient()
        
        # Initialize dictionary to store metrics
        all_runs_metrics = []
        
        try:
            # Get experiment by name
            experiment = mlflow.get_experiment_by_name(ml_flow_config['experiment_name'])
            if experiment is None:
                logger.warning(f"Experiment '{ml_flow_config['experiment_name']}' not found")
                # Try to find any experiments related to the model
                experiments = client.search_experiments()
                for exp in experiments:
                    if REGISTERED_MODEL_NAME.lower() in exp.name.lower():
                        experiment = exp
                        logger.info(f"Found related experiment: {exp.name}")
                        break
            
            if experiment is None:
                logger.error("No relevant experiments found")
                return pd.DataFrame()
            
            # Get all runs for the experiment
            runs = mlflow.search_runs(experiment_ids=[experiment.experiment_id])
            logger.info(f"Found {len(runs)} runs for experiment '{experiment.name}'")
            
            if runs.empty:
                logger.warning("No runs found for the experiment")
                return pd.DataFrame()
            
            # Extract relevant metrics and metadata from runs
            for _, run in runs.iterrows():
                run_metrics = {
                    'run_id': run.run_id,
                    'start_time': datetime.fromtimestamp(run.start_time/1000),  # Convert ms to datetime
                    'status': run.status
                }
                
                # Extract requested metrics
                for metric in METRICS_TO_MONITOR:
                    metric_key = f"metrics.{metric}"
                    if metric_key in run:
                        run_metrics[metric] = run[metric_key]
                    else:
                        run_metrics[metric] = None
                
                all_runs_metrics.append(run_metrics)
            
            # Convert to DataFrame and sort by start_time
            metrics_df = pd.DataFrame(all_runs_metrics)
            metrics_df = metrics_df.sort_values('start_time')
            
            # Save metrics to CSV for future reference
            metric_dir = os.path.join(config['artifacts_dir'], 'model_metrics')
            if not os.path.exists(metric_dir):
                os.makedirs(metric_dir, exist_ok=True)
            logger.info(f"Metrics directory created at: {metric_dir}")
            logger.info("Saving metrics to CSV file")
            metrics_file_path = os.path.join(metric_dir, 'model_metrics_history.csv')
            metrics_df.to_csv(metrics_file_path, index=False)
            logger.info(f"Metrics saved to {metrics_file_path}")
            
            return metrics_df
            
        except Exception as e:
            logger.error(f"❌ Error fetching metrics from MLflow: {e}")
            return pd.DataFrame()

    @task
    def analyze_metrics_for_drift(metrics_df, config):
        """
        Analyze metrics for potential data drift or concept drift
        """
        logger.info("Starting to analyze metrics for potential drift")
        
        if metrics_df.empty:
            logger.warning("No metrics data available for analysis")
            return {
                'drift_detected': False,
                'message': "No metrics data available for analysis"
            }
        
        # Create directory for plots
        plots_dir = os.path.join(config['artifacts_dir'], 'drift_analysis_plots')
        os.makedirs(plots_dir, exist_ok=True)
        
        drift_results = {}
        
        try:
            # Focus only on completed runs
            completed_runs = metrics_df[metrics_df['status'] == 'FINISHED'].copy()
            if completed_runs.empty:
                logger.warning("No completed runs available for analysis")
                return {
                    'drift_detected': False,
                    'message': "No completed runs available for analysis"
                }
            
            # Ensure metrics are numeric
            for metric in METRICS_TO_MONITOR:
                completed_runs[metric] = pd.to_numeric(completed_runs[metric], errors='coerce')
            
            # Calculate rolling statistics for trend analysis
            for metric in METRICS_TO_MONITOR:
                if metric not in completed_runs.columns:
                    continue
                    
                # Drop NA values for the current metric
                metric_data = completed_runs.dropna(subset=[metric])
                if len(metric_data) < 2:
                    logger.warning(f"Not enough data points for metric {metric}")
                    continue
                
                # Get recent values for analysis
                if len(metric_data) > TREND_WINDOW:
                    recent_values = metric_data[metric].tail(TREND_WINDOW).values
                    historical_values = metric_data[metric].iloc[:-TREND_WINDOW].values
                else:
                    if len(metric_data) > 1:
                        recent_values = metric_data[metric].tail(1).values
                        historical_values = metric_data[metric].iloc[:-1].values
                    else:
                        logger.warning(f"Not enough historical data for metric {metric}")
                        continue
                
                # Calculate statistics
                recent_mean = np.mean(recent_values)
                historical_mean = np.mean(historical_values) if len(historical_values) > 0 else recent_values[0]
                
                # Calculate percentage change
                if historical_mean != 0:
                    percent_change = abs(recent_mean - historical_mean) / historical_mean
                else:
                    percent_change = 0
                
                # Check for significant drift
                is_drift = percent_change > DRIFT_THRESHOLD
                
                # Store results
                drift_results[metric] = {
                    'recent_mean': recent_mean,
                    'historical_mean': historical_mean,
                    'percent_change': percent_change,
                    'drift_detected': is_drift
                }
                
                # Create and save plot
                plt.figure(figsize=(12, 6))
                plt.plot(metric_data['start_time'], metric_data[metric], marker='o', linestyle='-')
                plt.axhline(y=historical_mean, color='r', linestyle='--', label=f'Historical Mean: {historical_mean:.4f}')
                plt.axhline(y=recent_mean, color='g', linestyle='--', label=f'Recent Mean: {recent_mean:.4f}')
                plt.title(f'{metric} Over Time | Drift Detected: {is_drift}')
                plt.xlabel('Run Date')
                plt.ylabel(metric)
                plt.grid(True)
                plt.legend()
                
                # Add annotations for drift
                if is_drift:
                    plt.annotate(f'Drift: {percent_change:.2%}', 
                                xy=(metric_data['start_time'].iloc[-1], recent_mean),
                                xytext=(metric_data['start_time'].iloc[-1], recent_mean * 1.1),
                                arrowprops=dict(facecolor='red', shrink=0.05))
                
                plot_path = os.path.join(plots_dir, f'{metric}_trend.png')
                plt.savefig(plot_path)
                plt.close()
                logger.info(f"Plot saved to {plot_path}")
            
            # Determine overall drift status
            any_drift = any(result['drift_detected'] for result in drift_results.values())
            
            # Create summary report
            summary = "## Model Drift Analysis Report\n\n"
            summary += f"**Analysis Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            summary += f"**Model:** {REGISTERED_MODEL_NAME}\n\n"
            summary += f"**Drift Detected:** {'Yes' if any_drift else 'No'}\n\n"
            summary += "### Metric Details\n\n"
            
            for metric, result in drift_results.items():
                summary += f"#### {metric}\n"
                summary += f"- Recent Mean: {result['recent_mean']:.4f}\n"
                summary += f"- Historical Mean: {result['historical_mean']:.4f}\n"
                summary += f"- Change: {result['percent_change']:.2%}\n"
                summary += f"- Drift Detected: {'Yes' if result['drift_detected'] else 'No'}\n\n"
            
            # Save summary report
            report_path = os.path.join(plots_dir, 'drift_analysis_report.md')
            with open(report_path, 'w') as f:
                f.write(summary)
            
            logger.info(f"Drift analysis report saved to {report_path}")
            
            # Log summary to Airflow logs
            logger.info(f"Drift Analysis Summary:")
            logger.info(f"  Model: {REGISTERED_MODEL_NAME}")
            logger.info(f"  Drift Detected: {'Yes' if any_drift else 'No'}")
            for metric, result in drift_results.items():
                logger.info(f"  {metric}: Change of {result['percent_change']:.2%} (Drift: {'Yes' if result['drift_detected'] else 'No'})")
            
            return {
                'drift_detected': any_drift,
                'metrics_results': drift_results,
                'report_path': report_path,
                'plots_dir': plots_dir
            }
            
        except Exception as e:
            logger.error(f"❌ Error analyzing metrics for drift: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return {
                'drift_detected': False,
                'message': f"Error analyzing metrics: {str(e)}"
            }

    @task
    def generate_recommendations(drift_analysis, config):
        """
        Generate recommendations based on drift analysis
        """
        logger.info("Generating recommendations based on drift analysis")
        
        if 'message' in drift_analysis:
            logger.warning(f"Cannot generate recommendations: {drift_analysis['message']}")
            return
        
        if not drift_analysis['drift_detected']:
            logger.info("No drift detected, model performance appears stable")
            return
        
        # Generate recommendations based on which metrics showed drift
        metrics_results = drift_analysis.get('metrics_results', {})
        recommendations = []
        
        # Check for accuracy drift
        if 'test_accuracy' in metrics_results and metrics_results['test_accuracy']['drift_detected']:
            accuracy_decreased = metrics_results['test_accuracy']['recent_mean'] < metrics_results['test_accuracy']['historical_mean']
            
            if accuracy_decreased:
                recommendations.append("Model accuracy has decreased significantly. Consider retraining the model with recent data.")
            else:
                recommendations.append("Model accuracy has increased significantly. This could indicate a positive change or potential data leakage.")
        
        # Check for F1 score drift
        if 'test_f1_score' in metrics_results and metrics_results['test_f1_score']['drift_detected']:
            f1_decreased = metrics_results['test_f1_score']['recent_mean'] < metrics_results['test_f1_score']['historical_mean']
            
            if f1_decreased:
                recommendations.append("Model F1 score has decreased significantly. This could indicate class imbalance issues or changes in the data distribution.")
            else:
                recommendations.append("Model F1 score has increased significantly. Review the data to understand what might have caused this improvement.")
        
        # Check for train-test performance gap
        if ('train_accuracy' in metrics_results and 'test_accuracy' in metrics_results):
            train_acc = metrics_results['train_accuracy']['recent_mean']
            test_acc = metrics_results['test_accuracy']['recent_mean']
            
            if train_acc - test_acc > 0.1:  # More than 10% gap
                recommendations.append("There's a significant gap between training and testing accuracy, which could indicate overfitting.")
        
        # General recommendations
        recommendations.append("Review feature distributions in recent data to identify potential data drift.")
        recommendations.append("Consider performing an A/B test with the current model and a retrained model on recent data.")
        
        # Save recommendations to file
        recommendations_text = "# Model Drift Recommendations\n\n"
        recommendations_text += f"**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        recommendations_text += "## Recommendations\n\n"
        
        for i, rec in enumerate(recommendations, 1):
            recommendations_text += f"{i}. {rec}\n"
        
        recommendations_path = os.path.join(drift_analysis['plots_dir'], 'drift_recommendations.md')
        with open(recommendations_path, 'w') as f:
            f.write(recommendations_text)
        
        logger.info(f"Recommendations saved to {recommendations_path}")
        
        # Log recommendations to Airflow logs
        logger.info("Drift Analysis Recommendations:")
        for rec in recommendations:
            logger.info(f"  - {rec}")
        
        return recommendations

    # Define task dependencies
    config = initialize_configuration()
    metrics_df = fetch_mlflow_metrics(config)
    drift_analysis = analyze_metrics_for_drift(metrics_df, config)
    recommendations = generate_recommendations(drift_analysis, config)
