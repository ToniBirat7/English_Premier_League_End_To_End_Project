import React from "react";
import { Match } from "../types";
import "./MatchCard.css";

interface MatchCardProps {
  match: Match;
  showDate?: boolean;
  compact?: boolean;
}

const MatchCard: React.FC<MatchCardProps> = ({
  match,
  showDate = false,
  compact = false,
}) => {
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString("en-GB", {
      day: "2-digit",
      month: "short",
      year: showDate ? "numeric" : undefined,
    });
  };

  const formatTime = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleTimeString("en-GB", {
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  const getResultClass = () => {
    if (match.ftr === "H") return "home-win";
    if (match.ftr === "A") return "away-win";
    return "draw";
  };

  const getTeamLogo = (teamName: string) => {
    // Simple team emoji mapping - in a real app, you'd use actual logos
    const logoMap: { [key: string]: string } = {
      Arsenal: "🔴",
      Chelsea: "🔵",
      Liverpool: "🔴",
      "Man City": "💙",
      "Man United": "🔴",
      Tottenham: "⚪",
      Newcastle: "⚫",
      Brighton: "🔵",
      "West Ham": "⚒️",
      Everton: "🔵",
    };
    return logoMap[teamName] || "⚽";
  };

  return (
    <div
      className={`match-card ${compact ? "compact" : ""} ${getResultClass()}`}
    >
      {showDate && (
        <div className="match-date">
          <span className="date">{formatDate(match.date)}</span>
          <span className="season">{match.season}</span>
        </div>
      )}

      <div className="match-content">
        <div className="team home-team">
          <div className="team-info">
            <span className="team-logo">{getTeamLogo(match.home_team)}</span>
            <span className="team-name">{match.home_team}</span>
          </div>
          <span className="team-score">{match.fthg}</span>
        </div>

        <div className="match-separator">
          <span className="vs">VS</span>
          <div className="match-meta">
            <span className="matchweek">MW {match.matchweek}</span>
          </div>
        </div>

        <div className="team away-team">
          <span className="team-score">{match.ftag}</span>
          <div className="team-info">
            <span className="team-logo">{getTeamLogo(match.away_team)}</span>
            <span className="team-name">{match.away_team}</span>
          </div>
        </div>
      </div>

      <div className="match-result">
        <span className={`result-badge ${getResultClass()}`}>
          {match.ftr === "H" ? "H" : match.ftr === "A" ? "A" : "D"}
        </span>
      </div>
    </div>
  );
};

export default MatchCard;
