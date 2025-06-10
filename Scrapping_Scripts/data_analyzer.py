#!/usr/bin/env python3
"""
Premier League Data Analyzer v2.0
==================================

Analyzes the scraped Premier League data from PostgreSQL database and provides
comprehensive statistics, insights, and data quality reports.

Features:
- Data quality assessment
- Statistical analysis of match data
- Team performance analytics
- Export functionality for further analysis
- Detailed reporting

Author: Football Analytics Team
Date: June 10, 2025
"""

import psycopg2
from psycopg2.extras import RealDictCursor
import pandas as pd
import json
import logging
from datetime import datetime, date
import numpy as np
from typing import Dict, List, Tuple, Optional
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('analyzer.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class PremierLeagueDataAnalyzer:
    """
    Comprehensive analyzer for Premier League match data stored in PostgreSQL
    """
    
    def __init__(self):
        # PostgreSQL database configuration
        self.db_config = {
            'host': 'localhost',
            'port': '5434',
            'user': 'postgres',
            'password': 'postgres',
            'database': 'weekly_scrapped_data'
        }
        self.table_name = "premier_league_matches"
        self.current_season = "2024-25"
    
    def get_connection(self):
        """Get database connection"""
        return psycopg2.connect(**self.db_config)
    
    def get_basic_stats(self) -> Dict:
        """Get basic statistics about the dataset"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            stats = {}
            
            # Total matches
            cursor.execute(f"SELECT COUNT(*) as total FROM {self.table_name}")
            stats['total_matches'] = cursor.fetchone()['total']
            
            # Season coverage
            cursor.execute(f"SELECT DISTINCT season FROM {self.table_name} ORDER BY season")
            seasons = [row['season'] for row in cursor.fetchall()]
            stats['seasons'] = seasons
            
            # Date range
            cursor.execute(f"SELECT MIN(dt) as first_date, MAX(dt) as last_date FROM {self.table_name}")
            date_range = cursor.fetchone()
            stats['date_range'] = {
                'first_date': date_range['first_date'],
                'last_date': date_range['last_date']
            }
            
            # Matchweek coverage
            cursor.execute(f"SELECT MIN(mw) as min_mw, MAX(mw) as max_mw, COUNT(DISTINCT mw) as unique_mw FROM {self.table_name}")
            mw_stats = cursor.fetchone()
            stats['matchweek_coverage'] = {
                'min_matchweek': mw_stats['min_mw'],
                'max_matchweek': mw_stats['max_mw'],
                'unique_matchweeks': mw_stats['unique_mw']
            }
            
            # Team coverage
            cursor.execute(f"""
                SELECT COUNT(DISTINCT team) as unique_teams 
                FROM (
                    SELECT ht as team FROM {self.table_name}
                    UNION 
                    SELECT at as team FROM {self.table_name}
                ) teams
            """)
            stats['unique_teams'] = cursor.fetchone()['unique_teams']
            
            conn.close()
            return stats
            
        except Exception as e:
            logger.error(f"Error getting basic stats: {e}")
            return {}
    
    def check_data_quality(self) -> Dict:
        """Perform comprehensive data quality checks"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            quality_report = {}
            
            # Check for missing values
            cursor.execute(f"""
                SELECT 
                    COUNT(*) as total_rows,
                    COUNT(*) - COUNT(dt) as missing_dates,
                    COUNT(*) - COUNT(ht) as missing_home_teams,
                    COUNT(*) - COUNT(at) as missing_away_teams,
                    COUNT(*) - COUNT(fthg) as missing_home_goals,
                    COUNT(*) - COUNT(ftag) as missing_away_goals,
                    COUNT(*) - COUNT(ftr) as missing_results,
                    COUNT(*) - COUNT(hp) as missing_home_possession,
                    COUNT(*) - COUNT(ap) as missing_away_possession,
                    COUNT(*) - COUNT(hs) as missing_home_shots,
                    COUNT(*) - COUNT(as_) as missing_away_shots
                FROM {self.table_name}
            """)
            
            missing_data = cursor.fetchone()
            quality_report['missing_values'] = dict(missing_data)
            
            # Check for impossible values
            cursor.execute(f"""
                SELECT 
                    COUNT(*) as negative_goals
                FROM {self.table_name}
                WHERE fthg < 0 OR ftag < 0
            """)
            negative_goals = cursor.fetchone()
            
            cursor.execute(f"""
                SELECT 
                    COUNT(*) as invalid_possession
                FROM {self.table_name}
                WHERE hp < 0 OR hp > 100 OR ap < 0 OR ap > 100
            """)
            invalid_possession = cursor.fetchone()
            
            cursor.execute(f"""
                SELECT 
                    COUNT(*) as possession_not_100
                FROM {self.table_name}
                WHERE ABS((hp + ap) - 100) > 2
            """)
            possession_sum = cursor.fetchone()
            
            quality_report['data_validity'] = {
                'negative_goals': negative_goals['negative_goals'],
                'invalid_possession': invalid_possession['invalid_possession'],
                'possession_not_100_percent': possession_sum['possession_not_100']
            }
            
            # Check for duplicates
            cursor.execute(f"""
                SELECT COUNT(*) as duplicates
                FROM (
                    SELECT dt, ht, at, COUNT(*) 
                    FROM {self.table_name}
                    GROUP BY dt, ht, at
                    HAVING COUNT(*) > 1
                ) dup
            """)
            duplicates = cursor.fetchone()
            quality_report['duplicates'] = duplicates['duplicates']
            
            # Check matchweek consistency (should be 10 matches per week for 20 teams)
            cursor.execute(f"""
                SELECT COUNT(*) as inconsistent_weeks
                FROM (
                    SELECT mw, COUNT(*) as match_count
                    FROM {self.table_name}
                    GROUP BY mw
                    HAVING COUNT(*) != 10
                ) inc
            """)
            inconsistent_weeks = cursor.fetchone()
            quality_report['inconsistent_matchweeks'] = inconsistent_weeks['inconsistent_weeks']
            
            conn.close()
            return quality_report
            
        except Exception as e:
            logger.error(f"Error checking data quality: {e}")
            return {}
        
    def load_data(self) -> pd.DataFrame:
        """
        Load data from the PostgreSQL database into a pandas DataFrame
        """
        try:
            conn = psycopg2.connect(**self.db_config)
            
            query = f"""
            SELECT dt, ht, at, fthg, ftag, ftr, hp, ap, hs, as_, hst, ast, 
                   hc, ac, hf, af, hy, ay, hr, ar, mw, season
            FROM {self.table_name}
            WHERE season = %s
            ORDER BY dt, mw
            """
            
            df = pd.read_sql_query(query, conn, params=(self.current_season,))
            df['dt'] = pd.to_datetime(df['dt'])
            
            logger.info(f"Loaded {len(df)} matches from PostgreSQL database")
            return df
            
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            return pd.DataFrame()
        finally:
            if 'conn' in locals():
                conn.close()
    
    def generate_league_table(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate current league table from match results
        """
        # Get all unique teams
        home_teams = df['HT'].unique()
        away_teams = df['AT'].unique()
        all_teams = sorted(list(set(list(home_teams) + list(away_teams))))
        
        # Initialize table
        table_data = []
        
        for team in all_teams:
            # Home matches
            home_matches = df[df['HT'] == team]
            away_matches = df[df['AT'] == team]
            
            # Calculate stats
            matches_played = len(home_matches) + len(away_matches)
            
            # Goals
            goals_for = home_matches['FTHG'].sum() + away_matches['FTAG'].sum()
            goals_against = home_matches['FTAG'].sum() + away_matches['FTHG'].sum()
            goal_difference = goals_for - goals_against
            
            # Results
            home_wins = len(home_matches[home_matches['FTR'] == 'H'])
            away_wins = len(away_matches[away_matches['FTR'] == 'A'])
            total_wins = home_wins + away_wins
            
            home_draws = len(home_matches[home_matches['FTR'] == 'D'])
            away_draws = len(away_matches[away_matches['FTR'] == 'D'])
            total_draws = home_draws + away_draws
            
            total_losses = matches_played - total_wins - total_draws
            
            # Points
            points = (total_wins * 3) + (total_draws * 1)
            
            table_data.append({
                'Team': team,
                'Matches': matches_played,
                'Wins': total_wins,
                'Draws': total_draws,
                'Losses': total_losses,
                'Goals_For': goals_for,
                'Goals_Against': goals_against,
                'Goal_Difference': goal_difference,
                'Points': points
            })
        
        # Create DataFrame and sort by points, then goal difference
        table_df = pd.DataFrame(table_data)
        table_df = table_df.sort_values(['Points', 'Goal_Difference', 'Goals_For'], 
                                      ascending=[False, False, False])
        table_df.reset_index(drop=True, inplace=True)
        table_df.index += 1  # Start position from 1
        
        return table_df
    
    def analyze_statistics(self, df: pd.DataFrame):
        """
        Analyze various match statistics
        """
        print("\n" + "="*60)
        print("PREMIER LEAGUE 2024-25 SEASON ANALYSIS")
        print("="*60)
        
        # Basic statistics
        total_matches = len(df)
        total_goals = df['FTHG'].sum() + df['FTAG'].sum()
        avg_goals_per_match = total_goals / total_matches if total_matches > 0 else 0
        
        print(f"\n📊 BASIC STATISTICS:")
        print(f"Total Matches: {total_matches}")
        print(f"Total Goals: {total_goals}")
        print(f"Average Goals per Match: {avg_goals_per_match:.2f}")
        
        # Result distribution
        home_wins = len(df[df['FTR'] == 'H'])
        away_wins = len(df[df['FTR'] == 'A'])
        draws = len(df[df['FTR'] == 'D'])
        
        print(f"\n🏆 RESULTS DISTRIBUTION:")
        print(f"Home Wins: {home_wins} ({home_wins/total_matches*100:.1f}%)")
        print(f"Away Wins: {away_wins} ({away_wins/total_matches*100:.1f}%)")
        print(f"Draws: {draws} ({draws/total_matches*100:.1f}%)")
        
        # Possession statistics
        avg_home_possession = df['HP'].mean()
        avg_away_possession = df['AP'].mean()
        
        print(f"\n⚽ POSSESSION STATISTICS:")
        print(f"Average Home Possession: {avg_home_possession:.1f}%")
        print(f"Average Away Possession: {avg_away_possession:.1f}%")
        
        # Shots statistics
        total_shots = df['HS'].sum() + df['AS_'].sum()
        total_shots_on_target = df['HST'].sum() + df['AST'].sum()
        shot_accuracy = (total_shots_on_target / total_shots * 100) if total_shots > 0 else 0
        
        print(f"\n🎯 SHOTS STATISTICS:")
        print(f"Total Shots: {total_shots}")
        print(f"Total Shots on Target: {total_shots_on_target}")
        print(f"Shot Accuracy: {shot_accuracy:.1f}%")
        
        # Cards statistics
        total_yellows = df['HY'].sum() + df['AY'].sum()
        total_reds = df['HR'].sum() + df['AR'].sum()
        
        print(f"\n🟨 DISCIPLINARY STATISTICS:")
        print(f"Total Yellow Cards: {total_yellows}")
        print(f"Total Red Cards: {total_reds}")
        print(f"Average Yellow Cards per Match: {total_yellows/total_matches:.1f}")
        
    def show_league_table(self, df: pd.DataFrame):
        """
        Display the current league table
        """
        table = self.generate_league_table(df)
        
        print(f"\n🏆 PREMIER LEAGUE TABLE 2024-25")
        print("="*80)
        print(f"{'Pos':<3} {'Team':<20} {'MP':<3} {'W':<3} {'D':<3} {'L':<3} {'GF':<3} {'GA':<3} {'GD':<4} {'Pts':<3}")
        print("-"*80)
        
        for idx, row in table.iterrows():
            pos = idx
            print(f"{pos:<3} {row['Team']:<20} {row['Matches']:<3} {row['Wins']:<3} "
                  f"{row['Draws']:<3} {row['Losses']:<3} {row['Goals_For']:<3} "
                  f"{row['Goals_Against']:<3} {row['Goal_Difference']:+4} {row['Points']:<3}")
    
    def export_data(self, df: pd.DataFrame, format: str = 'csv'):
        """
        Export data to various formats
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if format.lower() == 'csv':
            filename = f"premier_league_data_{timestamp}.csv"
            df.to_csv(filename, index=False)
            print(f"\n📁 Data exported to: {filename}")
            
        elif format.lower() == 'excel':
            filename = f"premier_league_data_{timestamp}.xlsx"
            df.to_excel(filename, index=False)
            print(f"\n📁 Data exported to: {filename}")
    
    def generate_report(self):
        """
        Generate a comprehensive analysis report
        """
        # Load data
        df = self.load_data()
        
        if df.empty:
            print("No data found in database")
            return
        
        # Run analysis
        self.analyze_statistics(df)
        self.show_league_table(df)
        
        # Export data
        self.export_data(df, 'csv')
        
        print(f"\n✅ Analysis completed successfully!")
        print(f"Database: {self.db_name}")
        print(f"Matches analyzed: {len(df)}")
    
    def analyze_team_performance(self, season: str = "2024-25") -> Dict:
        """Analyze team performance statistics"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # Team statistics query with correct aggregation
            cursor.execute(f"""
                WITH home_stats AS (
                    SELECT 
                        ht as team,
                        COUNT(*) as home_games,
                        SUM(fthg) as home_goals_for,
                        SUM(ftag) as home_goals_against,
                        SUM(CASE WHEN ftr = 'H' THEN 3 WHEN ftr = 'D' THEN 1 ELSE 0 END) as home_points,
                        SUM(CASE WHEN ftr = 'H' THEN 1 ELSE 0 END) as home_wins,
                        SUM(CASE WHEN ftr = 'D' THEN 1 ELSE 0 END) as home_draws,
                        SUM(CASE WHEN ftr = 'A' THEN 1 ELSE 0 END) as home_losses,
                        AVG(hp::float) as avg_home_possession,
                        AVG(hs::float) as avg_home_shots
                    FROM {self.table_name}
                    WHERE season = %s
                    GROUP BY ht
                ),
                away_stats AS (
                    SELECT 
                        at as team,
                        COUNT(*) as away_games,
                        SUM(ftag) as away_goals_for,
                        SUM(fthg) as away_goals_against,
                        SUM(CASE WHEN ftr = 'A' THEN 3 WHEN ftr = 'D' THEN 1 ELSE 0 END) as away_points,
                        SUM(CASE WHEN ftr = 'A' THEN 1 ELSE 0 END) as away_wins,
                        SUM(CASE WHEN ftr = 'D' THEN 1 ELSE 0 END) as away_draws,
                        SUM(CASE WHEN ftr = 'H' THEN 1 ELSE 0 END) as away_losses,
                        AVG(ap::float) as avg_away_possession,
                        AVG(as_::float) as avg_away_shots
                    FROM {self.table_name}
                    WHERE season = %s
                    GROUP BY at
                )
                SELECT 
                    COALESCE(h.team, a.team) as team,
                    COALESCE(h.home_games, 0) + COALESCE(a.away_games, 0) as total_games,
                    COALESCE(h.home_goals_for, 0) + COALESCE(a.away_goals_for, 0) as total_goals_for,
                    COALESCE(h.home_goals_against, 0) + COALESCE(a.away_goals_against, 0) as total_goals_against,
                    COALESCE(h.home_points, 0) + COALESCE(a.away_points, 0) as total_points,
                    COALESCE(h.home_wins, 0) + COALESCE(a.away_wins, 0) as total_wins,
                    COALESCE(h.home_draws, 0) + COALESCE(a.away_draws, 0) as total_draws,
                    COALESCE(h.home_losses, 0) + COALESCE(a.away_losses, 0) as total_losses,
                    (COALESCE(h.avg_home_possession, 0) + COALESCE(a.avg_away_possession, 0)) / 2 as avg_possession,
                    (COALESCE(h.avg_home_shots, 0) + COALESCE(a.avg_away_shots, 0)) / 2 as avg_shots
                FROM home_stats h
                FULL OUTER JOIN away_stats a ON h.team = a.team
                ORDER BY total_points DESC, (COALESCE(h.home_goals_for, 0) + COALESCE(a.away_goals_for, 0) - COALESCE(h.home_goals_against, 0) - COALESCE(a.away_goals_against, 0)) DESC
            """, (season, season))
            
            team_performance = cursor.fetchall()
            
            # Convert to dictionary format
            performance_data = []
            for team in team_performance:
                team_dict = dict(team)
                team_dict['goal_difference'] = team_dict['total_goals_for'] - team_dict['total_goals_against']
                team_dict['points_per_game'] = round(team_dict['total_points'] / team_dict['total_games'], 2) if team_dict['total_games'] > 0 else 0
                performance_data.append(team_dict)
            
            conn.close()
            return {'team_performance': performance_data}
            
        except Exception as e:
            logger.error(f"Error analyzing team performance: {e}")
            return {}
    
    def analyze_match_statistics(self, season: str = "2024-25") -> Dict:
        """Analyze overall match statistics"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # Overall match statistics
            cursor.execute(f"""
                SELECT 
                    COUNT(*) as total_matches,
                    AVG(fthg + ftag) as avg_goals_per_match,
                    MAX(fthg + ftag) as highest_scoring_match,
                    MIN(fthg + ftag) as lowest_scoring_match,
                    SUM(CASE WHEN ftr = 'H' THEN 1 ELSE 0 END) as home_wins,
                    SUM(CASE WHEN ftr = 'A' THEN 1 ELSE 0 END) as away_wins,
                    SUM(CASE WHEN ftr = 'D' THEN 1 ELSE 0 END) as draws,
                    AVG(hs + as_) as avg_shots_per_match,
                    AVG(hst + ast) as avg_shots_target_per_match,
                    AVG(hc + ac) as avg_corners_per_match,
                    AVG(hf + af) as avg_fouls_per_match,
                    AVG(hy + ay) as avg_yellow_cards_per_match,
                    AVG(hr + ar) as avg_red_cards_per_match
                FROM {self.table_name}
                WHERE season = %s
            """, (season,))
            
            match_stats = cursor.fetchone()
            
            # Home advantage analysis
            cursor.execute(f"""
                SELECT 
                    COUNT(*) as total_matches,
                    SUM(CASE WHEN ftr = 'H' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as home_win_percentage,
                    AVG(fthg::float) as avg_home_goals,
                    AVG(ftag::float) as avg_away_goals,
                    AVG(hp::float) as avg_home_possession,
                    AVG(ap::float) as avg_away_possession
                FROM {self.table_name}
                WHERE season = %s
            """, (season,))
            
            home_advantage = cursor.fetchone()
            
            # Monthly trends
            cursor.execute(f"""
                SELECT 
                    EXTRACT(MONTH FROM dt) as month,
                    COUNT(*) as matches,
                    AVG(fthg + ftag) as avg_goals,
                    SUM(CASE WHEN ftr = 'H' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as home_win_pct
                FROM {self.table_name}
                WHERE season = %s
                GROUP BY EXTRACT(MONTH FROM dt)
                ORDER BY month
            """, (season,))
            
            monthly_trends = cursor.fetchall()
            
            conn.close()
            
            return {
                'match_statistics': dict(match_stats),
                'home_advantage': dict(home_advantage),
                'monthly_trends': [dict(row) for row in monthly_trends]
            }
            
        except Exception as e:
            logger.error(f"Error analyzing match statistics: {e}")
            return {}
    
    def export_to_csv(self, filename: Optional[str] = None) -> str:
        """Export all data to CSV file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"premier_league_analysis_{timestamp}.csv"
        
        try:
            conn = self.get_connection()
            
            # Use pandas for easy CSV export
            query = f"SELECT * FROM {self.table_name} ORDER BY dt DESC, mw, id"
            df = pd.read_sql_query(query, conn)
            
            df.to_csv(filename, index=False)
            conn.close()
            
            logger.info(f"Data exported to {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"Error exporting to CSV: {e}")
            return ""
    
    def generate_comprehensive_report(self, season: str = "2024-25") -> Dict:
        """Generate a comprehensive analysis report"""
        logger.info(f"Generating comprehensive report for {season} season...")
        
        report = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'season': season,
                'analyzer_version': '2.0'
            }
        }
        
        # Get all analyses
        report['basic_statistics'] = self.get_basic_stats()
        report['data_quality'] = self.check_data_quality()
        report['team_performance'] = self.analyze_team_performance(season)
        report['match_analysis'] = self.analyze_match_statistics(season)
        
        return report
    
    def print_summary(self, report: Dict):
        """Print a formatted summary of the analysis"""
        print("\n" + "="*80)
        print("PREMIER LEAGUE DATA ANALYSIS SUMMARY")
        print("="*80)
        
        # Basic stats
        basic = report.get('basic_statistics', {})
        print(f"\n📊 DATASET OVERVIEW:")
        print(f"   Total Matches: {basic.get('total_matches', 'N/A')}")
        print(f"   Seasons: {', '.join(basic.get('seasons', []))}")
        print(f"   Unique Teams: {basic.get('unique_teams', 'N/A')}")
        mw_coverage = basic.get('matchweek_coverage', {})
        print(f"   Matchweeks: {mw_coverage.get('min_matchweek', 'N/A')} - {mw_coverage.get('max_matchweek', 'N/A')}")
        date_range = basic.get('date_range', {})
        print(f"   Date Range: {date_range.get('first_date', 'N/A')} to {date_range.get('last_date', 'N/A')}")
        
        # Data quality
        quality = report.get('data_quality', {})
        print(f"\n🔍 DATA QUALITY:")
        missing = quality.get('missing_values', {})
        validity = quality.get('data_validity', {})
        missing_total = sum([v for k, v in missing.items() if k != 'total_rows'])
        validity_total = sum(validity.values())
        print(f"   Missing Values: {missing_total}")
        print(f"   Invalid Data Points: {validity_total}")
        print(f"   Duplicate Matches: {quality.get('duplicates', 'N/A')}")
        print(f"   Inconsistent Matchweeks: {quality.get('inconsistent_matchweeks', 'N/A')}")
        
        # Match analysis
        match_analysis = report.get('match_analysis', {})
        match_stats = match_analysis.get('match_statistics', {})
        home_adv = match_analysis.get('home_advantage', {})
        
        print(f"\n⚽ MATCH STATISTICS:")
        print(f"   Total Matches: {match_stats.get('total_matches', 'N/A')}")
        avg_goals = match_stats.get('avg_goals_per_match', 0)
        if avg_goals:
            print(f"   Average Goals per Match: {avg_goals:.2f}")
        print(f"   Home Wins: {match_stats.get('home_wins', 'N/A')} ({home_adv.get('home_win_percentage', 0):.1f}%)")
        print(f"   Away Wins: {match_stats.get('away_wins', 'N/A')}")
        print(f"   Draws: {match_stats.get('draws', 'N/A')}")
        avg_shots = match_stats.get('avg_shots_per_match', 0)
        if avg_shots:
            print(f"   Average Shots per Match: {avg_shots:.1f}")
        
        # Top teams
        team_perf = report.get('team_performance', {}).get('team_performance', [])
        if team_perf:
            print(f"\n🏆 TOP 5 TEAMS (by points):")
            for i, team in enumerate(team_perf[:5], 1):
                gd = team['goal_difference']
                print(f"   {i}. {team['team']} - {team['total_points']} pts ({team['total_wins']}W {team['total_draws']}D {team['total_losses']}L, GD: {gd:+d})")
        
        print("\n" + "="*80)
    
def main():
    """Main function to run the comprehensive data analyzer"""
    print("=" * 80)
    print("Premier League Data Analyzer v2.0")
    print("=" * 80)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Target: 2024-25 Premier League Season Analysis")
    print("=" * 80)
    
    analyzer = PremierLeagueDataAnalyzer()
    
    try:
        # Generate comprehensive report
        report = analyzer.generate_comprehensive_report("2024-25")
        
        # Print summary
        analyzer.print_summary(report)
        
        # Export data
        csv_filename = analyzer.export_to_csv()
        if csv_filename:
            print(f"\n📄 Data exported to: {csv_filename}")
        
        # Save detailed report
        report_filename = f"analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_filename, 'w') as f:
            # Convert datetime objects to strings for JSON serialization
            import json
            from decimal import Decimal
            
            def convert_datetime(obj):
                if isinstance(obj, (datetime, date)):
                    return obj.isoformat()
                elif isinstance(obj, Decimal):
                    return float(obj)
                raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
            
            json.dump(report, f, indent=2, default=convert_datetime)
        
        print(f"📊 Detailed report saved to: {report_filename}")
        print("\n✅ Analysis completed successfully!")
        
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        print(f"\n❌ Analysis failed: {e}")
        return False
    
    return True


if __name__ == "__main__":
    main()
