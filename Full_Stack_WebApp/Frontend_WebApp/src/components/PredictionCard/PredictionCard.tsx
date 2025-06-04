import React from "react";
import { Prediction, Match } from "../../types";
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
    <div className={styles.card}>
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
            src={prediction.match.homeTeam.logo || "/placeholder-team.png"}
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
            src={prediction.match.awayTeam.logo || "/placeholder-team.png"}
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
    </div>
  );
};

export default PredictionCard;
