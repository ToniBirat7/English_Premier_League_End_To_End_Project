import React from "react";
import { Prediction } from "../../types";
import { motion } from "framer-motion";
import styles from "./PredictionCard.module.css";

interface PredictionCardProps {
  prediction: Prediction;
  onDelete?: () => void;
}

const PredictionCard: React.FC<PredictionCardProps> = ({
  prediction,
  onDelete,
}) => {
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString("en-GB", {
      weekday: "short",
      day: "numeric",
      month: "short",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 80) return "#22c55e"; // High confidence
    if (confidence >= 60) return "#eab308"; // Medium confidence
    return "#ef4444"; // Low confidence
  };

  return (
    <motion.div
      className={`${styles.card} glass shadow`}
      whileHover={{
        scale: 1.04,
        boxShadow: "0 8px 32px 0 rgba(124,58,237,0.18)",
      }}
      whileTap={{ scale: 0.98 }}
      initial={{ opacity: 0, y: 40 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ type: "spring", stiffness: 120, damping: 18 }}
    >
      <div className={styles.header}>
        <span className={styles.date}>{formatDate(prediction.match.date)}</span>
        <div
          className={styles.confidence}
          style={{ color: getConfidenceColor(prediction.confidence) }}
        >
          {prediction.confidence}% Confidence
        </div>
      </div>

      <div className={styles.match}>
        <div className={styles.team}>
          <img
            src={
              prediction.match.homeTeam.logo ||
              "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%23666'%3E%3Cpath d='M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-13h2v6h-2zm0 8h2v2h-2z'/%3E%3C/svg%3E"
            }
            alt={prediction.match.homeTeam.name}
            className={styles.teamLogo}
          />
          <span className={styles.teamName}>
            {prediction.match.homeTeam.name}
          </span>
          <span className={styles.score}>{prediction.homeScore}</span>
        </div>
        <div className={styles.vs}>VS</div>
        <div className={styles.team}>
          <img
            src={
              prediction.match.awayTeam.logo ||
              "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%23666'%3E%3Cpath d='M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-13h2v6h-2zm0 8h2v2h-2z'/%3E%3C/svg%3E"
            }
            alt={prediction.match.awayTeam.name}
            className={styles.teamLogo}
          />
          <span className={styles.teamName}>
            {prediction.match.awayTeam.name}
          </span>
          <span className={styles.score}>{prediction.awayScore}</span>
        </div>
      </div>

      <div className={styles.footer}>
        <span className={styles.venue}>{prediction.match.venue}</span>
        {onDelete && (
          <button onClick={onDelete} className={styles.deleteButton}>
            Delete Prediction
          </button>
        )}
      </div>
    </motion.div>
  );
};

export default PredictionCard;
