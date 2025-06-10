import React from "react";
import styled from "styled-components";
import { Link } from "react-router-dom";
import { theme, Card, Text, Flex, Grid, Button } from "../styles/GlobalStyles";
import Matches from "../components/Matches";

const HomeContainer = styled.div`
  display: grid;
  grid-template-columns: 8fr 4fr; /* 8-column main, 4-column sidebar for 12-column system */
  gap: ${theme.spacing.xl};

  @media (max-width: ${theme.breakpoints.desktop}) {
    gap: ${theme.spacing.lg};
  }

  @media (max-width: ${theme.breakpoints.tablet}) {
    grid-template-columns: 1fr;
    gap: ${theme.spacing.md};
  }
`;

const MainColumn = styled.div`
  display: flex;
  flex-direction: column;
  gap: ${theme.spacing.lg};
`;

const SideColumn = styled.div`
  display: flex;
  flex-direction: column;
  gap: ${theme.spacing.lg};
`;

const WelcomeCard = styled(Card)`
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  color: white;
  padding: ${theme.spacing.xl};
`;

const WelcomeTitle = styled.h1`
  font-size: 28px;
  font-weight: bold;
  margin: 0 0 ${theme.spacing.sm} 0;
`;

const WelcomeSubtitle = styled.p`
  font-size: 16px;
  opacity: 0.9;
  margin: 0 0 ${theme.spacing.lg} 0;
`;

const FeaturedSection = styled(Card)`
  padding: ${theme.spacing.lg};
`;

const SectionTitle = styled.h2`
  font-size: 20px;
  font-weight: bold;
  color: ${theme.colors.textPrimary};
  margin: 0 0 ${theme.spacing.md} 0;
  display: flex;
  align-items: center;
  gap: ${theme.spacing.sm};
`;

const SectionIcon = styled.span`
  font-size: 24px;
`;

const CompetitionGrid = styled(Grid)`
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: ${theme.spacing.md};
`;

const CompetitionCard = styled(Link)`
  display: block;
  padding: ${theme.spacing.lg};
  background: ${theme.colors.secondary};
  border: 1px solid ${theme.colors.border};
  border-radius: ${theme.borderRadius.lg};
  text-decoration: none;
  transition: all 0.2s ease;

  &:hover {
    background: ${theme.colors.tertiary};
    border-color: ${theme.colors.purple};
    transform: translateY(-2px);
  }
`;

const CompetitionHeader = styled.div`
  display: flex;
  align-items: center;
  gap: ${theme.spacing.md};
  margin-bottom: ${theme.spacing.md};
`;

const CompetitionLogo = styled.div`
  width: 40px;
  height: 40px;
  background: ${theme.colors.purple};
  border-radius: ${theme.borderRadius.md};
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
`;

const CompetitionInfo = styled.div`
  flex: 1;
`;

const CompetitionName = styled.h3`
  font-size: 16px;
  font-weight: bold;
  color: ${theme.colors.textPrimary};
  margin: 0;
`;

const CompetitionCountry = styled.p`
  font-size: 12px;
  color: ${theme.colors.textSecondary};
  margin: 2px 0 0 0;
`;

const CompetitionStats = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: ${theme.spacing.md};
`;

const StatItem = styled.div`
  text-align: center;
`;

const StatValue = styled.div`
  font-size: 18px;
  font-weight: bold;
  color: ${theme.colors.textPrimary};
`;

const StatLabel = styled.div`
  font-size: 10px;
  color: ${theme.colors.textSecondary};
  text-transform: uppercase;
`;

const LiveCard = styled(Card)`
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
  padding: ${theme.spacing.lg};
`;

const LiveTitle = styled.h3`
  font-size: 16px;
  font-weight: bold;
  margin: 0 0 ${theme.spacing.sm} 0;
  display: flex;
  align-items: center;
  gap: ${theme.spacing.sm};
`;

const LiveDot = styled.div`
  width: 8px;
  height: 8px;
  background: #22c55e;
  border-radius: 50%;
  animation: pulse 2s infinite;

  @keyframes pulse {
    0% {
      opacity: 1;
    }
    50% {
      opacity: 0.5;
    }
    100% {
      opacity: 1;
    }
  }
`;

const ChallengeCard = styled(Card)`
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  color: white;
  padding: ${theme.spacing.lg};
`;

const ChallengeTitle = styled.h3`
  font-size: 16px;
  font-weight: bold;
  margin: 0 0 ${theme.spacing.sm} 0;
  display: flex;
  align-items: center;
  gap: ${theme.spacing.sm};
`;

const ChallengeTimer = styled.div`
  display: flex;
  gap: ${theme.spacing.md};
  margin: ${theme.spacing.md} 0;
`;

const TimerItem = styled.div`
  text-align: center;
  flex: 1;
`;

const TimerValue = styled.div`
  font-size: 24px;
  font-weight: bold;
`;

const TimerLabel = styled.div`
  font-size: 10px;
  opacity: 0.8;
`;

const HomePage: React.FC = () => {
  const competitions = [
    {
      name: "Premier League",
      country: "England",
      logo: "🏴󠁧󠁢󠁥󠁮󠁧󠁿",
      path: "/premier-league",
      teams: 20,
      matches: 380,
      season: "2024/25",
    },
  ];

  return (
    <HomeContainer>
      <MainColumn>
        <WelcomeCard>
          <WelcomeTitle>Premier League Hub</WelcomeTitle>
          <WelcomeSubtitle>
            Your ultimate destination for Premier League scores, fixtures, and
            standings
          </WelcomeSubtitle>
          <Text size="sm" style={{ opacity: 0.8 }}>
            16 Aug • 25 May • England's Premier Football Competition
          </Text>
        </WelcomeCard>

        <FeaturedSection>
          <SectionTitle>
            <SectionIcon>🏆</SectionIcon>
            Top competitions
          </SectionTitle>
          <CompetitionGrid>
            {competitions.map((competition) => (
              <CompetitionCard key={competition.path} to={competition.path}>
                <CompetitionHeader>
                  <CompetitionLogo>{competition.logo}</CompetitionLogo>
                  <CompetitionInfo>
                    <CompetitionName>{competition.name}</CompetitionName>
                    <CompetitionCountry>
                      {competition.country} • {competition.season}
                    </CompetitionCountry>
                  </CompetitionInfo>
                </CompetitionHeader>
                <CompetitionStats>
                  <StatItem>
                    <StatValue>{competition.teams}</StatValue>
                    <StatLabel>Teams</StatLabel>
                  </StatItem>
                  <StatItem>
                    <StatValue>{competition.matches}</StatValue>
                    <StatLabel>Matches</StatLabel>
                  </StatItem>
                </CompetitionStats>
              </CompetitionCard>
            ))}
          </CompetitionGrid>
        </FeaturedSection>

        <Matches />
      </MainColumn>

      <SideColumn>
        <LiveCard>
          <LiveTitle>
            <LiveDot />
            Live matches
          </LiveTitle>
          <Text size="sm">No live matches at the moment</Text>
        </LiveCard>

        <ChallengeCard>
          <ChallengeTitle>🏆 Weekly Challenge</ChallengeTitle>
          <Text size="sm" style={{ opacity: 0.9 }}>
            Time left: 6d 1h
          </Text>
          <ChallengeTimer>
            <TimerItem>
              <TimerValue>6</TimerValue>
              <TimerLabel>Days</TimerLabel>
            </TimerItem>
            <TimerItem>
              <TimerValue>21</TimerValue>
              <TimerLabel>Hours</TimerLabel>
            </TimerItem>
            <TimerItem>
              <TimerValue>7</TimerValue>
              <TimerLabel>Minutes</TimerLabel>
            </TimerItem>
            <TimerItem>
              <TimerValue>30</TimerValue>
              <TimerLabel>Seconds</TimerLabel>
            </TimerItem>
          </ChallengeTimer>
        </ChallengeCard>

        <Card>
          <SectionTitle>
            <SectionIcon>⭐</SectionIcon>
            Top teams
          </SectionTitle>
          <Text size="sm" color="secondary">
            Average SofaScore Rating
          </Text>
          <Flex
            direction="column"
            gap={theme.spacing.md}
            style={{ marginTop: theme.spacing.md }}
          >
            {[
              { name: "Manchester City", rating: "7.13", logo: "🏙️" },
              { name: "Liverpool", rating: "7.07", logo: "🔴" },
              { name: "Arsenal", rating: "7.05", logo: "🔴" },
              { name: "Chelsea", rating: "7.01", logo: "🔵" },
              { name: "Brentford", rating: "6.99", logo: "🐝" },
            ].map((team, index) => (
              <Flex key={team.name} justify="space-between" align="center">
                <Flex align="center" gap={theme.spacing.sm}>
                  <Text size="lg">{team.logo}</Text>
                  <Text weight="medium">{team.name}</Text>
                </Flex>
                <Text color="green" weight="bold">
                  {team.rating}
                </Text>
              </Flex>
            ))}
          </Flex>
        </Card>
      </SideColumn>
    </HomeContainer>
  );
};

export default HomePage;
