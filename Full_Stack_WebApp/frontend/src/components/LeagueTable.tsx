import React, { useState, useEffect } from "react";
import styled, { keyframes, css } from "styled-components";
import { teamsApi, StandingsTeam } from "../services/api";
import { theme, Card, Text } from "../styles/GlobalStyles";

// Define keyframes outside of styled components
const underlineAnimation = keyframes`
  0% { transform: scaleX(0); }
  100% { transform: scaleX(1); }
`;

const slideInAnimation = keyframes`
  0% {
    opacity: 0;
    transform: translateY(20px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
`;

const StandingsContainer = styled(Card)`
  background: ${theme.colors.secondary};
  padding: 0;
  overflow: hidden;
`;

const StandingsHeader = styled.div`
  padding: ${theme.spacing.lg};
  border-bottom: 1px solid ${theme.colors.border};
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
`;

const StandingsTitle = styled.div`
  display: flex;
  align-items: center;
  gap: ${theme.spacing.md};
  color: white;
`;

const LeagueLogo = styled.div`
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: ${theme.borderRadius.md};
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
`;

const TitleText = styled.div`
  display: flex;
  flex-direction: column;
`;

const LeagueName = styled.h2`
  font-size: 20px;
  font-weight: bold;
  margin: 0;
`;

const SeasonInfo = styled.span`
  font-size: 14px;
  opacity: 0.9;
  display: flex;
  align-items: center;
  gap: ${theme.spacing.sm};
`;

const TabsContainer = styled.div`
  display: flex;
  padding: 0 ${theme.spacing.lg};
  background: ${theme.colors.secondary};
  border-bottom: 1px solid ${theme.colors.border};
`;

const Tab = styled.button.withConfig({
  shouldForwardProp: (prop) => prop !== "active",
})<{ active?: boolean }>`
  padding: ${theme.spacing.md} ${theme.spacing.lg};
  background: transparent;
  border: none;
  color: ${(props) =>
    props.active ? theme.colors.purple : theme.colors.textSecondary};
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  position: relative;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);

  &::before {
    content: "";
    position: absolute;
    top: 0;
    left: 50%;
    width: 0;
    height: 100%;
    background: rgba(139, 92, 246, 0.1);
    transition: all 0.3s ease;
    transform: translateX(-50%);
  }

  &:hover {
    color: ${theme.colors.textPrimary};
    transform: translateY(-1px);

    &::before {
      width: 100%;
    }
  }

  ${(props) =>
    props.active &&
    css`
      color: ${theme.colors.purple};

      &::before {
        width: 100%;
        background: rgba(139, 92, 246, 0.15);
      }

      &::after {
        content: "";
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(
          90deg,
          ${theme.colors.purple},
          ${theme.colors.blue}
        );
        animation: ${underlineAnimation} 0.3s ease-out;
      }
    `}
`;

const TableContainer = styled.div`
  overflow-x: auto;
`;

const Table = styled.table`
  width: 100%;
  border-collapse: collapse;
`;

const TableHeader = styled.thead`
  background: ${theme.colors.tertiary};
`;

const HeaderRow = styled.tr``;

const HeaderCell = styled.th<{ align?: "left" | "center" | "right" }>`
  padding: ${theme.spacing.md} ${theme.spacing.sm};
  text-align: ${(props) => props.align || "left"};
  font-size: 12px;
  font-weight: 600;
  color: ${theme.colors.textSecondary};
  text-transform: uppercase;
  letter-spacing: 0.5px;
  white-space: nowrap;

  &:first-child {
    padding-left: ${theme.spacing.lg};
  }

  &:last-child {
    padding-right: ${theme.spacing.lg};
  }
`;

const TableBody = styled.tbody``;

const TableRow = styled.tr<{ position?: number }>`
  border-bottom: 1px solid ${theme.colors.border};
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;

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

  &:hover {
    background: ${theme.colors.tertiary}30;
    transform: translateX(4px);
    box-shadow: 0 2px 8px rgba(139, 92, 246, 0.1);

    &::before {
      left: 100%;
    }
  }

  /* Staggered animation */
  animation: ${slideInAnimation} 0.5s ease-out both;

  ${(props) => {
    const delay = props.position ? (props.position - 1) * 0.05 : 0;
    return `animation-delay: ${delay}s;`;
  }}

  ${(props) => {
    if (props.position && props.position <= 4) {
      return `
        border-left: 3px solid ${theme.colors.green};
        
        &:hover {
          border-left-color: ${theme.colors.green};
          border-left-width: 4px;
        }
      `;
    } else if (props.position && props.position <= 6) {
      return `
        border-left: 3px solid ${theme.colors.yellow};
        
        &:hover {
          border-left-color: ${theme.colors.yellow};
          border-left-width: 4px;
        }
      `;
    } else if (props.position && props.position >= 18) {
      return `
        border-left: 3px solid ${theme.colors.red};
        
        &:hover {
          border-left-color: ${theme.colors.red};
          border-left-width: 4px;
        }
      `;
    }
    return "";
  }}
`;

const TableCell = styled.td<{ align?: "left" | "center" | "right" }>`
  padding: ${theme.spacing.md} ${theme.spacing.sm};
  text-align: ${(props) => props.align || "left"};
  font-size: 14px;

  &:first-child {
    padding-left: ${theme.spacing.lg};
  }

  &:last-child {
    padding-right: ${theme.spacing.lg};
  }
`;

const PositionCell = styled(TableCell)`
  width: 40px;
  font-weight: bold;
  color: ${theme.colors.textSecondary};
`;

const TeamCell = styled(TableCell)`
  min-width: 200px;
`;

const TeamInfo = styled.div`
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
  border-radius: ${theme.borderRadius.sm};
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
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
      rgba(139, 92, 246, 0.3) 0%,
      transparent 70%
    );
    transition: all 0.3s ease;
    transform: translate(-50%, -50%);
    border-radius: 50%;
  }

  &:hover {
    transform: scale(1.1) rotate(5deg);
    background: linear-gradient(
      135deg,
      rgba(139, 92, 246, 0.1) 0%,
      ${theme.colors.tertiary} 100%
    );
    box-shadow: 0 2px 8px rgba(139, 92, 246, 0.2);

    &::before {
      width: 40px;
      height: 40px;
    }
  }
`;

const TeamName = styled.span`
  font-weight: 500;
  color: ${theme.colors.textPrimary};
`;

const StatCell = styled(TableCell)`
  width: 50px;
  font-weight: 500;
  color: ${theme.colors.textPrimary};
`;

const FormContainer = styled.div`
  display: flex;
  gap: 2px;
`;

const FormResult = styled.div<{ result: "W" | "D" | "L" }>`
  width: 16px;
  height: 16px;
  border-radius: 2px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  font-weight: bold;
  color: white;

  ${(props) => {
    switch (props.result) {
      case "W":
        return `background: ${theme.colors.green};`;
      case "D":
        return `background: ${theme.colors.yellow};`;
      case "L":
        return `background: ${theme.colors.red};`;
      default:
        return `background: ${theme.colors.textTertiary};`;
    }
  }}
`;

const LoadingContainer = styled.div`
  padding: ${theme.spacing.xxl};
  text-align: center;
  color: ${theme.colors.textSecondary};
`;

interface LeagueTableProps {
  season?: string;
}

const LeagueTable: React.FC<LeagueTableProps> = ({ season = "2024-25" }) => {
  const [standings, setStandings] = useState<StandingsTeam[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState("ALL");

  useEffect(() => {
    const fetchStandings = async () => {
      try {
        setLoading(true);
        const data = await teamsApi.getStandings(season);
        setStandings(data);
      } catch (error) {
        console.error("Error fetching standings:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchStandings();
  }, [season]);

  // Mock form data - you can enhance this with actual recent matches
  const getTeamForm = (teamName: string): ("W" | "D" | "L")[] => {
    const forms: { [key: string]: ("W" | "D" | "L")[] } = {
      Liverpool: ["W", "L", "D", "L", "D"],
      Arsenal: ["D", "L", "D", "W", "W"],
      "Man City": ["W", "W", "D", "W", "W"],
      Chelsea: ["W", "W", "L", "W", "W"],
    };
    return forms[teamName] || ["W", "D", "L", "W", "D"];
  };

  if (loading) {
    return (
      <StandingsContainer>
        <LoadingContainer>Loading standings...</LoadingContainer>
      </StandingsContainer>
    );
  }

  return (
    <StandingsContainer>
      <StandingsHeader>
        <StandingsTitle>
          <LeagueLogo>🏴󠁧󠁢󠁥󠁮󠁧󠁿</LeagueLogo>
          <TitleText>
            <LeagueName>Premier League {season}</LeagueName>
            <SeasonInfo>🇬🇧 England • 16 Aug • 25 May</SeasonInfo>
          </TitleText>
        </StandingsTitle>
      </StandingsHeader>

      <TabsContainer>
        <Tab active={activeTab === "ALL"} onClick={() => setActiveTab("ALL")}>
          ALL
        </Tab>
        <Tab active={activeTab === "HOME"} onClick={() => setActiveTab("HOME")}>
          HOME
        </Tab>
        <Tab active={activeTab === "AWAY"} onClick={() => setActiveTab("AWAY")}>
          AWAY
        </Tab>
      </TabsContainer>

      <TableContainer>
        <Table>
          <TableHeader>
            <HeaderRow>
              <HeaderCell>#</HeaderCell>
              <HeaderCell>Team</HeaderCell>
              <HeaderCell align="center">P</HeaderCell>
              <HeaderCell align="center">W</HeaderCell>
              <HeaderCell align="center">D</HeaderCell>
              <HeaderCell align="center">L</HeaderCell>
              <HeaderCell align="center">DIFF</HeaderCell>
              <HeaderCell align="center">Goals</HeaderCell>
              <HeaderCell align="center">Last 5</HeaderCell>
              <HeaderCell align="center">PTS</HeaderCell>
            </HeaderRow>
          </TableHeader>
          <TableBody>
            {standings.map((team) => (
              <TableRow key={team.id} position={team.position}>
                <PositionCell>{team.position}</PositionCell>
                <TeamCell>
                  <TeamInfo>
                    <TeamLogo>{team.short_name}</TeamLogo>
                    <TeamName>{team.name}</TeamName>
                  </TeamInfo>
                </TeamCell>
                <StatCell align="center">{team.matches_played}</StatCell>
                <StatCell align="center">{team.wins}</StatCell>
                <StatCell align="center">{team.draws}</StatCell>
                <StatCell align="center">{team.losses}</StatCell>
                <StatCell align="center">
                  <Text
                    color={
                      team.goal_difference > 0
                        ? "green"
                        : team.goal_difference < 0
                        ? "red"
                        : "secondary"
                    }
                  >
                    {team.goal_difference > 0 ? "+" : ""}
                    {team.goal_difference}
                  </Text>
                </StatCell>
                <StatCell align="center">
                  <Text size="sm" color="secondary">
                    {team.goals_for}-{team.goals_against}
                  </Text>
                </StatCell>
                <StatCell align="center">
                  <FormContainer>
                    {getTeamForm(team.name).map((result, index) => (
                      <FormResult key={index} result={result}>
                        {result}
                      </FormResult>
                    ))}
                  </FormContainer>
                </StatCell>
                <StatCell align="center">
                  <Text weight="bold">{team.points}</Text>
                </StatCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </StandingsContainer>
  );
};

export default LeagueTable;
