import React, { useState, useEffect } from 'react';
import { Match } from '../types';
import { PremierLeagueAPI } from '../api';
import MatchCard from '../components/MatchCard';
import './Fixtures.css';

const Fixtures: React.FC = () => {
  const [matches, setMatches] = useState<Match[]>([]);
  const [filteredMatches, setFilteredMatches] = useState<Match[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedSeason, setSelectedSeason] = useState('2024-25');
  const [selectedTeam, setSelectedTeam] = useState('all');
  const [seasons] = useState(['2024-25', '2023-24', '2022-23', '2021-22', '2020-21', '2019-20']);

  const teams = [
    'Arsenal', 'Chelsea', 'Liverpool', 'Man City', 'Man United', 'Tottenham',
    'Newcastle', 'Brighton', 'West Ham', 'Everton', 'Aston Villa', 'Crystal Palace',
    'Wolves', 'Leicester', 'Leeds', 'Southampton', 'Burnley', 'Watford',
    'Norwich', 'Brentford'
  ];

  useEffect(() => {
    fetchMatches();
  }, [selectedSeason]);

  useEffect(() => {
    filterMatches();
  }, [matches, selectedTeam]);

  const fetchMatches = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await PremierLeagueAPI.getMatches({
        season: selectedSeason,
        page_size: 100
      });
      
      setMatches(response.results);
    } catch (err) {
      setError('Failed to load fixtures. Please try again.');
      console.error('Error fetching fixtures:', err);
    } finally {
      setLoading(false);
    }
  };

  const filterMatches = () => {
    if (selectedTeam === 'all') {
      setFilteredMatches(matches);
    } else {
      const filtered = matches.filter(
        match => match.home_team === selectedTeam || match.away_team === selectedTeam
      );
      setFilteredMatches(filtered);
    }
  };

  const groupMatchesByMatchweek = (matches: Match[]) => {
    const grouped: { [key: number]: Match[] } = {};
    matches.forEach(match => {
      if (!grouped[match.matchweek]) {
        grouped[match.matchweek] = [];
      }
      grouped[match.matchweek].push(match);
    });
    return grouped;
  };

  if (loading) {
    return (
      <div className="fixtures-page">
        <div className="loading-container">
          <div className="loading-spinner">⚽</div>
          <p>Loading fixtures...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="fixtures-page">
        <div className="error-container">
          <div className="error-icon">⚠️</div>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  const groupedMatches = groupMatchesByMatchweek(filteredMatches);

  return (
    <div className="fixtures-page">
      <div className="page-header">
        <h1 className="page-title">Fixtures & Results</h1>
        <p className="page-subtitle">Complete schedule of Premier League matches</p>
      </div>

      <div className="filters-section">
        <div className="filter-group">
          <label htmlFor="season-select" className="filter-label">Season:</label>
          <select
            id="season-select"
            value={selectedSeason}
            onChange={(e) => setSelectedSeason(e.target.value)}
            className="filter-select"
          >
            {seasons.map(season => (
              <option key={season} value={season}>{season}</option>
            ))}
          </select>
        </div>

        <div className="filter-group">
          <label htmlFor="team-select" className="filter-label">Team:</label>
          <select
            id="team-select"
            value={selectedTeam}
            onChange={(e) => setSelectedTeam(e.target.value)}
            className="filter-select"
          >
            <option value="all">All Teams</option>
            {teams.map(team => (
              <option key={team} value={team}>{team}</option>
            ))}
          </select>
        </div>

        <div className="results-count">
          <span className="count-badge">
            {filteredMatches.length} matches found
          </span>
        </div>
      </div>

      <div className="fixtures-content">
        {Object.entries(groupedMatches)
          .sort(([a], [b]) => parseInt(a) - parseInt(b))
          .map(([matchweek, weekMatches]) => (
            <div key={matchweek} className="matchweek-section">
              <div className="matchweek-header">
                <h2 className="matchweek-title">Matchweek {matchweek}</h2>
                <span className="matchweek-count">{weekMatches.length} matches</span>
              </div>
              
              <div className="matches-grid">
                {weekMatches
                  .sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime())
                  .map((match) => (
                    <MatchCard
                      key={match.id}
                      match={match}
                      showDate={true}
                      compact={true}
                    />
                  ))}
              </div>
            </div>
          ))}
      </div>

      {filteredMatches.length === 0 && !loading && (
        <div className="no-results">
          <div className="no-results-icon">📅</div>
          <h3>No matches found</h3>
          <p>Try adjusting your filters to see more results.</p>
        </div>
      )}
    </div>
  );
};

export default Fixtures;
