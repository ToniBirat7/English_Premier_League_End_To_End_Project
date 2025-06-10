import React, { useState, useEffect } from "react";
import styled, { keyframes, css } from "styled-components";
import { useNavigate } from "react-router-dom";
import { matchesApi, Match, formatTime } from "../services/api";
import { theme, Card } from "../styles/GlobalStyles";
import LoadingSpinner from "./LoadingSpinner";

// Enhanced animations
const slideInUp = keyframes`
  0% {
    opacity: 0;
    transform: translateY(30px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
`;

const glowPulse = keyframes`
  0%, 100% {
    box-shadow: 0 0 5px rgba(139, 92, 246, 0.3);
  }
  50% {
    box-shadow: 0 0 20px rgba(139, 92, 246, 0.6), 0 0 30px rgba(139, 92, 246, 0.4);
  }
`;

const shimmerAnimation = keyframes`
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
`;

const progressAnimation = keyframes`
  50% { opacity: 1; transform: translateX(0%); }
  100% { opacity: 0.3; transform: translateX(100%); }
`;

const sparkleMove = keyframes`
  0% { transform: translateX(-100%) translateY(-100%); }
  100% { transform: translateX(100%) translateY(100%); }
`;

const starGlow = keyframes`
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
`;

const starRotate = keyframes`
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
`;

const MatchesContainer = styled(Card)`
  background: ${theme.colors.secondary};
  padding: 0;
  animation: ${slideInUp} 0.6s ease-out;
  overflow: hidden;
  position: relative;

  &::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(
      90deg,
      transparent,
      ${theme.colors.purple},
      transparent
    );
    opacity: 0.6;
  }
`;

const MatchesHeader = styled.div`
  padding: ${theme.spacing.lg};
  border-bottom: 1px solid ${theme.colors.border};
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: linear-gradient(
    135deg,
    rgba(139, 92, 246, 0.02) 0%,
    rgba(59, 130, 246, 0.02) 100%
  );
  backdrop-filter: blur(10px);
`;

const HeaderTitle = styled.h2`
  font-size: 20px;
  font-weight: 700;
  color: ${theme.colors.textPrimary};
  margin: 0;
  position: relative;

  &::after {
    content: "";
    position: absolute;
    bottom: -4px;
    left: 0;
    width: 30px;
    height: 2px;
    background: linear-gradient(
      90deg,
      ${theme.colors.purple},
      ${theme.colors.blue}
    );
    border-radius: 1px;
  }
`;

const FilterTabs = styled.div`
  display: flex;
  background: rgba(255, 255, 255, 0.03);
  border-radius: ${theme.borderRadius.xl};
  padding: 4px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(139, 92, 246, 0.1);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  position: relative;
  overflow: hidden;

  &::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(
      45deg,
      transparent 0%,
      rgba(139, 92, 246, 0.1) 25%,
      transparent 50%,
      rgba(59, 130, 246, 0.1) 75%,
      transparent 100%
    );
    animation: ${shimmerAnimation} 3s ease-in-out infinite;
    pointer-events: none;
  }

  &:hover {
    border-color: rgba(139, 92, 246, 0.3);
    box-shadow: 0 8px 25px rgba(139, 92, 246, 0.2);
    transform: translateY(-2px);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }
`;

const FilterTab = styled.button<{ active?: boolean }>`
  padding: ${theme.spacing.sm} ${theme.spacing.md};
  background: ${(props) =>
    props.active
      ? "linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%)"
      : "transparent"};
  border: none;
  border-radius: ${theme.borderRadius.lg};
  color: ${(props) => (props.active ? "white" : theme.colors.textSecondary)};
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
  min-width: 60px;
  z-index: 1;

  &::before {
    content: "";
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(
      90deg,
      transparent,
      rgba(255, 255, 255, 0.1),
      transparent
    );
    transition: left 0.5s ease;
    z-index: -1;
  }

  &::after {
    content: "";
    position: absolute;
    bottom: 0;
    left: 50%;
    width: 0;
    height: 2px;
    background: linear-gradient(
      90deg,
      ${theme.colors.purple},
      ${theme.colors.blue}
    );
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    transform: translateX(-50%);
  }

  &:hover {
    color: ${(props) => (props.active ? "white" : theme.colors.textPrimary)};
    background: ${(props) =>
      props.active
        ? "linear-gradient(135deg, #7c3aed 0%, #8b5cf6 100%)"
        : "rgba(139, 92, 246, 0.1)"};
    transform: translateY(-1px) scale(1.05);
    box-shadow: 0 4px 12px rgba(139, 92, 246, 0.2);

    &::before {
      left: 100%;
    }

    &::after {
      width: 80%;
    }
  }

  &:active {
    transform: translateY(0) scale(0.98);
  }

  ${(props) =>
    props.active &&
    `
    box-shadow: 0 2px 10px rgba(139, 92, 246, 0.3);
    
    &::after {
      width: 100%;
    }
  `}
`;

const RoundSelector = styled.div`
  display: flex;
  align-items: center;
  gap: ${theme.spacing.sm};
  padding: ${theme.spacing.lg};
  border-bottom: 1px solid ${theme.colors.border};
  background: linear-gradient(
    135deg,
    rgba(139, 92, 246, 0.01) 0%,
    rgba(59, 130, 246, 0.01) 100%
  );
  position: relative;
  overflow: hidden;

  &::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(
      90deg,
      transparent,
      ${theme.colors.purple}60,
      ${theme.colors.blue}60,
      transparent
    );
    animation: ${progressAnimation} 3s ease-in-out infinite;
  }

  &::after {
    content: "";
    position: absolute;
    bottom: 0;
    left: 20%;
    right: 20%;
    height: 1px;
    background: linear-gradient(
      90deg,
      transparent,
      ${theme.colors.purple}30,
      transparent
    );
  }

  &:hover {
    background: linear-gradient(
      135deg,
      rgba(139, 92, 246, 0.03) 0%,
      rgba(59, 130, 246, 0.03) 100%
    );
    transform: translateY(-1px);
    box-shadow: 0 4px 20px rgba(139, 92, 246, 0.1);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }
`;

const RoundButton = styled.button`
  background: rgba(255, 255, 255, 0.05);
  border: 2px solid transparent;
  color: ${theme.colors.textSecondary};
  font-size: 16px;
  cursor: pointer;
  padding: ${theme.spacing.sm};
  border-radius: ${theme.borderRadius.lg};
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;

  &::before {
    content: "";
    position: absolute;
    top: 50%;
    left: 50%;
    width: 0;
    height: 0;
    background: radial-gradient(
      circle,
      rgba(139, 92, 246, 0.2) 0%,
      transparent 70%
    );
    transition: all 0.3s ease;
    transform: translate(-50%, -50%);
    border-radius: 50%;
  }

  &:hover {
    color: ${theme.colors.purple};
    background: rgba(139, 92, 246, 0.1);
    border-color: rgba(139, 92, 246, 0.3);
    transform: scale(1.1);
    box-shadow: 0 4px 15px rgba(139, 92, 246, 0.2);

    &::before {
      width: 80px;
      height: 80px;
    }
  }

  &:active {
    transform: scale(0.95);
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none;

    &:hover {
      background: rgba(255, 255, 255, 0.05);
      border-color: transparent;
      box-shadow: none;
    }
  }
`;

const RoundInfo = styled.div`
  flex: 1;
  text-align: center;
  padding: ${theme.spacing.md} 0;
  position: relative;
`;

const RoundTitle = styled.div`
  color: ${theme.colors.purple};
  font-size: 16px;
  font-weight: 700;
  margin-bottom: 4px;
  animation: ${glowPulse} 3s ease-in-out infinite;
`;

const RoundDate = styled.div`
  color: ${theme.colors.textSecondary};
  font-size: 12px;
  font-weight: 500;
  opacity: 0.8;
`;

const MatchesList = styled.div`
  max-height: 600px;
  overflow-y: auto;

  /* Custom scrollbar styling */
  &::-webkit-scrollbar {
    width: 8px;
  }

  &::-webkit-scrollbar-track {
    background: ${theme.colors.tertiary};
    border-radius: 4px;
  }

  &::-webkit-scrollbar-thumb {
    background: ${theme.colors.border};
    border-radius: 4px;

    &:hover {
      background: ${theme.colors.textTertiary};
    }
  }

  /* Firefox scrollbar styling */
  scrollbar-width: thin;
  scrollbar-color: ${theme.colors.border} ${theme.colors.tertiary};

  /* Responsive height adjustments */
  @media (max-width: ${theme.breakpoints.tablet}) {
    max-height: 500px;
  }

  @media (max-width: ${theme.breakpoints.mobile}) {
    max-height: 400px;
  }
`;

const MatchItem = styled.div`
  padding: ${theme.spacing.md} ${theme.spacing.lg};
  border-bottom: 1px solid ${theme.colors.border};
  display: flex;
  align-items: center;
  gap: ${theme.spacing.md};
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  position: relative;
  overflow: hidden;
  background: transparent;
  animation: ${slideInUp} 0.6s ease-out both;

  &::before {
    content: "";
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(
      90deg,
      transparent,
      rgba(139, 92, 246, 0.05),
      transparent
    );
    transition: left 0.5s ease;
  }

  &::after {
    content: "";
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 0;
    background: linear-gradient(
      135deg,
      ${theme.colors.purple} 0%,
      ${theme.colors.blue} 100%
    );
    transition: width 0.3s ease;
  }

  &:hover {
    background: rgba(139, 92, 246, 0.03);
    transform: translateX(8px);
    box-shadow: 0 8px 25px rgba(139, 92, 246, 0.1);

    &::before {
      left: 100%;
    }

    &::after {
      width: 4px;
    }

    .team-logo {
      transform: scale(1.1) rotate(5deg);
    }

    .score-container {
      transform: scale(1.05);
    }

    .star-button {
      transform: scale(1.2) rotate(18deg);
    }
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
  width: 24px;
  height: 24px;
  background: linear-gradient(
    135deg,
    ${theme.colors.tertiary} 0%,
    ${theme.colors.secondary} 100%
  );
  border-radius: ${theme.borderRadius.md};
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  font-weight: 700;
  color: ${theme.colors.textPrimary};
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid rgba(139, 92, 246, 0.1);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: relative;
  overflow: hidden;

  &::before {
    content: "";
    position: absolute;
    top: 50%;
    left: 50%;
    width: 0;
    height: 0;
    background: radial-gradient(
      circle,
      rgba(139, 92, 246, 0.3) 0%,
      transparent 70%
    );
    transition: all 0.3s ease;
    transform: translate(-50%, -50%);
    border-radius: 50%;
  }

  &::after {
    content: "";
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(
      90deg,
      transparent,
      rgba(255, 255, 255, 0.2),
      transparent
    );
    transition: left 0.5s ease;
  }

  &:hover {
    transform: scale(1.15) rotate(10deg);
    box-shadow: 0 4px 15px rgba(139, 92, 246, 0.3);
    background: linear-gradient(
      135deg,
      rgba(139, 92, 246, 0.1) 0%,
      ${theme.colors.tertiary} 100%
    );

    &::before {
      width: 40px;
      height: 40px;
    }

    &::after {
      left: 100%;
    }
  }
`;

const TeamName = styled.span`
  color: ${theme.colors.textPrimary};
  font-size: 14px;
  font-weight: 600;
  min-width: 120px;
  transition: color 0.3s ease;
`;

const ScoreContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 80px;
  padding: ${theme.spacing.sm};
  border-radius: ${theme.borderRadius.md};
  background: rgba(255, 255, 255, 0.02);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;

  &::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(
      45deg,
      transparent 30%,
      rgba(139, 92, 246, 0.1) 50%,
      transparent 70%
    );
    opacity: 0;
    transition: all 0.3s ease;
    animation: ${sparkleMove} 2s ease-in-out infinite;
  }

  &:hover {
    transform: scale(1.08);
    background: rgba(139, 92, 246, 0.08);
    box-shadow: 0 4px 20px rgba(139, 92, 246, 0.2);

    &::before {
      opacity: 1;
    }
  }
`;

const Score = styled.div`
  display: flex;
  align-items: center;
  gap: ${theme.spacing.sm};
  font-size: 18px;
  font-weight: 800;
  color: ${theme.colors.textPrimary};
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  position: relative;

  &::before {
    content: "";
    position: absolute;
    top: 50%;
    left: 50%;
    width: 0;
    height: 0;
    background: radial-gradient(
      circle,
      rgba(139, 92, 246, 0.4) 0%,
      transparent 70%
    );
    transition: all 0.3s ease;
    transform: translate(-50%, -50%);
    border-radius: 50%;
    z-index: -1;
  }

  &:hover {
    transform: scale(1.1);
    color: ${theme.colors.purple};
    text-shadow: 0 0 10px rgba(139, 92, 246, 0.5);

    &::before {
      width: 60px;
      height: 60px;
    }
  }
`;

const GoalCount = styled.span`
  min-width: 24px;
  text-align: center;
`;

const ScoreSeparator = styled.span`
  color: ${theme.colors.textSecondary};
  font-size: 14px;
  font-weight: 600;
`;

const MatchStatus = styled.div`
  color: ${theme.colors.textSecondary};
  font-size: 10px;
  margin-top: 2px;
  font-weight: 500;
`;

const MatchActions = styled.div`
  display: flex;
  align-items: center;
  gap: ${theme.spacing.sm};
`;

const StarButton = styled.button.withConfig({
  shouldForwardProp: (prop) => prop !== "starred",
})<{ starred?: boolean }>`
  background: transparent;
  border: 2px solid transparent;
  color: ${(props) =>
    props.starred ? theme.colors.yellow : theme.colors.textTertiary};
  font-size: 18px;
  cursor: pointer;
  padding: ${theme.spacing.sm};
  border-radius: ${theme.borderRadius.lg};
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;

  &::before {
    content: "";
    position: absolute;
    top: 50%;
    left: 50%;
    width: 0;
    height: 0;
    background: radial-gradient(
      circle,
      ${theme.colors.yellow}20 0%,
      transparent 70%
    );
    transition: all 0.3s ease;
    transform: translate(-50%, -50%);
    border-radius: 50%;
  }

  &::after {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(
      45deg,
      transparent 40%,
      rgba(255, 215, 0, 0.2) 50%,
      transparent 60%
    );
    opacity: 0;
    transition: all 0.3s ease;
    animation: ${sparkleMove} 2s ease-in-out infinite;
  }

  &:hover {
    color: ${theme.colors.yellow};
    border-color: ${theme.colors.yellow}30;
    background: ${theme.colors.yellow}10;
    transform: scale(1.2)
      rotate(${(props) => (props.starred ? "0deg" : "18deg")});
    box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);

    &::before {
      width: 40px;
      height: 40px;
    }

    &::after {
      opacity: ${(props) => (props.starred ? "1" : "0.7")};
    }
  }

  &:active {
    transform: scale(1.4) rotate(36deg);
    transition: transform 0.1s ease;
  }

  ${(props) =>
    props.starred &&
    css`
      color: ${theme.colors.yellow};
      text-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
      animation: ${starGlow} 2s ease-in-out infinite;

      &::after {
        opacity: 1;
      }
    `}
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

const Matches: React.FC<MatchesProps> = ({ season = "2024-25", team }) => {
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
        <LoadingSpinner
          text="Loading Premier League matches..."
          showProgress={true}
        />
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
          <LoadingSpinner text={`No matches found for Round ${currentRound}`} />
        ) : (
          matches.map((match, index) => (
            <MatchItem
              key={match.id}
              onClick={() => navigate(`/match/${match.id}`)}
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <MatchTime>
                <TimeText>{formatTime(match.date)}</TimeText>
                <StatusText>FT</StatusText>
              </MatchTime>

              <MatchContent>
                <TeamsContainer>
                  <TeamRow>
                    <TeamLogo className="team-logo">
                      {getTeamShortName(match.home_team)}
                    </TeamLogo>
                    <TeamName>{match.home_team}</TeamName>
                  </TeamRow>
                  <TeamRow>
                    <TeamLogo className="team-logo">
                      {getTeamShortName(match.away_team)}
                    </TeamLogo>
                    <TeamName>{match.away_team}</TeamName>
                  </TeamRow>
                </TeamsContainer>

                <ScoreContainer className="score-container">
                  <Score>
                    <GoalCount>{match.fthg}</GoalCount>
                    <ScoreSeparator>-</ScoreSeparator>
                    <GoalCount>{match.ftag}</GoalCount>
                  </Score>
                  <MatchStatus>{getMatchStatus(match)}</MatchStatus>
                </ScoreContainer>
              </MatchContent>

              <MatchActions>
                <StarButton className="star-button" starred={false}>
                  ☆
                </StarButton>
              </MatchActions>
            </MatchItem>
          ))
        )}
      </MatchesList>
    </MatchesContainer>
  );
};

export default Matches;
