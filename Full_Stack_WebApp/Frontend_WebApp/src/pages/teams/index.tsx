import React, { useState, useEffect } from "react";
import Layout from "../../components/Layout/Layout";
import TeamCard from "../../components/TeamCard/TeamCard";
import Loading from "../../components/Loading/Loading";
import { getTeams } from "../../utils/api";
import { Team } from "../../types";
import styles from "../../styles/Teams.module.css";

const TeamsPage: React.FC = () => {
  const [teams, setTeams] = useState<Team[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchTeams = async () => {
      try {
        setLoading(true);
        const data = await getTeams();
        setTeams(data);
        setError(null);
      } catch (err) {
        setError("Failed to fetch teams. Please try again later.");
        console.error("Error fetching teams:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchTeams();
  }, []);

  return (
    <Layout>
      <div className={styles.container}>
        <h1 className={styles.title}>Premier League Teams</h1>
        {loading ? (
          <Loading message="Loading teams..." />
        ) : error ? (
          <div className={styles.error}>{error}</div>
        ) : (
          <div className={styles.teams}>
            {teams.map((team) => (
              <TeamCard key={team.id} team={team} />
            ))}
          </div>
        )}
      </div>
    </Layout>
  );
};

export default TeamsPage;
