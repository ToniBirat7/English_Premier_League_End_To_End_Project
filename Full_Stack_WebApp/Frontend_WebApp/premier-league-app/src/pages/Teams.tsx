import React, { useState, useEffect } from 'react';
import { Team, Match, TeamStats } from '../types';
import { PremierLeagueAPI } from '../api';
import MatchCard from '../components/MatchCard';
import './Teams.css';

const Teams: React.FC = () => {
  const [teams, setTeams] = useState<Team[]>([]);
  const [selectedTeam, setSelectedTeam] = useState<Team | null>(null);
  const [teamMatches, setTeamMatches] = useState<Match[]>([]);
  const [teamStats, setTeamStats] = useState<TeamStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [matchesLoading, setMatchesLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedSeason, setSelectedSeason] = useState('2024-25');

  const seasons = ['2024-25', '2023-24', '2022-23', '2021-22', '2020-21', '2019-20'];

  useEffect(() => {
    fetchTeams();
  }, []);

  useEffect(() => {
    if (selectedTeam) {
      fetchTeamData();
    }
  }, [selectedTeam, selectedSeason]);

  const fetchTeams = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const teamsData = await PremierLeagueAPI.getTeams();
      setTeams(teamsData);
    } catch (err) {
      setError('Failed to load teams. Please try again.');
      console.error('Error fetching teams:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchTeamData = async () => {
    if (!selectedTeam) return;
    
    try {
      setMatchesLoading(true);
      
      const [matches, stats] = await Promise.all([
        PremierLeagueAPI.getTeamMatches(selectedTeam.id, selectedSeason),
        PremierLeagueAPI.getTeamStats(selectedTeam.id, selectedSeason)
      ]);
      
      setTeamMatches(matches.results);
      setTeamStats(stats);
    } catch (err) {
      console.error('Error fetching team data:', err);
    } finally {
      setMatchesLoading(false);
    }
  };

  const getTeamLogo = (teamName: string) => {
    const logoMap: { [key: string]: string } = {
      'Arsenal': '🔴', 'Chelsea': '🔵', 'Liverpool': '🔴', 'Man City': '💙',
      'Man United': '🔴', 'Tottenham': '⚪', 'Newcastle': '⚫', 'Brighton': '🔵',
      'West Ham': '⚒️', 'Everton': '🔵', 'Aston Villa': '🟣', 'Crystal Palace': '🦅',
      'Wolves': '🟠', 'Leicester': '🦊', 'Leeds': '⚪', 'Southampton': '🔴',
      'Burnley': '🟤', 'Watford': '🟡', 'Norwich': '🟡', 'Brentford': '🔴'
    };
    return logoMap[teamName] || '⚽';
  };

  const getFormClass = (result: string) => {
    if (result === 'H' || result === 'A') return 'win';
    if (result === 'D') return 'draw';
    return 'loss';
  };

  if (loading) {
    return (
      <div className="teams-page">
        <div className="loading-container">
          <div className="loading-spinner">👥</div>
          <p>Loading teams...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="teams-page">
        <div className="error-container">
          <div className="error-icon">⚠️</div>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="teams-page">
      <div className="page-header">
        <h1 className="page-title">Teams</h1>
        <p className="page-subtitle">Premier League team profiles and statistics</p>
      </div>

      <div className="teams-layout">
        <div className="teams-sidebar">
          <div className="teams-header">
            <h2>Premier League Teams</h2>
            <span className="teams-count">{teams.length} teams</span>
          </div>
          
          <div className="teams-grid">
            {teams.map((team) => (
              <div
                key={team.id}
                className={`team-card ${selectedTeam?.id === team.id ? 'active' : ''}`}
                onClick={() => setSelectedTeam(team)}
              >
                <div className="team-logo-large">
                  {getTeamLogo(team.name)}
                </div>
                <span className="team-name">{team.name}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="team-details">
          {!selectedTeam ? (
            <div className="select-team-prompt">
              <div className="prompt-icon">👆</div>
              <h3>Select a team</h3>
              <p>Choose a team from the left to view their profile and statistics</p>
            </div>
          ) : (
            <>
              <div className="team-profile">
                <div className="profile-header">
                  <div className="team-info-large">
                    <div className="team-logo-xl">
                      {getTeamLogo(selectedTeam.name)}
                    </div>
                    <div className="team-text">
                      <h2 className="team-name-large">{selectedTeam.name}</h2>
                      <p className="team-description">Premier League Team</p>
                    </div>
                  </div>
                  
                  <div className="season-selector">
                    <label htmlFor="season-select">Season:</label>
                    <select
                      id="season-select"
                      value={selectedSeason}
                      onChange={(e) => setSelectedSeason(e.target.value)}
                      className="season-select"
                    >
                      {seasons.map(season => (
                        <option key={season} value={season}>{season}</option>
                      ))}
                    </select>
                  </div>
                </div>

                {teamStats && (
                  <div className="team-statistics">
                    <h3>Season Statistics</h3>
                    <div className="stats-grid">
                      <div className="stat-item">
                        <div className="stat-value">{teamStats.matches_played}</div>
                        <div className="stat-label">Matches</div>
                      </div>
                      <div className="stat-item">
                        <div className="stat-value">{teamStats.wins}</div>
                        <div className="stat-label">Wins</div>
                      </div>
                      <div className="stat-item">
                        <div className="stat-value">{teamStats.draws}</div>
                        <div className="stat-label">Draws</div>
                      </div>
                      <div className="stat-item">
                        <div className="stat-value">{teamStats.losses}</div>
                        <div className="stat-label">Losses</div>
                      </div>
                      <div className="stat-item">
                        <div className="stat-value">{teamStats.goals_for}</div>
                        <div className="stat-label">Goals For</div>
                      </div>
                      <div className="stat-item">
                        <div className="stat-value">{teamStats.goals_against}</div>
                        <div className="stat-label">Goals Against</div>
                      </div>
                      <div className="stat-item">
                        <div className={`stat-value ${teamStats.goal_difference >= 0 ? 'positive' : 'negative'}`}>
                          {teamStats.goal_difference >= 0 ? '+' : ''}{teamStats.goal_difference}
                        </div>
                        <div className="stat-label">Goal Difference</div>
                      </div>
                      <div className="stat-item highlighted">
                        <div className="stat-value">{teamStats.points}</div>
                        <div className="stat-label">Points</div>
                      </div>
                    </div>
                  </div>
                )}
              </div>

              <div className="team-matches-section">
                <h3>Recent Matches</h3>
                
                {matchesLoading ? (
                  <div className="matches-loading">
                    <div className="loading-spinner">⚽</div>
                    <p>Loading matches...</p>
                  </div>
                ) : (
                  <div className="matches-list">
                    {teamMatches.slice(0, 10).map((match) => (
                      <MatchCard
                        key={match.id}
                        match={match}
                        showDate={true}
                        compact={true}
                      />
                    ))}
                    
                    {teamMatches.length === 0 && (
                      <div className="no-matches">
                        <p>No matches found for this season.</p>
                      </div>
                    )}
                  </div>
                )}
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default Teams;
