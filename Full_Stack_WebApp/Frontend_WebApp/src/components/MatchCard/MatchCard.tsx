import React from "react";
import { Match } from "../../types";
import styles from "./MatchCard.module.css";

interface MatchCardProps {
  match: Match;
  onPredict?: () => void;
}

const MatchCard: React.FC<MatchCardProps> = ({ match, onPredict }) => {
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

  return (
    <div className={styles.card}>
      <div className={styles.header}>
        <span className={styles.status}>{match.status.toUpperCase()}</span>
        <span className={styles.date}>{formatDate(match.match_date)}</span>
      </div>
      <div className={styles.teams}>
        <div className={styles.team}>
          <img
            src={match.home_team.logo || "/placeholder-team.png"}
            alt={match.home_team.name}
            className={styles.teamLogo}
          />
          <span className={styles.teamName}>{match.home_team.name}</span>
          {match.home_score !== null && (
            <span className={styles.score}>{match.home_score}</span>
          )}
        </div>
        <div className={styles.vs}>VS</div>
        <div className={styles.team}>
          <img
            src={match.away_team.logo || "/placeholder-team.png"}
            alt={match.away_team.name}
            className={styles.teamLogo}
          />
          <span className={styles.teamName}>{match.away_team.name}</span>
          {match.away_score !== null && (
            <span className={styles.score}>{match.away_score}</span>
          )}
        </div>
      </div>
      <div className={styles.footer}>
        <span className={styles.stadium}>{match.stadium}</span>
        {match.status === "scheduled" && onPredict && (
          <button onClick={onPredict} className={styles.predictButton}>
            Predict Match
          </button>
        )}
      </div>
    </div>
  );
};

export default MatchCard;