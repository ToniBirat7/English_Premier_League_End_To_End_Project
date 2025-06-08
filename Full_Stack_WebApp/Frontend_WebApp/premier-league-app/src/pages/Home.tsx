import React, { useState, useEffect } from 'react';
import { Match, StatsOverview } from '../types';
import { PremierLeagueAPI } from '../api';
import TestMatchCard from '../components/TestMatchCard';
import './Home.css';

const Home: React.FC = () => {
  const [recentMatches, setRecentMatches] = useState<Match[]>([]);
  const [statsOverview, setStatsOverview] = useState<StatsOverview | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);
        
        const [matches, stats] = await Promise.all([
          PremierLeagueAPI.getRecentMatches(),
          PremierLeagueAPI.getStatsOverview('2024-25')
        ]);
        
        setRecentMatches(matches.slice(0, 6)); // Show only first 6 matches
        setStatsOverview(stats);
      } catch (err) {
        setError('Failed to load data. Please try again.');
        console.error('Error fetching home data:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="home-page">
        <div className="loading-container">
          <div className="loading-spinner">⚽</div>
          <p>Loading Premier League data...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="home-page">
        <div className="error-container">
          <div className="error-icon">⚠️</div>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="home-page">
      <div className="hero-section">
        <div className="hero-content">
          <h1 className="hero-title">Premier League 2024-25</h1>
          <p className="hero-subtitle">Live scores, fixtures, and standings</p>
        </div>
        <div className="hero-stats">
          {statsOverview && (
            <>
              <div className="stat-card">
                <div className="stat-number">{statsOverview.total_matches}</div>
                <div className="stat-label">Matches Played</div>
              </div>
              <div className="stat-card">
                <div className="stat-number">{statsOverview.total_goals}</div>
                <div className="stat-label">Goals Scored</div>
              </div>
              <div className="stat-card">
                <div className="stat-number">{(statsOverview.total_goals / statsOverview.total_matches).toFixed(1)}</div>
                <div className="stat-label">Goals per Game</div>
              </div>
            </>
          )}
        </div>
      </div>

      <section className="recent-matches-section">
        <div className="section-header">
          <h2 className="section-title">Recent Matches</h2>
          <span className="section-subtitle">Latest results from the Premier League</span>
        </div>
        
        <div className="matches-grid">
          {recentMatches.map((match) => (
            <MatchCard
              key={match.id}
              match={match}
              showDate={true}
              compact={false}
            />
          ))}
        </div>
      </section>

      <section className="quick-stats-section">
        <div className="section-header">
          <h2 className="section-title">Season Highlights</h2>
        </div>
        
        <div className="highlights-grid">
          <div className="highlight-card">
            <div className="highlight-icon">🥅</div>
            <div className="highlight-content">
              <h3>Top Scorer</h3>
              <p>Most goals in a single match</p>
              <span className="highlight-value">6 goals</span>
            </div>
          </div>
          
          <div className="highlight-card">
            <div className="highlight-icon">🏆</div>
            <div className="highlight-content">
              <h3>Biggest Win</h3>
              <p>Largest victory margin</p>
              <span className="highlight-value">5-0</span>
            </div>
          </div>
          
          <div className="highlight-card">
            <div className="highlight-icon">⚽</div>
            <div className="highlight-content">
              <h3>Most Goals</h3>
              <p>Highest scoring match</p>
              <span className="highlight-value">7 goals</span>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;
