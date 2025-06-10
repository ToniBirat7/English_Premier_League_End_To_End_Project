import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import styled from "styled-components";
import { matchesApi, MatchDetails } from "../services/api";
import { theme, Card, Text, Flex } from "../styles/GlobalStyles";

const MatchDetailContainer = styled.div`
  display: grid;
  grid-template-columns: 1fr 380px;
  gap: ${theme.spacing.lg};

  @media (max-width: ${theme.breakpoints.tablet}) {
    grid-template-columns: 1fr;
  }
`;

const MainContent = styled.div`
  display: flex;
  flex-direction: column;
  gap: ${theme.spacing.lg};
`;

const SideContent = styled.div`
  display: flex;
  flex-direction: column;
  gap: ${theme.spacing.lg};
`;

const MatchHeader = styled(Card)`
  background: ${theme.colors.gradient.secondary};
  border: 1px solid ${theme.colors.border};
  padding: 0;
  overflow: hidden;
`;

const MatchInfo = styled.div`
  padding: ${theme.spacing.lg};
  text-align: center;
`;

const MatchDate = styled.div`
  color: ${theme.colors.textSecondary};
  font-size: 14px;
  margin-bottom: ${theme.spacing.sm};
`;

const TeamsContainer = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  gap: ${theme.spacing.xl};
  margin: ${theme.spacing.lg} 0;
`;

const TeamSection = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: ${theme.spacing.sm};
`;

const TeamLogo = styled.div`
  width: 60px;
  height: 60px;
  background: ${theme.colors.tertiary};
  border-radius: ${theme.borderRadius.lg};
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  font-weight: bold;
`;

const TeamName = styled.h2`
  font-size: 18px;
  font-weight: 600;
  color: ${theme.colors.textPrimary};
  margin: 0;
`;

const ScoreSection = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: ${theme.spacing.sm};
`;

const Score = styled.div`
  font-size: 36px;
  font-weight: bold;
  color: ${theme.colors.textPrimary};
`;

const MatchStatus = styled.div`
  color: ${theme.colors.textSecondary};
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
`;

const TabsContainer = styled.div`
  display: flex;
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
  transition: color 0.2s ease;

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

const StatisticsContainer = styled.div`
  padding: ${theme.spacing.lg};
`;

const StatItem = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: ${theme.spacing.md} 0;
  border-bottom: 1px solid ${theme.colors.border};

  &:last-child {
    border-bottom: none;
  }
`;

const StatLabel = styled.div`
  color: ${theme.colors.textSecondary};
  font-size: 14px;
  flex: 1;
  text-align: center;
`;

const StatValues = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
`;

const StatValue = styled.div`
  color: ${theme.colors.textPrimary};
  font-size: 16px;
  font-weight: 600;
  min-width: 60px;
  text-align: center;
`;

const StatBar = styled.div`
  flex: 1;
  height: 6px;
  background: ${theme.colors.tertiary};
  border-radius: 3px;
  margin: 0 ${theme.spacing.md};
  position: relative;
  overflow: hidden;
`;

const StatProgress = styled.div<{
  homeValue: number;
  awayValue: number;
  isHomeHigher: boolean;
}>`
  position: absolute;
  top: 0;
  height: 100%;
  background: ${(props) =>
    props.isHomeHigher ? theme.colors.green : theme.colors.blue};
  width: ${(props) => {
    const total = props.homeValue + props.awayValue;
    if (total === 0) return "50%";
    return props.isHomeHigher
      ? `${(props.homeValue / total) * 100}%`
      : `${100 - (props.homeValue / total) * 100}%`;
  }};
  left: ${(props) => (props.isHomeHigher ? "0" : "auto")};
  right: ${(props) => (!props.isHomeHigher ? "0" : "auto")};
  transition: width 0.3s ease;
`;

const LineupContainer = styled.div`
  background: linear-gradient(135deg, #2a3f2a 0%, #1a2f1a 100%);
  min-height: 400px;
  border-radius: ${theme.borderRadius.lg};
  position: relative;
  overflow: hidden;
  padding: ${theme.spacing.lg};
  display: flex;
  align-items: center;
  justify-content: center;
`;

const FormationContainer = styled.div`
  display: flex;
  justify-content: space-between;
  width: 100%;
  max-width: 800px;
`;

const TeamFormation = styled.div`
  display: flex;
  flex-direction: column;
  gap: ${theme.spacing.lg};
  width: 45%;
`;

const FormationText = styled.div`
  text-align: center;
  color: ${theme.colors.textPrimary};
  font-weight: 600;
  margin-bottom: ${theme.spacing.md};
`;

const LoadingContainer = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  padding: ${theme.spacing.xxl};
  color: ${theme.colors.textSecondary};
`;

interface MatchDetailPageProps {}

const MatchDetailPage: React.FC<MatchDetailPageProps> = () => {
  const { matchId } = useParams<{ matchId: string }>();
  const [matchDetails, setMatchDetails] = useState<MatchDetails | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState("Statistics");

  useEffect(() => {
    const fetchMatchDetails = async () => {
      if (!matchId) return;

      try {
        setLoading(true);
        const details = await matchesApi.getMatchDetails(parseInt(matchId));
        setMatchDetails(details);
      } catch (error) {
        console.error("Error fetching match details:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchMatchDetails();
  }, [matchId]);

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

  if (loading) {
    return <LoadingContainer>Loading match details...</LoadingContainer>;
  }

  if (!matchDetails) {
    return <LoadingContainer>Match not found</LoadingContainer>;
  }

  const { match, statistics } = matchDetails;

  const tabs = ["Statistics", "Lineups", "Player Stats"];

  return (
    <MatchDetailContainer>
      <MainContent>
        <MatchHeader>
          <MatchInfo>
            <MatchDate>
              {new Date(match.date).toLocaleDateString("en-GB", {
                weekday: "long",
                year: "numeric",
                month: "long",
                day: "numeric",
              })}{" "}
              • 20:45
            </MatchDate>

            <TeamsContainer>
              <TeamSection>
                <TeamLogo>{getTeamShortName(match.home_team_name)}</TeamLogo>
                <TeamName>{match.home_team_name}</TeamName>
              </TeamSection>

              <ScoreSection>
                <Score>
                  {match.fthg} - {match.ftag}
                </Score>
                <MatchStatus>Finished</MatchStatus>
              </ScoreSection>

              <TeamSection>
                <TeamLogo>{getTeamShortName(match.away_team_name)}</TeamLogo>
                <TeamName>{match.away_team_name}</TeamName>
              </TeamSection>
            </TeamsContainer>
          </MatchInfo>

          <TabsContainer>
            {tabs.map((tab) => (
              <Tab
                key={tab}
                active={activeTab === tab}
                onClick={() => setActiveTab(tab)}
              >
                {tab}
              </Tab>
            ))}
          </TabsContainer>
        </MatchHeader>

        {activeTab === "Statistics" && (
          <Card>
            <StatisticsContainer>
              <StatItem>
                <StatValues>
                  <StatValue>{statistics.possession.home}%</StatValue>
                  <StatLabel>Ball possession</StatLabel>
                  <StatValue>{statistics.possession.away}%</StatValue>
                </StatValues>
                <StatBar>
                  <StatProgress
                    homeValue={statistics.possession.home}
                    awayValue={statistics.possession.away}
                    isHomeHigher={
                      statistics.possession.home > statistics.possession.away
                    }
                  />
                </StatBar>
              </StatItem>

              <StatItem>
                <StatValues>
                  <StatValue>{statistics.shots.home}</StatValue>
                  <StatLabel>Total shots</StatLabel>
                  <StatValue>{statistics.shots.away}</StatValue>
                </StatValues>
                <StatBar>
                  <StatProgress
                    homeValue={statistics.shots.home}
                    awayValue={statistics.shots.away}
                    isHomeHigher={statistics.shots.home > statistics.shots.away}
                  />
                </StatBar>
              </StatItem>

              <StatItem>
                <StatValues>
                  <StatValue>{statistics.shots_on_target.home}</StatValue>
                  <StatLabel>Shots on target</StatLabel>
                  <StatValue>{statistics.shots_on_target.away}</StatValue>
                </StatValues>
                <StatBar>
                  <StatProgress
                    homeValue={statistics.shots_on_target.home}
                    awayValue={statistics.shots_on_target.away}
                    isHomeHigher={
                      statistics.shots_on_target.home >
                      statistics.shots_on_target.away
                    }
                  />
                </StatBar>
              </StatItem>

              <StatItem>
                <StatValues>
                  <StatValue>{statistics.corners.home}</StatValue>
                  <StatLabel>Corner kicks</StatLabel>
                  <StatValue>{statistics.corners.away}</StatValue>
                </StatValues>
                <StatBar>
                  <StatProgress
                    homeValue={statistics.corners.home}
                    awayValue={statistics.corners.away}
                    isHomeHigher={
                      statistics.corners.home > statistics.corners.away
                    }
                  />
                </StatBar>
              </StatItem>

              <StatItem>
                <StatValues>
                  <StatValue>{statistics.fouls.home}</StatValue>
                  <StatLabel>Fouls</StatLabel>
                  <StatValue>{statistics.fouls.away}</StatValue>
                </StatValues>
                <StatBar>
                  <StatProgress
                    homeValue={statistics.fouls.home}
                    awayValue={statistics.fouls.away}
                    isHomeHigher={statistics.fouls.home > statistics.fouls.away}
                  />
                </StatBar>
              </StatItem>

              <StatItem>
                <StatValues>
                  <StatValue>{statistics.yellow_cards.home}</StatValue>
                  <StatLabel>Yellow cards</StatLabel>
                  <StatValue>{statistics.yellow_cards.away}</StatValue>
                </StatValues>
                <StatBar>
                  <StatProgress
                    homeValue={statistics.yellow_cards.home}
                    awayValue={statistics.yellow_cards.away}
                    isHomeHigher={
                      statistics.yellow_cards.home >
                      statistics.yellow_cards.away
                    }
                  />
                </StatBar>
              </StatItem>
            </StatisticsContainer>
          </Card>
        )}

        {activeTab === "Lineups" && (
          <Card>
            <LineupContainer>
              <FormationContainer>
                <TeamFormation>
                  <FormationText>4-2-3-1</FormationText>
                  <Text color="secondary" style={{ textAlign: "center" }}>
                    {match.home_team_name}
                  </Text>
                </TeamFormation>

                <TeamFormation>
                  <FormationText>4-3-3</FormationText>
                  <Text color="secondary" style={{ textAlign: "center" }}>
                    {match.away_team_name}
                  </Text>
                </TeamFormation>
              </FormationContainer>
            </LineupContainer>
          </Card>
        )}

        {activeTab === "Player Stats" && (
          <Card style={{ padding: theme.spacing.lg, textAlign: "center" }}>
            <Text color="secondary">Player statistics coming soon...</Text>
          </Card>
        )}
      </MainContent>

      <SideContent>
        <Card>
          <Text
            size="lg"
            weight="bold"
            style={{ marginBottom: theme.spacing.md }}
          >
            Player of the match
          </Text>
          <Flex align="center" gap={theme.spacing.md}>
            <div
              style={{
                width: 48,
                height: 48,
                borderRadius: "50%",
                background: theme.colors.tertiary,
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
              }}
            >
              👤
            </div>
            <div>
              <Text weight="medium">Mohamed Salah</Text>
              <br />
              <Text size="sm" color="secondary">
                {match.home_team_name}
              </Text>
            </div>
            <div
              style={{
                marginLeft: "auto",
                background: theme.colors.green,
                color: "white",
                padding: "4px 8px",
                borderRadius: theme.borderRadius.sm,
                fontSize: "12px",
                fontWeight: "bold",
              }}
            >
              8.5
            </div>
          </Flex>
        </Card>
      </SideContent>
    </MatchDetailContainer>
  );
};

export default MatchDetailPage;
