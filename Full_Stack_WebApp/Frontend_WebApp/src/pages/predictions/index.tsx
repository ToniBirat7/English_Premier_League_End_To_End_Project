import React, { useState, useEffect } from "react";
import { useRouter } from "next/router";
import Layout from "../../components/Layout/Layout";
import PredictionCard from "../../components/PredictionCard/PredictionCard";
import Loading from "../../components/Loading/Loading";
import { getPredictions } from "../../utils/api";
import { Prediction } from "../../types";
import styles from "../../styles/Predictions.module.css";

const PredictionsPage: React.FC = () => {
  const router = useRouter();
  const [predictions, setPredictions] = useState<Prediction[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPredictions = async () => {
      try {
        setLoading(true);
        const data = await getPredictions();
        setPredictions(data);
        setError(null);
      } catch (err) {
        setError("Failed to fetch predictions. Please try again later.");
        console.error("Error fetching predictions:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchPredictions();
  }, []);

  const handleDelete = async (predictionId: number) => {
    try {
      // TODO: Implement delete prediction API call
      setPredictions(predictions.filter((p) => p.id !== predictionId));
    } catch (err) {
      console.error("Error deleting prediction:", err);
    }
  };

  const handleCreatePrediction = () => {
    router.push("/predictions/new");
  };

  if (loading) {
    return (
      <Layout>
        <Loading message="Loading predictions..." />
      </Layout>
    );
  }

  return (
    <Layout>
      <div className={styles.container}>
        <div className={styles.header}>
          <h1 className={styles.title}>Match Predictions</h1>
          <button
            onClick={handleCreatePrediction}
            className={styles.createButton}
          >
            Create New Prediction
          </button>
        </div>

        {error ? (
          <div className={styles.error}>{error}</div>
        ) : predictions.length > 0 ? (
          <div className={styles.predictions}>
            {predictions.map((prediction) => (
              <PredictionCard
                key={prediction.id}
                prediction={prediction}
                onDelete={() => handleDelete(prediction.id)}
              />
            ))}
          </div>
        ) : (
          <div className={styles.empty}>
            <p>No predictions found.</p>
            <button
              onClick={handleCreatePrediction}
              className={styles.createButton}
            >
              Create Your First Prediction
            </button>
          </div>
        )}
      </div>
    </Layout>
  );
};

export default PredictionsPage;
