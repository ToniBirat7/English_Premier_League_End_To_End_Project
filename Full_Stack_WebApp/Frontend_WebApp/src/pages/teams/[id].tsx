import React, { useState, useEffect } from "react";
import { useRouter } from "next/router";
import Layout from "../../components/Layout/Layout";
import Loading from "../../components/Loading/Loading";
import MatchCard from "../../components/MatchCard/MatchCard";
import TeamStats from "../../components/TeamStats/TeamStats";
import { getTeam, getMatches } from "../../utils/api";
import { Team, Match } from "../../types";
import styles from "../../styles/TeamDetail.module.css";

const TeamDetailPage: React.FC = () => {
  const router = useRouter();
  const { id } = router.query;
  const [team, setTeam] = useState<Team | null>(null);
  const [matches, setMatches] = useState<Match[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchTeamData = async () => {
      if (!id) return;

      try {
        setLoading(true);
        const [teamData, matchesData] = await Promise.all([
          getTeam(Number(id)),
          getMatches(`team=${id}`),
        ]);
        setTeam(teamData);
        setMatches(matchesData);
        setError(null);
      } catch (err) {
        setError("Failed to fetch team data. Please try again later.");
        console.error("Error fetching team data:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchTeamData();
  }, [id]);

  const calculateTeamStats = (matches: Match[]) => {
    const completedMatches = matches.filter(
      (match) => match.status === "completed"
    );
    const stats = {
      played: completedMatches.length,
      wins: 0,
      draws: 0,
      losses: 0,
      goalsFor: 0,
      goalsAgainst: 0,
      points: 0,
      position: 0, // This would need to be fetched from the API
    };

    completedMatches.forEach((match) => {
      const isHomeTeam = match.homeTeam.id === Number(id);
      const teamScore = isHomeTeam ? match.homeScore : match.awayScore;
      const opponentScore = isHomeTeam ? match.awayScore : match.homeScore;

      if (teamScore !== null && opponentScore !== null) {
        stats.goalsFor += teamScore;
        stats.goalsAgainst += opponentScore;

        if (teamScore > opponentScore) {
          stats.wins++;
          stats.points += 3;
        } else if (teamScore === opponentScore) {
          stats.draws++;
          stats.points += 1;
        } else {
          stats.losses++;
        }
      }
    });

    return stats;
  };

  if (loading) {
    return (
      <Layout>
        <Loading message="Loading team information..." />
      </Layout>
    );
  }

  if (error || !team) {
    return (
      <Layout>
        <div className={styles.error}>{error || "Team not found"}</div>
      </Layout>
    );
  }

  const upcomingMatches = matches.filter(
    (match) => match.status === "scheduled"
  );
  const recentMatches = matches.filter((match) => match.status === "completed");
  const teamStats = calculateTeamStats(matches);

  return (
    <Layout>
      <div className={styles.container}>
        <div className={styles.header}>
          <div className={styles.logoContainer}>
            <img
              src={team.logo || "/placeholder-team.png"}
              alt={team.name}
              className={styles.logo}
            />
          </div>
          <div className={styles.info}>
            <h1 className={styles.name}>{team.name}</h1>
            <p className={styles.shortName}>{team.shortName}</p>
            <div className={styles.details}>
              <div className={styles.detail}>
                <span className={styles.label}>Stadium:</span>
                <span className={styles.value}>{team.stadium}</span>
              </div>
              <div className={styles.detail}>
                <span className={styles.label}>City:</span>
                <span className={styles.value}>{team.city}</span>
              </div>
              <div className={styles.detail}>
                <span className={styles.label}>Founded:</span>
                <span className={styles.value}>{team.founded}</span>
              </div>
              {team.website && (
                <div className={styles.detail}>
                  <span className={styles.label}>Website:</span>
                  <a
                    href={team.website}
                    target="_blank"
                    rel="noopener noreferrer"
                    className={styles.website}
                  >
                    {team.website}
                  </a>
                </div>
              )}
            </div>
          </div>
        </div>

        <div className={styles.section}>
          <h2 className={styles.sectionTitle}>Season Statistics</h2>
          <TeamStats stats={teamStats} />
        </div>

        <div className={styles.section}>
          <h2 className={styles.sectionTitle}>Upcoming Matches</h2>
          {upcomingMatches.length > 0 ? (
            <div className={styles.matches}>
              {upcomingMatches.map((match) => (
                <MatchCard key={match.id} match={match} />
              ))}
            </div>
          ) : (
            <p className={styles.noMatches}>No upcoming matches scheduled.</p>
          )}
        </div>

        <div className={styles.section}>
          <h2 className={styles.sectionTitle}>Recent Matches</h2>
          {recentMatches.length > 0 ? (
            <div className={styles.matches}>
              {recentMatches.slice(0, 5).map((match) => (
                <MatchCard key={match.id} match={match} />
              ))}
            </div>
          ) : (
            <p className={styles.noMatches}>No recent matches found.</p>
          )}
        </div>
      </div>
    </Layout>
  );
};

export default TeamDetailPage;
