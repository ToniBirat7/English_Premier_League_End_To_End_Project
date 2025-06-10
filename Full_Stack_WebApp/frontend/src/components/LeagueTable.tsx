import React, { useState, useEffect } from "react";
import styled from "styled-components";
import { teamsApi, StandingsTeam } from "../services/api";
import { theme, Card, Text, Flex } from "../styles/GlobalStyles";

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

const Tab = styled.button<{ active?: boolean }>`
  padding: ${theme.spacing.md} ${theme.spacing.lg};
  background: transparent;
  border: none;
  color: ${(props) =>
    props.active ? theme.colors.purple : theme.colors.textSecondary};
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  position: relative;

  &:hover {
    color: ${theme.colors.textPrimary};
  }

  ${(props) =>
    props.active &&
    `
    &::after {
      content: '';
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      height: 2px;
      background: ${theme.colors.purple};
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

  &:hover {
    background: ${theme.colors.tertiary}30;
  }

  ${(props) => {
    if (props.position && props.position <= 4) {
      return `border-left: 3px solid ${theme.colors.green};`;
    } else if (props.position && props.position <= 6) {
      return `border-left: 3px solid ${theme.colors.yellow};`;
    } else if (props.position && props.position >= 18) {
      return `border-left: 3px solid ${theme.colors.red};`;
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
  background: ${theme.colors.tertiary};
  border-radius: ${theme.borderRadius.sm};
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
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

const LeagueTable: React.FC<LeagueTableProps> = ({ season = "2023-24" }) => {
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
            <LeagueName>Premier League 2024/2025</LeagueName>
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
