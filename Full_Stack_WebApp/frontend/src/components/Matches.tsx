import React, { useState, useEffect } from "react";
import styled from "styled-components";
import { useNavigate } from "react-router-dom";
import { matchesApi, Match, formatTime } from "../services/api";
import { theme, Card } from "../styles/GlobalStyles";

const MatchesContainer = styled(Card)`
  background: ${theme.colors.secondary};
  padding: 0;
`;

const MatchesHeader = styled.div`
  padding: ${theme.spacing.lg};
  border-bottom: 1px solid ${theme.colors.border};
  display: flex;
  align-items: center;
  justify-content: space-between;
`;

const HeaderTitle = styled.h2`
  font-size: 18px;
  font-weight: bold;
  color: ${theme.colors.textPrimary};
  margin: 0;
`;

const FilterTabs = styled.div`
  display: flex;
  background: ${theme.colors.tertiary};
  border-radius: ${theme.borderRadius.md};
  padding: 2px;
`;

const FilterTab = styled.button<{ active?: boolean }>`
  padding: ${theme.spacing.sm} ${theme.spacing.md};
  background: ${(props) =>
    props.active ? theme.colors.purple : "transparent"};
  border: none;
  border-radius: ${theme.borderRadius.sm};
  color: ${(props) => (props.active ? "white" : theme.colors.textSecondary)};
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  &:hover {
    color: ${(props) => (props.active ? "white" : theme.colors.textPrimary)};
  }
`;

const RoundSelector = styled.div`
  display: flex;
  align-items: center;
  gap: ${theme.spacing.sm};
  padding: 0 ${theme.spacing.lg};
  border-bottom: 1px solid ${theme.colors.border};
`;

const RoundButton = styled.button`
  background: transparent;
  border: none;
  color: ${theme.colors.textSecondary};
  font-size: 14px;
  cursor: pointer;
  padding: ${theme.spacing.sm};

  &:hover {
    color: ${theme.colors.textPrimary};
  }
`;

const RoundInfo = styled.div`
  flex: 1;
  text-align: center;
  padding: ${theme.spacing.md} 0;
`;

const RoundTitle = styled.div`
  color: ${theme.colors.purple};
  font-size: 14px;
  font-weight: 500;
`;

const RoundDate = styled.div`
  color: ${theme.colors.textSecondary};
  font-size: 12px;
  margin-top: 2px;
`;

const MatchesList = styled.div`
  max-height: 600px;
  overflow-y: auto;
`;

const MatchItem = styled.div`
  padding: ${theme.spacing.md} ${theme.spacing.lg};
  border-bottom: 1px solid ${theme.colors.border};
  display: flex;
  align-items: center;
  gap: ${theme.spacing.md};
  transition: background-color 0.2s ease;
  cursor: pointer;

  &:hover {
    background: ${theme.colors.tertiary}30;
  }

  &:last-child {
    border-bottom: none;
  }
`;

const MatchTime = styled.div`
  min-width: 60px;
  text-align: center;
`;

const TimeText = styled.div`
  color: ${theme.colors.textSecondary};
  font-size: 12px;
  font-weight: 500;
`;

const StatusText = styled.div`
  color: ${theme.colors.textTertiary};
  font-size: 10px;
  margin-top: 2px;
`;

const MatchContent = styled.div`
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
`;

const TeamsContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: ${theme.spacing.sm};
  flex: 1;
`;

const TeamRow = styled.div`
  display: flex;
  align-items: center;
  gap: ${theme.spacing.sm};
`;

const TeamLogo = styled.div`
  width: 20px;
  height: 20px;
  background: ${theme.colors.tertiary};
  border-radius: ${theme.borderRadius.sm};
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  font-weight: bold;
`;

const TeamName = styled.span`
  color: ${theme.colors.textPrimary};
  font-size: 14px;
  font-weight: 500;
  min-width: 100px;
`;

const ScoreContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 60px;
`;

const Score = styled.div`
  display: flex;
  align-items: center;
  gap: ${theme.spacing.sm};
  font-size: 16px;
  font-weight: bold;
  color: ${theme.colors.textPrimary};
`;

const GoalCount = styled.span`
  min-width: 20px;
  text-align: center;
`;

const ScoreSeparator = styled.span`
  color: ${theme.colors.textSecondary};
  font-size: 14px;
`;

const MatchStatus = styled.div`
  color: ${theme.colors.textSecondary};
  font-size: 10px;
  margin-top: 2px;
`;

const MatchActions = styled.div`
  display: flex;
  align-items: center;
  gap: ${theme.spacing.sm};
`;

const StarButton = styled.button<{ starred?: boolean }>`
  background: transparent;
  border: none;
  color: ${(props) =>
    props.starred ? theme.colors.yellow : theme.colors.textTertiary};
  font-size: 16px;
  cursor: pointer;
  padding: ${theme.spacing.xs};

  &:hover {
    color: ${theme.colors.yellow};
  }
`;

const LoadingContainer = styled.div`
  padding: ${theme.spacing.xxl};
  text-align: center;
  color: ${theme.colors.textSecondary};
`;

interface MatchesProps {
  season?: string;
  team?: string;
}

const Matches: React.FC<MatchesProps> = ({ season = "2023-24", team }) => {
  const [matches, setMatches] = useState<Match[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeFilter, setActiveFilter] = useState("All");
  const [currentRound, setCurrentRound] = useState(1);
  const [roundDate, setRoundDate] = useState<string>("");
  const navigate = useNavigate();

  useEffect(() => {
    const fetchMatches = async () => {
      try {
        setLoading(true);
        // Fetch all matches for the season (not just page 1)
        const allMatches: Match[] = [];
        let page = 1;
        let hasMore = true;

        while (hasMore) {
          const data = await matchesApi.getMatches(page, season, team);
          allMatches.push(...data.results);
          hasMore = data.next !== null;
          page++;
        }

        // Filter matches for the current round
        const roundMatches = allMatches.filter(
          (match) => match.matchweek === currentRound
        );
        setMatches(roundMatches);

        // Set round date based on the first match in the round or season
        if (roundMatches.length > 0) {
          const firstMatch = roundMatches[0];
          const matchDate = new Date(firstMatch.date);
          const dateStr = matchDate.toLocaleDateString("en-GB", {
            day: "2-digit",
            month: "2-digit",
            year: "numeric",
          });
          const timeStr = formatTime(firstMatch.date);
          setRoundDate(`${dateStr} • ${timeStr}`);
        } else {
          // Fallback: estimate date based on season and round
          const estimatedDate = getEstimatedRoundDate(season, currentRound);
          setRoundDate(`${estimatedDate} • 15:00`);
        }
      } catch (error) {
        console.error("Error fetching matches:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchMatches();
  }, [season, team, currentRound]);

  const getTeamShortName = (teamName: string): string => {
    const shortNames: { [key: string]: string } = {
      Arsenal: "ARS",
      Chelsea: "CHE",
      Liverpool: "LIV",
      "Man City": "MCI",
      "Man United": "MUN",
      Tottenham: "TOT",
      Brighton: "BHA",
      Newcastle: "NEW",
      "West Ham": "WHU",
      "Aston Villa": "AVL",
      Bournemouth: "BOU",
      Leicester: "LEI",
      Fulham: "FUL",
      Ipswich: "IPS",
      Everton: "EVE",
      "Crystal Palace": "CRY",
      Brentford: "BRE",
      Wolves: "WOL",
      Southampton: "SOU",
    };
    return shortNames[teamName] || teamName.substring(0, 3).toUpperCase();
  };

  const getMatchStatus = (match: Match): string => {
    return "Finished";
  };

  const getEstimatedRoundDate = (season: string, round: number): string => {
    // Estimate date based on season and round
    const seasonStartYear = parseInt(season.split("-")[0]);
    const seasonStartDate = new Date(seasonStartYear, 7, 15); // August 15th as rough season start

    // Each round is approximately 1 week apart
    const estimatedDate = new Date(seasonStartDate);
    estimatedDate.setDate(estimatedDate.getDate() + (round - 1) * 7);

    return estimatedDate.toLocaleDateString("en-GB", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
    });
  };

  if (loading) {
    return (
      <MatchesContainer>
        <LoadingContainer>Loading matches...</LoadingContainer>
      </MatchesContainer>
    );
  }

  return (
    <MatchesContainer>
      <MatchesHeader>
        <HeaderTitle>Matches</HeaderTitle>
        <FilterTabs>
          {["All", "Favourites", "Live [0]", "Finished", "Upcoming"].map(
            (filter) => (
              <FilterTab
                key={filter}
                active={activeFilter === filter}
                onClick={() => setActiveFilter(filter)}
              >
                {filter}
              </FilterTab>
            )
          )}
        </FilterTabs>
      </MatchesHeader>

      <RoundSelector>
        <RoundButton
          onClick={() => setCurrentRound(Math.max(1, currentRound - 1))}
        >
          ◀
        </RoundButton>
        <RoundInfo>
          <RoundTitle>Round {currentRound}</RoundTitle>
          <RoundDate>{roundDate}</RoundDate>
        </RoundInfo>
        <RoundButton
          onClick={() => setCurrentRound(Math.min(38, currentRound + 1))}
        >
          ▶
        </RoundButton>
      </RoundSelector>

      <MatchesList>
        {matches.length === 0 ? (
          <LoadingContainer>
            No matches found for Round {currentRound}
          </LoadingContainer>
        ) : (
          matches.map((match) => (
            <MatchItem
              key={match.id}
              onClick={() => navigate(`/match/${match.id}`)}
            >
              <MatchTime>
                <TimeText>{formatTime(match.date)}</TimeText>
                <StatusText>FT</StatusText>
              </MatchTime>

              <MatchContent>
                <TeamsContainer>
                  <TeamRow>
                    <TeamLogo>{getTeamShortName(match.home_team)}</TeamLogo>
                    <TeamName>{match.home_team}</TeamName>
                  </TeamRow>
                  <TeamRow>
                    <TeamLogo>{getTeamShortName(match.away_team)}</TeamLogo>
                    <TeamName>{match.away_team}</TeamName>
                  </TeamRow>
                </TeamsContainer>

                <ScoreContainer>
                  <Score>
                    <GoalCount>{match.fthg}</GoalCount>
                    <ScoreSeparator>-</ScoreSeparator>
                    <GoalCount>{match.ftag}</GoalCount>
                  </Score>
                  <MatchStatus>{getMatchStatus(match)}</MatchStatus>
                </ScoreContainer>
              </MatchContent>

              <MatchActions>
                <StarButton starred={false}>☆</StarButton>
              </MatchActions>
            </MatchItem>
          ))
        )}
      </MatchesList>
    </MatchesContainer>
  );
};

export default Matches;
