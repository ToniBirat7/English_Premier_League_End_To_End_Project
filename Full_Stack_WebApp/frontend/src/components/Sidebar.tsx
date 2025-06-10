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

const ShowMoreButton = styled.button`
  width: 100%;
  padding: ${theme.spacing.sm};
  background: transparent;
  border: none;
  color: ${theme.colors.purple};
  font-size: 14px;
  cursor: pointer;
  border-radius: ${theme.borderRadius.md};

  &:hover {
    background: ${theme.colors.secondary};
  }
`;

interface SidebarProps {}

const Sidebar: React.FC<SidebarProps> = () => {
  const location = useLocation();

  const isActive = (path: string) => {
    return location.pathname === path;
  };

  const competitions = [
    {
      name: "UEFA Champions League",
      path: "/champions-league",
      icon: "🏆",
      starred: true,
    },
    {
      name: "UEFA Europa League",
      path: "/europa-league",
      icon: "🥈",
      starred: true,
    },
    {
      name: "Premier League",
      path: "/premier-league",
      icon: "🏴󠁧󠁢󠁥󠁮󠁧󠁿",
      starred: true,
    },
    {
      name: "LaLiga",
      path: "/laliga",
      icon: "🇪🇸",
      starred: true,
    },
    {
      name: "Bundesliga",
      path: "/bundesliga",
      icon: "🇩🇪",
      starred: false,
    },
  ];

  return (
    <SidebarContainer>
      <SidebarContent>
        <Section>
          <SectionTitle>Top competitions</SectionTitle>
          <CompetitionList>
            {competitions.map((competition) => (
              <CompetitionItem
                key={competition.path}
                to={competition.path}
                active={isActive(competition.path)}
              >
                <CompetitionIcon>{competition.icon}</CompetitionIcon>
                {competition.name}
                <StarIcon starred={competition.starred}>
                  {competition.starred ? "⭐" : "☆"}
                </StarIcon>
              </CompetitionItem>
            ))}
            <ShowMoreButton>Show more ⌄</ShowMoreButton>
          </CompetitionList>
        </Section>
      </SidebarContent>
    </SidebarContainer>
  );
};

export default Sidebar;
