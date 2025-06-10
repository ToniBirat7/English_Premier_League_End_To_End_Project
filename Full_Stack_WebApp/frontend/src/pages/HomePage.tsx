import React from "react";
import styled, { keyframes } from "styled-components";
import { Link } from "react-router-dom";
import { theme, Card, Text, Flex, Grid, Button } from "../styles/GlobalStyles";
import Matches from "../components/Matches";

// Enhanced animations
const fadeInUp = keyframes`
  0% {
    opacity: 0;
    transform: translateY(30px) scale(0.95);
  }
  100% {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
`;

const slideInLeft = keyframes`
  0% {
    opacity: 0;
    transform: translateX(-30px) rotate(-2deg);
  }
  100% {
    opacity: 1;
    transform: translateX(0) rotate(0deg);
  }
`;

const slideInRight = keyframes`
  0% {
    opacity: 0;
    transform: translateX(30px) rotate(2deg);
  }
  100% {
    opacity: 1;
    transform: translateX(0) rotate(0deg);
  }
`;

const staggeredFadeIn = keyframes`
  0% {
    opacity: 0;
    transform: translateY(20px) scale(0.9);
  }
  100% {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
`;

const floatingAnimation = keyframes`
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-5px);
  }
`;

const sparkleAnimation = keyframes`
  0%, 100% {
    opacity: 0;
    transform: scale(0);
  }
  50% {
    opacity: 1;
    transform: scale(1);
  }
`;

const float = keyframes`
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-10px);
  }
`;

const diagonalMove = keyframes`
  0% { transform: translateX(-100%) translateY(-100%); }
  100% { transform: translateX(100%) translateY(100%); }
`;

const HomeContainer = styled.div`
  display: grid;
  grid-template-columns: 8fr 4fr;
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
  animation: ${slideInLeft} 0.8s ease-out;
`;

const SideColumn = styled.div`
  display: flex;
  flex-direction: column;
  gap: ${theme.spacing.lg};
  animation: ${slideInRight} 0.8s ease-out 0.2s both;
`;

const WelcomeCard = styled(Card)`
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  color: white;
  padding: ${theme.spacing.xl};
  position: relative;
  overflow: hidden;
  animation: ${fadeInUp} 0.6s ease-out;

  &::before {
    content: "";
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(
      circle,
      rgba(255, 255, 255, 0.1) 0%,
      transparent 70%
    );
    animation: ${floatingAnimation} 6s ease-in-out infinite;
    pointer-events: none;
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
      transparent 30%,
      rgba(255, 255, 255, 0.1) 50%,
      transparent 70%
    );
    animation: ${diagonalMove} 3s ease-in-out infinite;
    pointer-events: none;
  }

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 30px rgba(139, 92, 246, 0.3);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);

    &::before {
      animation-duration: 4s;
    }
  }
`;

const WelcomeTitle = styled.h1`
  font-size: 32px;
  font-weight: 800;
  margin: 0 0 ${theme.spacing.sm} 0;
  position: relative;
  z-index: 1;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
`;

const WelcomeSubtitle = styled.p`
  font-size: 18px;
  opacity: 0.95;
  margin: 0 0 ${theme.spacing.lg} 0;
  position: relative;
  z-index: 1;
  line-height: 1.6;
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

  > * {
    animation: ${staggeredFadeIn} 0.6s ease-out both;
  }

  > *:nth-child(1) {
    animation-delay: 0.1s;
  }
  > *:nth-child(2) {
    animation-delay: 0.2s;
  }
  > *:nth-child(3) {
    animation-delay: 0.3s;
  }
  > *:nth-child(4) {
    animation-delay: 0.4s;
  }
  > *:nth-child(5) {
    animation-delay: 0.5s;
  }
  > *:nth-child(6) {
    animation-delay: 0.6s;
  }
`;

const CompetitionCard = styled(Link)`
  display: block;
  padding: ${theme.spacing.lg};
  background: ${theme.colors.secondary};
  border: 1px solid ${theme.colors.border};
  border-radius: ${theme.borderRadius.lg};
  text-decoration: none;
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
      rgba(139, 92, 246, 0.1),
      transparent
    );
    transition: left 0.5s ease;
  }

  &::after {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(
      90deg,
      ${theme.colors.purple},
      ${theme.colors.blue}
    );
    transform: translateX(-100%);
    transition: transform 0.3s ease;
  }

  &:hover {
    background: ${theme.colors.tertiary};
    border-color: ${theme.colors.purple};
    transform: translateY(-4px) scale(1.02);
    box-shadow: 0 8px 25px rgba(139, 92, 246, 0.2);

    &::before {
      left: 100%;
    }

    &::after {
      transform: translateX(0);
    }

    .competition-logo {
      transform: scale(1.1) rotate(5deg);
    }

    .competition-stats {
      transform: translateY(-2px);
    }
  }

  &:active {
    transform: translateY(-2px) scale(1.01);
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
  background: linear-gradient(
    135deg,
    ${theme.colors.purple} 0%,
    ${theme.colors.blue} 100%
  );
  border-radius: ${theme.borderRadius.md};
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
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
      rgba(255, 255, 255, 0.3) 0%,
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
    box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4);

    &::before {
      width: 60px;
      height: 60px;
    }

    &::after {
      left: 100%;
    }
  }
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
            {competitions.map((competition, index) => (
              <CompetitionCard
                key={competition.path}
                to={competition.path}
                style={{ animationDelay: `${index * 0.1}s` }}
              >
                <CompetitionHeader>
                  <CompetitionLogo className="competition-logo">
                    {competition.logo}
                  </CompetitionLogo>
                  <CompetitionInfo>
                    <CompetitionName>{competition.name}</CompetitionName>
                    <CompetitionCountry>
                      {competition.country} • {competition.season}
                    </CompetitionCountry>
                  </CompetitionInfo>
                </CompetitionHeader>
                <CompetitionStats className="competition-stats">
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
