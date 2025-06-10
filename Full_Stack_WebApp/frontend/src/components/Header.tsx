import React from "react";
import styled from "styled-components";
import { Link, useLocation } from "react-router-dom";
import { theme } from "../styles/GlobalStyles";

const HeaderContainer = styled.header`
  background: ${theme.colors.primary};
  border-bottom: 1px solid ${theme.colors.border};
  position: sticky;
  top: 0;
  z-index: 1000;
`;

const HeaderContent = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 ${theme.spacing.lg};
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 60px;
`;

const Logo = styled(Link)`
  display: flex;
  align-items: center;
  gap: ${theme.spacing.sm};
  font-size: 24px;
  font-weight: bold;
  color: ${theme.colors.textPrimary};
  text-decoration: none;

  &:hover {
    color: ${theme.colors.purple};
  }
`;

const LogoIcon = styled.div`
  width: 32px;
  height: 32px;
  background: ${theme.colors.purple};
  border-radius: ${theme.borderRadius.sm};
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  font-size: 16px;
`;

const Navigation = styled.nav`
  display: flex;
  align-items: center;
  gap: ${theme.spacing.xl};
`;

const NavSection = styled.div`
  display: flex;
  align-items: center;
  gap: ${theme.spacing.lg};
`;

const NavItem = styled(Link)<{ active?: boolean }>`
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
  padding: ${theme.spacing.sm};
  color: ${(props) =>
    props.active ? theme.colors.purple : theme.colors.textSecondary};
  text-decoration: none;
  font-size: 12px;
  font-weight: 500;
  transition: color 0.2s ease;

  &:hover {
    color: ${theme.colors.purple};
  }
`;

const NavIcon = styled.div`
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
`;

const NavBadge = styled.span`
  background: ${theme.colors.red};
  color: white;
  font-size: 10px;
  padding: 2px 6px;
  border-radius: 10px;
  position: absolute;
  top: -5px;
  right: -5px;
  min-width: 16px;
  text-align: center;
`;

const SearchContainer = styled.div`
  position: relative;
  flex: 1;
  max-width: 400px;
  margin: 0 ${theme.spacing.xl};
`;

const SearchInput = styled.input`
  width: 100%;
  padding: ${theme.spacing.sm} ${theme.spacing.md};
  padding-left: 40px;
  background: ${theme.colors.secondary};
  border: 1px solid ${theme.colors.border};
  border-radius: ${theme.borderRadius.lg};
  color: ${theme.colors.textPrimary};
  font-size: 14px;

  &::placeholder {
    color: ${theme.colors.textTertiary};
  }

  &:focus {
    border-color: ${theme.colors.purple};
  }
`;

const SearchIcon = styled.div`
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: ${theme.colors.textTertiary};
`;

const RightSection = styled.div`
  display: flex;
  align-items: center;
  gap: ${theme.spacing.md};
`;

const IconButton = styled.button`
  width: 36px;
  height: 36px;
  background: transparent;
  border: none;
  border-radius: ${theme.borderRadius.md};
  color: ${theme.colors.textSecondary};
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;

  &:hover {
    background: ${theme.colors.secondary};
    color: ${theme.colors.textPrimary};
  }
`;

interface HeaderProps {}

const Header: React.FC<HeaderProps> = () => {
  const location = useLocation();

  const isActive = (path: string) => {
    return location.pathname === path;
  };

  return (
    <HeaderContainer>
      <HeaderContent>
        <Logo to="/">
          <LogoIcon>S</LogoIcon>
          SofaScore
        </Logo>

        <Navigation>
          <NavSection>
            <NavItem to="/" active={isActive("/")}>
              <NavIcon>⚽</NavIcon>
              Football
            </NavItem>
            <NavItem to="/basketball" active={isActive("/basketball")}>
              <NavIcon>🏀</NavIcon>
              Basketball
            </NavItem>
            <NavItem to="/tennis" active={isActive("/tennis")}>
              <NavIcon>🎾</NavIcon>
              Tennis
            </NavItem>
            <NavItem to="/table-tennis" active={isActive("/table-tennis")}>
              <NavIcon>🏓</NavIcon>
              Table Tennis
            </NavItem>
            <NavItem to="/ice-hockey" active={isActive("/ice-hockey")}>
              <NavIcon>🏒</NavIcon>
              Ice Hockey
            </NavItem>
            <NavItem to="/esports" active={isActive("/esports")}>
              <NavIcon>🎮</NavIcon>
              Esports
            </NavItem>
            <NavItem to="/handball" active={isActive("/handball")}>
              <NavIcon>🤾</NavIcon>
              Handball
            </NavItem>
            <NavItem to="/volleyball" active={isActive("/volleyball")}>
              <NavIcon>🏐</NavIcon>
              Volleyball
            </NavItem>
            <NavItem to="/baseball" active={isActive("/baseball")}>
              <NavIcon>⚾</NavIcon>
              Baseball
            </NavItem>
            <NavItem
              to="/american-football"
              active={isActive("/american-football")}
            >
              <NavIcon>🏈</NavIcon>
              American Football
            </NavItem>
          </NavSection>
        </Navigation>

        <SearchContainer>
          <SearchIcon>🔍</SearchIcon>
          <SearchInput placeholder="Search matches, competitions, teams, players, and more" />
        </SearchContainer>

        <RightSection>
          <IconButton>⭐</IconButton>
          <IconButton>❓</IconButton>
          <IconButton>⚙️</IconButton>
          <IconButton style={{ background: theme.colors.red, color: "white" }}>
            B
          </IconButton>
        </RightSection>
      </HeaderContent>
    </HeaderContainer>
  );
};

export default Header;
