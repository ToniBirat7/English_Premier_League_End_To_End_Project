import React, { useState, useEffect, useCallback } from "react";
import { TeamStats } from "../types";
import { PremierLeagueAPI } from "../api";
import "./Table.css";

const LeagueTablePage: React.FC = () => {
  const [leagueTable, setLeagueTable] = useState<TeamStats[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedSeason, setSelectedSeason] = useState("2024-25");
  const [sortBy, setSortBy] = useState<keyof TeamStats | "team_name">("points");
  const [sortOrder, setSortOrder] = useState<"asc" | "desc">("desc");

  const seasons = [
    "2024-25",
    "2023-24",
    "2022-23",
    "2021-22",
    "2020-21",
    "2019-20",
  ];

  const fetchLeagueTable = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);

      const table = await PremierLeagueAPI.getLeagueTable(selectedSeason);
      setLeagueTable(table);
    } catch (err) {
      setError("Failed to load league table. Please try again.");
      console.error("Error fetching league table:", err);
    } finally {
      setLoading(false);
    }
  }, [selectedSeason]);

  useEffect(() => {
    fetchLeagueTable();
  }, [fetchLeagueTable]);

  const sortTable = (field: keyof TeamStats | "team_name") => {
    const newOrder = sortBy === field && sortOrder === "desc" ? "asc" : "desc";
    setSortBy(field);
    setSortOrder(newOrder);

    const sorted = [...leagueTable].sort((a, b) => {
      let aVal, bVal;

      if (field === "team_name") {
        aVal = a.team.name;
        bVal = b.team.name;
      } else {
        aVal = a[field as keyof TeamStats];
        bVal = b[field as keyof TeamStats];
      }

      if (typeof aVal === "number" && typeof bVal === "number") {
        return newOrder === "desc" ? bVal - aVal : aVal - bVal;
      }

      const aStr = String(aVal).toLowerCase();
      const bStr = String(bVal).toLowerCase();
      return newOrder === "desc"
        ? bStr.localeCompare(aStr)
        : aStr.localeCompare(bStr);
    });

    setLeagueTable(sorted);
  };

  const getQualificationClass = (position: number) => {
    if (position <= 4) return "champions-league";
    if (position === 5) return "europa-league";
    if (position === 6) return "conference-league";
    if (position >= 18) return "relegation";
    return "";
  };

  const getTeamLogo = (teamName: string) => {
    const logos: { [key: string]: string } = {
      Arsenal: "🔴",
      Chelsea: "🔵",
      Liverpool: "🔴",
      "Man City": "💙",
      "Man United": "🔴",
      Tottenham: "⚪",
      Newcastle: "⚫",
      Brighton: "🔵",
      "Aston Villa": "🟣",
      "West Ham": "⚒️",
      "Crystal Palace": "🦅",
      Fulham: "⚪",
      Wolves: "🟠",
      Everton: "🔵",
      Brentford: "🔴",
      "Nottingham Forest": "🔴",
      "Leicester City": "🦊",
      Southampton: "🔴",
      "Ipswich Town": "🔵",
      Bournemouth: "🔴",
    };
    return logos[teamName] || "⚽";
  };

  if (loading) {
    return (
      <div className="table-page">
        <div className="loading-container">
          <div className="loading-spinner">📊</div>
          <p>Loading league table...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="table-page">
        <div className="error-container">
          <div className="error-icon">⚠️</div>
          <p>{error}</p>
          <button onClick={fetchLeagueTable} className="retry-button">
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="table-page">
      <div className="page-header">
        <h1 className="page-title">League Table</h1>
        <div className="controls">
          <div className="season-selector">
            <label htmlFor="season">Season:</label>
            <select
              id="season"
              value={selectedSeason}
              onChange={(e) => setSelectedSeason(e.target.value)}
              className="season-select"
            >
              {seasons.map((season) => (
                <option key={season} value={season}>
                  {season}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      <div className="table-container">
        <table className="league-table">
          <thead>
            <tr>
              <th className="position-col">Pos</th>
              <th className="team-col" onClick={() => sortTable("team_name")}>
                Team{" "}
                {sortBy === "team_name" && (sortOrder === "desc" ? "↓" : "↑")}
              </th>
              <th
                onClick={() => sortTable("matches_played")}
                className="sortable"
              >
                P{" "}
                {sortBy === "matches_played" &&
                  (sortOrder === "desc" ? "↓" : "↑")}
              </th>
              <th onClick={() => sortTable("wins")} className="sortable">
                W {sortBy === "wins" && (sortOrder === "desc" ? "↓" : "↑")}
              </th>
              <th onClick={() => sortTable("draws")} className="sortable">
                D {sortBy === "draws" && (sortOrder === "desc" ? "↓" : "↑")}
              </th>
              <th onClick={() => sortTable("losses")} className="sortable">
                L {sortBy === "losses" && (sortOrder === "desc" ? "↓" : "↑")}
              </th>
              <th onClick={() => sortTable("goals_for")} className="sortable">
                GF{" "}
                {sortBy === "goals_for" && (sortOrder === "desc" ? "↓" : "↑")}
              </th>
              <th
                onClick={() => sortTable("goals_against")}
                className="sortable"
              >
                GA{" "}
                {sortBy === "goals_against" &&
                  (sortOrder === "desc" ? "↓" : "↑")}
              </th>
              <th
                onClick={() => sortTable("goal_difference")}
                className="sortable"
              >
                GD{" "}
                {sortBy === "goal_difference" &&
                  (sortOrder === "desc" ? "↓" : "↑")}
              </th>
              <th
                onClick={() => sortTable("points")}
                className="sortable points-col"
              >
                Pts {sortBy === "points" && (sortOrder === "desc" ? "↓" : "↑")}
              </th>
            </tr>
          </thead>
          <tbody>
            {leagueTable.map((teamData, index) => (
              <tr
                key={teamData.team.id}
                className={`table-row ${getQualificationClass(index + 1)}`}
              >
                <td className="position">{index + 1}</td>
                <td className="team-cell">
                  <span className="team-logo">
                    {getTeamLogo(teamData.team.name)}
                  </span>
                  <span className="team-name">{teamData.team.name}</span>
                </td>
                <td>{teamData.matches_played}</td>
                <td>{teamData.wins}</td>
                <td>{teamData.draws}</td>
                <td>{teamData.losses}</td>
                <td>{teamData.goals_for}</td>
                <td>{teamData.goals_against}</td>
                <td
                  className={
                    teamData.goal_difference >= 0 ? "positive" : "negative"
                  }
                >
                  {teamData.goal_difference >= 0 ? "+" : ""}
                  {teamData.goal_difference}
                </td>
                <td className="points">{teamData.points}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="table-legend">
        <h3>Qualification</h3>
        <div className="legend-items">
          <div className="legend-item champions-league">
            <span className="legend-color"></span>
            <span>Champions League (1-4)</span>
          </div>
          <div className="legend-item europa-league">
            <span className="legend-color"></span>
            <span>Europa League (5)</span>
          </div>
          <div className="legend-item conference-league">
            <span className="legend-color"></span>
            <span>Conference League (6)</span>
          </div>
          <div className="legend-item relegation">
            <span className="legend-color"></span>
            <span>Relegation (18-20)</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LeagueTablePage;
