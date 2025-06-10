import React, { useState, useEffect } from "react";
import styled from "styled-components";
import { teamsApi } from "../services/api";
import { theme } from "../styles/GlobalStyles";

const SelectorContainer = styled.div`
  position: relative;
  display: inline-block;
  z-index: 1000;
`;

const SelectorButton = styled.button<{ isOpen?: boolean }>`
  display: flex;
  align-items: center;
  gap: ${theme.spacing.sm};
  padding: ${theme.spacing.sm} ${theme.spacing.md};
  background: ${theme.colors.secondary};
  border: 1px solid
    ${(props) =>
      props.isOpen ? theme.colors.borderAccent : theme.colors.border};
  border-radius: ${theme.borderRadius.md};
  color: ${theme.colors.textPrimary};
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  min-width: 120px;
  justify-content: space-between;

  &:hover {
    background: ${theme.colors.tertiary};
    border-color: ${theme.colors.borderLight};
  }

  &:focus {
    outline: none;
  }
`;

const DropdownIcon = styled.span<{ isOpen?: boolean }>`
  font-size: 12px;
  transition: transform 0.2s ease;
  transform: ${(props) => (props.isOpen ? "rotate(180deg)" : "rotate(0deg)")};
`;

const DropdownMenu = styled.div<{ isOpen?: boolean }>`
  position: absolute;
  top: calc(100% + 4px);
  left: 0;
  right: 0;
  background: ${theme.colors.secondary};
  border: 1px solid ${theme.colors.border};
  border-radius: ${theme.borderRadius.md};
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
  z-index: 1001;
  overflow: hidden;
  opacity: ${(props) => (props.isOpen ? 1 : 0)};
  visibility: ${(props) => (props.isOpen ? "visible" : "hidden")};
  transform: ${(props) =>
    props.isOpen ? "translateY(0)" : "translateY(-8px)"};
  transition: all 0.2s ease;
  max-height: 200px;
  overflow-y: auto;
`;

const DropdownItem = styled.button<{ active?: boolean }>`
  width: 100%;
  padding: ${theme.spacing.sm} ${theme.spacing.md};
  background: ${(props) =>
    props.active ? theme.colors.purple : "transparent"};
  border: none;
  color: ${(props) => (props.active ? "white" : theme.colors.textPrimary)};
  font-size: 14px;
  text-align: left;
  cursor: pointer;
  transition: all 0.2s ease;

  &:hover {
    background: ${(props) =>
      props.active ? theme.colors.purpleDark : theme.colors.tertiary};
  }
`;

interface SeasonSelectorProps {
  selectedSeason: string;
  onSeasonChange: (season: string) => void;
}

const SeasonSelector: React.FC<SeasonSelectorProps> = ({
  selectedSeason,
  onSeasonChange,
}) => {
  const [seasons, setSeasons] = useState<string[]>([]);
  const [isOpen, setIsOpen] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSeasons = async () => {
      try {
        setLoading(true);
        const seasonsData = await teamsApi.getSeasons();
        setSeasons(seasonsData.reverse()); // Show latest seasons first
      } catch (error) {
        console.error("Error fetching seasons:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchSeasons();
  }, []);

  const handleSeasonSelect = (season: string) => {
    onSeasonChange(season);
    setIsOpen(false);
  };

  const formatSeasonDisplay = (season: string) => {
    return season.replace("-", "/");
  };

  if (loading) {
    return (
      <SelectorContainer>
        <SelectorButton disabled>
          Loading...
          <DropdownIcon>⌄</DropdownIcon>
        </SelectorButton>
      </SelectorContainer>
    );
  }

  return (
    <SelectorContainer>
      <SelectorButton isOpen={isOpen} onClick={() => setIsOpen(!isOpen)}>
        {formatSeasonDisplay(selectedSeason)}
        <DropdownIcon isOpen={isOpen}>⌄</DropdownIcon>
      </SelectorButton>

      <DropdownMenu isOpen={isOpen}>
        {seasons.map((season) => (
          <DropdownItem
            key={season}
            active={season === selectedSeason}
            onClick={() => handleSeasonSelect(season)}
          >
            {formatSeasonDisplay(season)}
          </DropdownItem>
        ))}
      </DropdownMenu>

      {isOpen && (
        <div
          style={{
            position: "fixed",
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            zIndex: 999,
            background: "transparent",
          }}
          onClick={() => setIsOpen(false)}
        />
      )}
    </SelectorContainer>
  );
};

export default SeasonSelector;
