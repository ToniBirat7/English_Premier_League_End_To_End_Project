import React from "react";
import styled from "styled-components";
import { Link, useLocation } from "react-router-dom";
import { theme } from "../styles/GlobalStyles";

const SidebarContainer = styled.aside`
  width: 280px;
  background: ${theme.colors.primary};
  border-right: 1px solid ${theme.colors.border};
  height: calc(100vh - 60px);
  overflow-y: auto;
  position: fixed;
  left: 0;
  top: 60px;

  /* Custom scrollbar styling */
  &::-webkit-scrollbar {
    width: 6px;
  }

  &::-webkit-scrollbar-track {
    background: ${theme.colors.secondary};
  }

  &::-webkit-scrollbar-thumb {
    background: ${theme.colors.border};
    border-radius: 3px;

    &:hover {
      background: ${theme.colors.textTertiary};
    }
  }

  /* Firefox scrollbar styling */
  scrollbar-width: thin;
  scrollbar-color: ${theme.colors.border} ${theme.colors.secondary};

  @media (max-width: ${theme.breakpoints.tablet}) {
    transform: translateX(-100%);
    transition: transform 0.3s ease;
    z-index: 1000;
  }
`;

const SidebarContent = styled.div`
  padding: ${theme.spacing.lg};
`;

const Section = styled.div`
  margin-bottom: ${theme.spacing.xl};
`;

const SectionTitle = styled.h3`
  color: ${theme.colors.textSecondary};
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: ${theme.spacing.md};
  padding: 0 ${theme.spacing.sm};
`;

const CompetitionList = styled.div`
  display: flex;
  flex-direction: column;
  gap: ${theme.spacing.xs};
`;

const CompetitionItem = styled(Link)<{ active?: boolean }>`
  display: flex;
  align-items: center;
  gap: ${theme.spacing.sm};
  padding: ${theme.spacing.sm};
  border-radius: ${theme.borderRadius.md};
  color: ${(props) =>
    props.active ? theme.colors.purple : theme.colors.textPrimary};
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  background: ${(props) =>
    props.active ? `${theme.colors.purple}15` : "transparent"};
  border: ${(props) =>
    props.active
      ? `1px solid ${theme.colors.purple}30`
      : "1px solid transparent"};

  &:hover {
    background: ${theme.colors.secondary};
    color: ${theme.colors.textPrimary};
  }
`;

const CompetitionIcon = styled.div`
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
`;

const StarIcon = styled.div<{ starred?: boolean }>`
  width: 16px;
  height: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-left: auto;
  color: ${(props) =>
    props.starred ? theme.colors.yellow : theme.colors.textTertiary};
  cursor: pointer;

  &:hover {
    color: ${theme.colors.yellow};
  }
`;

const Sidebar: React.FC = () => {
  const location = useLocation();

  const isActive = (path: string) => {
    return location.pathname === path;
  };

  const handleLinkClick = () => {
    // No mobile menu to close
  };

  const competitions = [
    {
      name: "Premier League",
      path: "/premier-league",
      icon: "🏴",
      starred: true,
    },
  ];

  return (
    <SidebarContainer>
      <SidebarContent>
        <Section>
          <SectionTitle>Football Competitions</SectionTitle>
          <CompetitionList>
            {competitions.map((competition) => (
              <CompetitionItem
                key={competition.path}
                to={competition.path}
                active={isActive(competition.path)}
                onClick={handleLinkClick}
              >
                <CompetitionIcon>{competition.icon}</CompetitionIcon>
                {competition.name}
                <StarIcon starred={competition.starred}>
                  {competition.starred ? "⭐" : "☆"}
                </StarIcon>
              </CompetitionItem>
            ))}
          </CompetitionList>
        </Section>

        <Section>
          <SectionTitle>Quick Stats</SectionTitle>
          <CompetitionList>
            <CompetitionItem to="/premier-league" onClick={handleLinkClick}>
              <CompetitionIcon>⚽</CompetitionIcon>
              380 Matches
            </CompetitionItem>
            <CompetitionItem to="/premier-league" onClick={handleLinkClick}>
              <CompetitionIcon>👥</CompetitionIcon>
              20 Teams
            </CompetitionItem>
            <CompetitionItem to="/premier-league" onClick={handleLinkClick}>
              <CompetitionIcon>🏆</CompetitionIcon>6 Seasons
            </CompetitionItem>
          </CompetitionList>
        </Section>
      </SidebarContent>
    </SidebarContainer>
  );
};

export default Sidebar;
