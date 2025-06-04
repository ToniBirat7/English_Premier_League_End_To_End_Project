import React, { useState, useEffect } from "react";
import { useRouter } from "next/router";
import Layout from "../../components/Layout/Layout";
import MatchCard from "../../components/MatchCard/MatchCard";
import MatchFilters from "../../components/MatchFilters/MatchFilters";
import Loading from "../../components/Loading/Loading";
import { getMatches } from "../../utils/api";
import { Match } from "../../types";
import styles from "../../styles/Matches.module.css";

const MatchesPage: React.FC = () => {
  const router = useRouter();
  const [matches, setMatches] = useState<Match[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [status, setStatus] = useState("");
  const [sortBy, setSortBy] = useState("match_date");

  useEffect(() => {
    const fetchMatches = async () => {
      try {
        setLoading(true);
        const params = new URLSearchParams();
        if (status) params.append("status", status);
        if (sortBy) params.append("ordering", sortBy);

        const data = await getMatches(params.toString());
        setMatches(data);
        setError(null);
      } catch (err) {
        setError("Failed to fetch matches. Please try again later.");
        console.error("Error fetching matches:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchMatches();
  }, [status, sortBy]);

  const handlePredict = (matchId: number) => {
    router.push(`/predictions/new?matchId=${matchId}`);
  };

  return (
    <Layout>
      <div className={styles.container}>
        <h1 className={styles.title}>Matches</h1>
        <MatchFilters
          status={status}
          onStatusChange={setStatus}
          sortBy={sortBy}
          onSortChange={setSortBy}
        />
        {loading ? (
          <Loading message="Loading matches..." />
        ) : error ? (
          <div className={styles.error}>{error}</div>
        ) : (
          <div className={styles.matches}>
            {matches.length > 0 ? (
              matches.map((match) => (
                <MatchCard
                  key={match.id}
                  match={match}
                  onPredict={() => handlePredict(match.id)}
                />
              ))
            ) : (
              <div className={styles.noMatches}>
                No matches found with the selected filters.
              </div>
            )}
          </div>
        )}
      </div>
    </Layout>
  );
};

export default MatchesPage;
