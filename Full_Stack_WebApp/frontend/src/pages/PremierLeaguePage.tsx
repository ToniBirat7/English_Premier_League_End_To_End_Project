import React, { useState } from "react";
import styled from "styled-components";
import { theme, Card, Text, Flex, Button } from "../styles/GlobalStyles";
import LeagueTable from "../components/LeagueTable";
import Matches from "../components/Matches";
import SeasonSelector from "../components/SeasonSelector";

const PremierLeagueContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: ${theme.spacing.lg};
`;

const PageHeader = styled.div`
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  padding: ${theme.spacing.xl};
  border-radius: ${theme.borderRadius.lg};
  color: white;
  margin-bottom: ${theme.spacing.lg};
`;

const HeaderContent = styled.div`
  display: flex;
  align-items: center;
  gap: ${theme.spacing.lg};
`;

const LeagueLogo = styled.div`
  width: 80px;
  height: 80px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: ${theme.borderRadius.lg};
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 40px;
`;

const HeaderInfo = styled.div`
  flex: 1;
`;

const LeagueTitle = styled.h1`
  font-size: 32px;
  font-weight: bold;
  margin: 0 0 ${theme.spacing.sm} 0;
`;

const LeagueSubtitle = styled.p`
  font-size: 16px;
  opacity: 0.9;
  margin: 0 0 ${theme.spacing.md} 0;
`;

const SeasonInfo = styled.div`
  display: flex;
  align-items: center;
  gap: ${theme.spacing.lg};
  font-size: 14px;
`;

const InfoItem = styled.div`
  display: flex;
  align-items: center;
  gap: ${theme.spacing.sm};
`;

const HeaderControls = styled.div`
  display: flex;
  align-items: center;
  gap: ${theme.spacing.md};
  margin-top: ${theme.spacing.md};
`;

const TabsContainer = styled.div`
  display: flex;
  gap: ${theme.spacing.md};
  margin-bottom: ${theme.spacing.lg};
`;

const Tab = styled.button.withConfig({
  shouldForwardProp: (prop) => prop !== "active",
})<{ active?: boolean }>`
  padding: ${theme.spacing.md} ${theme.spacing.lg};
  background: ${(props) =>
    props.active ? theme.colors.purple : theme.colors.secondary};
  border: 1px solid
    ${(props) => (props.active ? theme.colors.purple : theme.colors.border)};
  border-radius: ${theme.borderRadius.lg};
  color: ${(props) => (props.active ? "white" : theme.colors.textPrimary)};
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;

  &:hover {
    background: ${(props) =>
      props.active ? theme.colors.purpleDark : theme.colors.tertiary};
  }
`;

const ContentContainer = styled.div`
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

const StatsCard = styled(Card)`
  padding: ${theme.spacing.lg};
`;

const StatsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: ${theme.spacing.lg};
`;

const StatItem = styled.div`
  text-align: center;
`;

const StatValue = styled.div`
  font-size: 24px;
  font-weight: bold;
  color: ${theme.colors.textPrimary};
  margin-bottom: ${theme.spacing.xs};
`;

const StatLabel = styled.div`
  font-size: 12px;
  color: ${theme.colors.textSecondary};
  text-transform: uppercase;
  letter-spacing: 0.5px;
`;

const NewsCard = styled(Card)`
  padding: ${theme.spacing.lg};
`;

const NewsTitle = styled.h3`
  font-size: 16px;
  font-weight: bold;
  color: ${theme.colors.textPrimary};
  margin: 0 0 ${theme.spacing.md} 0;
`;

const NewsItem = styled.div`
  padding: ${theme.spacing.md} 0;
  border-bottom: 1px solid ${theme.colors.border};

  &:last-child {
    border-bottom: none;
  }
`;

const NewsHeadline = styled.h4`
  font-size: 14px;
  font-weight: 500;
  color: ${theme.colors.textPrimary};
  margin: 0 0 ${theme.spacing.xs} 0;
  line-height: 1.4;
`;

const NewsTime = styled.p`
  font-size: 12px;
  color: ${theme.colors.textSecondary};
  margin: 0;
`;

const PlayerCard = styled(Card)`
  padding: ${theme.spacing.lg};
`;

const PlayerTitle = styled.h3`
  font-size: 16px;
  font-weight: bold;
  color: ${theme.colors.textPrimary};
  margin: 0 0 ${theme.spacing.md} 0;
  display: flex;
  align-items: center;
  gap: ${theme.spacing.sm};
`;

const PlayerItem = styled.div`
  display: flex;
  align-items: center;
  gap: ${theme.spacing.md};
  padding: ${theme.spacing.md} 0;
  border-bottom: 1px solid ${theme.colors.border};

  &:last-child {
    border-bottom: none;
  }
`;

const PlayerAvatar = styled.div`
  width: 40px;
  height: 40px;
  background: ${theme.colors.tertiary};
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
`;

const PlayerInfo = styled.div`
  flex: 1;
`;

const PlayerName = styled.div`
  font-size: 14px;
  font-weight: 500;
  color: ${theme.colors.textPrimary};
`;

const PlayerTeam = styled.div`
  font-size: 12px;
  color: ${theme.colors.textSecondary};
`;

const PlayerRating = styled.div`
  background: ${theme.colors.green};
  color: white;
  padding: 2px 8px;
  border-radius: ${theme.borderRadius.sm};
  font-size: 12px;
  font-weight: bold;
`;

interface PremierLeaguePageProps {}

const PremierLeaguePage: React.FC<PremierLeaguePageProps> = () => {
  const [activeTab, setActiveTab] = useState("Standings");
  const [selectedSeason, setSelectedSeason] = useState("2024-25");

  const tabs = ["Standings", "Fixtures", "Statistics", "Commentary", "Teams"];

  const newsItems = [
    {
      headline: "Manchester City secure dramatic victory over Arsenal",
      time: "2 hours ago",
    },
    {
      headline: "Liverpool maintain perfect start with 3-1 win",
      time: "4 hours ago",
    },
    {
      headline: "Chelsea sign new striker in £80m deal",
      time: "6 hours ago",
    },
    {
      headline: "Tottenham manager speaks ahead of big match",
      time: "8 hours ago",
    },
  ];

  const topPlayers = [
    {
      name: "Mohamed Salah",
      team: "Liverpool",
      rating: "7.78",
      avatar: "👤",
    },
    {
      name: "Erling Haaland",
      team: "Man City",
      rating: "7.65",
      avatar: "👤",
    },
    {
      name: "Bruno Fernandes",
      team: "Man United",
      rating: "7.42",
      avatar: "👤",
    },
    {
      name: "Kevin De Bruyne",
      team: "Man City",
      rating: "7.38",
      avatar: "👤",
    },
  ];

  return (
    <PremierLeagueContainer>
      <PageHeader>
        <HeaderContent>
          <LeagueLogo>🏴󠁧󠁢󠁥󠁮󠁧󠁿</LeagueLogo>
          <HeaderInfo>
            <LeagueTitle>Premier League {selectedSeason}</LeagueTitle>
            <LeagueSubtitle>🇬🇧 England • 16 Aug • 25 May</LeagueSubtitle>
            <SeasonInfo>
              <InfoItem>
                <span>⚽</span>
                <span>380 matches</span>
              </InfoItem>
              <InfoItem>
                <span>👥</span>
                <span>20 teams</span>
              </InfoItem>
              <InfoItem>
                <span>🏆</span>
                <span>Matchweek 38</span>
              </InfoItem>
            </SeasonInfo>
            <HeaderControls>
              <SeasonSelector
                selectedSeason={selectedSeason}
                onSeasonChange={setSelectedSeason}
              />
            </HeaderControls>
          </HeaderInfo>
        </HeaderContent>
      </PageHeader>

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

      <ContentContainer>
        <MainContent>
          {activeTab === "Standings" && <LeagueTable season={selectedSeason} />}
          {activeTab === "Fixtures" && <Matches season={selectedSeason} />}
          {activeTab === "Statistics" && (
            <StatsCard>
              <Text
                size="lg"
                weight="bold"
                style={{ marginBottom: theme.spacing.lg }}
              >
                League Statistics
              </Text>
              <StatsGrid>
                <StatItem>
                  <StatValue>2,280</StatValue>
                  <StatLabel>Total Matches</StatLabel>
                </StatItem>
                <StatItem>
                  <StatValue>6,141</StatValue>
                  <StatLabel>Total Goals</StatLabel>
                </StatItem>
                <StatItem>
                  <StatValue>2.69</StatValue>
                  <StatLabel>Goals per Match</StatLabel>
                </StatItem>
                <StatItem>
                  <StatValue>47%</StatValue>
                  <StatLabel>Home Wins</StatLabel>
                </StatItem>
              </StatsGrid>
            </StatsCard>
          )}
          {activeTab === "Commentary" && (
            <Card style={{ padding: theme.spacing.lg, textAlign: "center" }}>
              <Text color="secondary">
                Live commentary will appear here during matches
              </Text>
            </Card>
          )}
          {activeTab === "Teams" && (
            <Card style={{ padding: theme.spacing.lg, textAlign: "center" }}>
              <Text color="secondary">Team profiles coming soon...</Text>
            </Card>
          )}
        </MainContent>

        <SideContent>
          <PlayerCard>
            <PlayerTitle>🏆 Player of the Season</PlayerTitle>
            <Text
              size="sm"
              color="secondary"
              style={{ marginBottom: theme.spacing.md }}
            >
              See player stats
            </Text>
            {topPlayers.map((player, index) => (
              <PlayerItem key={player.name}>
                <Text
                  size="sm"
                  weight="bold"
                  color="secondary"
                  style={{ minWidth: "20px" }}
                >
                  {index + 1}
                </Text>
                <PlayerAvatar>{player.avatar}</PlayerAvatar>
                <PlayerInfo>
                  <PlayerName>{player.name}</PlayerName>
                  <PlayerTeam>{player.team}</PlayerTeam>
                </PlayerInfo>
                <PlayerRating>{player.rating}</PlayerRating>
              </PlayerItem>
            ))}
          </PlayerCard>

          <NewsCard>
            <NewsTitle>Latest News</NewsTitle>
            {newsItems.map((item, index) => (
              <NewsItem key={index}>
                <NewsHeadline>{item.headline}</NewsHeadline>
                <NewsTime>{item.time}</NewsTime>
              </NewsItem>
            ))}
          </NewsCard>

          <StatsCard>
            <Text
              size="lg"
              weight="bold"
              style={{ marginBottom: theme.spacing.lg }}
            >
              Quick Stats
            </Text>
            <Flex direction="column" gap={theme.spacing.md}>
              <Flex justify="space-between">
                <Text color="secondary">Matches Played</Text>
                <Text weight="bold">380</Text>
              </Flex>
              <Flex justify="space-between">
                <Text color="secondary">Goals Scored</Text>
                <Text weight="bold">1,023</Text>
              </Flex>
              <Flex justify="space-between">
                <Text color="secondary">Yellow Cards</Text>
                <Text weight="bold">1,547</Text>
              </Flex>
              <Flex justify="space-between">
                <Text color="secondary">Red Cards</Text>
                <Text weight="bold">89</Text>
              </Flex>
            </Flex>
          </StatsCard>
        </SideContent>
      </ContentContainer>
    </PremierLeagueContainer>
  );
};

export default PremierLeaguePage;
