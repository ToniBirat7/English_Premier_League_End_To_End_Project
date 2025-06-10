import React, { useState } from "react";
import styled, { keyframes } from "styled-components";
import { Link, useLocation } from "react-router-dom";
import { theme } from "../styles/GlobalStyles";

// Football animation keyframes
const footballSpin = keyframes`
  0% { transform: rotate(0deg) scale(1); }
  50% { transform: rotate(180deg) scale(1.1); }
  100% { transform: rotate(360deg) scale(1); }
`;

const footballBounce = keyframes`
  0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
  40% { transform: translateY(-10px); }
  60% { transform: translateY(-5px); }
`;

const shimmer = keyframes`
  0% { background-position: -200px 0; }
  100% { background-position: calc(200px + 100%) 0; }
`;

const fadeInUp = keyframes`
  0% {
    opacity: 0;
    transform: translateY(20px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
`;

const pulse = keyframes`
  0% { box-shadow: 0 0 0 0 rgba(139, 92, 246, 0.7); }
  70% { box-shadow: 0 0 0 10px rgba(139, 92, 246, 0); }
  100% { box-shadow: 0 0 0 0 rgba(139, 92, 246, 0); }
`;

const HeaderContainer = styled.header`
  background: linear-gradient(
    135deg,
    ${theme.colors.primary} 0%,
    ${theme.colors.secondary} 100%
  );
  border-bottom: 1px solid ${theme.colors.border};
  position: sticky;
  top: 0;
  z-index: 1000;
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;

  &::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(
      90deg,
      ${theme.colors.purple},
      ${theme.colors.blue},
      ${theme.colors.green}
    );
    background-size: 200% 100%;
    animation: ${shimmer} 3s infinite;
  }
`;

const HeaderContent = styled.div`
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 ${theme.spacing.xl};
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 70px;
  animation: ${fadeInUp} 0.6s ease-out;

  @media (max-width: ${theme.breakpoints.desktop}) {
    padding: 0 ${theme.spacing.lg};
  }

  @media (max-width: ${theme.breakpoints.tablet}) {
    padding: 0 ${theme.spacing.md};
    height: 60px;
  }

  @media (max-width: ${theme.breakpoints.mobile}) {
    padding: 0 ${theme.spacing.sm};
  }
`;

const Logo = styled(Link)`
  display: flex;
  align-items: center;
  gap: ${theme.spacing.md};
  font-size: 26px;
  font-weight: 800;
  color: ${theme.colors.textPrimary};
  text-decoration: none;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;

  &:hover {
    color: ${theme.colors.purple};
    transform: translateY(-2px);

    .logo-icon {
      animation: ${footballSpin} 1s ease-in-out;
    }
  }

  &::after {
    content: "";
    position: absolute;
    width: 0;
    height: 2px;
    bottom: -5px;
    left: 50%;
    background: linear-gradient(
      90deg,
      ${theme.colors.purple},
      ${theme.colors.blue}
    );
    transition: all 0.3s ease;
    transform: translateX(-50%);
  }

  &:hover::after {
    width: 100%;
  }
`;

const LogoIcon = styled.div`
  width: 40px;
  height: 40px;
  background: linear-gradient(
    135deg,
    ${theme.colors.purple} 0%,
    ${theme.colors.blue} 100%
  );
  border-radius: ${theme.borderRadius.lg};
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  font-size: 18px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(139, 92, 246, 0.3);

  &:hover {
    animation: ${pulse} 1.5s infinite;
    transform: scale(1.1);
  }
`;

const Navigation = styled.nav`
  display: flex;
  align-items: center;
  gap: ${theme.spacing.xl};

  @media (max-width: ${theme.breakpoints.tablet}) {
    display: none;
  }
`;

const NavSection = styled.div`
  display: flex;
  align-items: center;
  gap: ${theme.spacing.lg};
`;

const NavItem = styled(Link).withConfig({
  shouldForwardProp: (prop) => prop !== "active",
})<{ active?: boolean }>`
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: ${theme.spacing.md} ${theme.spacing.lg};
  color: ${(props) =>
    props.active ? theme.colors.purple : theme.colors.textSecondary};
  text-decoration: none;
  font-size: 14px;
  font-weight: 600;
  border-radius: ${theme.borderRadius.lg};
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

  &:hover {
    color: ${theme.colors.purple};
    background: rgba(139, 92, 246, 0.05);
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(139, 92, 246, 0.15);

    &::before {
      left: 100%;
    }

    .nav-icon {
      animation: ${footballBounce} 0.6s ease;
    }
  }

  ${(props) =>
    props.active &&
    `
    color: ${theme.colors.purple};
    background: rgba(139, 92, 246, 0.1);
    box-shadow: 0 4px 15px rgba(139, 92, 246, 0.2);
  `}
`;

const NavIcon = styled.div`
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  transition: transform 0.3s ease;
`;

const SearchContainer = styled.div`
  position: relative;
  flex: 1;
  max-width: 500px;
  margin: 0 ${theme.spacing.xl};

  @media (max-width: ${theme.breakpoints.tablet}) {
    max-width: 300px;
    margin: 0 ${theme.spacing.md};
  }

  @media (max-width: ${theme.breakpoints.mobile}) {
    display: none;
  }
`;

const SearchInput = styled.input`
  width: 100%;
  padding: ${theme.spacing.md} ${theme.spacing.lg};
  padding-left: 50px;
  background: rgba(255, 255, 255, 0.05);
  border: 2px solid transparent;
  border-radius: ${theme.borderRadius.xl};
  color: ${theme.colors.textPrimary};
  font-size: 14px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  backdrop-filter: blur(10px);

  &::placeholder {
    color: ${theme.colors.textTertiary};
    transition: color 0.3s ease;
  }

  &:focus {
    outline: none;
    border-color: ${theme.colors.purple};
    background: rgba(255, 255, 255, 0.08);
    box-shadow: 0 0 0 4px rgba(139, 92, 246, 0.1);
    transform: translateY(-1px);

    &::placeholder {
      color: transparent;
    }

    + .search-icon {
      color: ${theme.colors.purple};
      transform: scale(1.1);
    }
  }

  &:hover {
    border-color: rgba(139, 92, 246, 0.3);
    background: rgba(255, 255, 255, 0.07);
  }
`;

const SearchIcon = styled.div`
  position: absolute;
  left: ${theme.spacing.md};
  top: 50%;
  transform: translateY(-50%);
  color: ${theme.colors.textTertiary};
  font-size: 18px;
  transition: all 0.3s ease;
  pointer-events: none;
`;

const RightSection = styled.div`
  display: flex;
  align-items: center;
  gap: ${theme.spacing.md};

  @media (max-width: ${theme.breakpoints.mobile}) {
    gap: ${theme.spacing.sm};
  }
`;

const IconButton = styled.button`
  width: 42px;
  height: 42px;
  background: rgba(255, 255, 255, 0.05);
  border: 2px solid transparent;
  border-radius: ${theme.borderRadius.lg};
  color: ${theme.colors.textSecondary};
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 16px;
  font-weight: 600;
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
    color: ${theme.colors.purple};
    background: rgba(139, 92, 246, 0.1);
    border-color: rgba(139, 92, 246, 0.3);
    transform: translateY(-2px) scale(1.05);
    box-shadow: 0 8px 25px rgba(139, 92, 246, 0.2);

    &::before {
      width: 100px;
      height: 100px;
    }
  }

  &:active {
    transform: translateY(0) scale(0.95);
  }

  &.profile-btn {
    background: linear-gradient(135deg, ${theme.colors.red} 0%, #ff6b6b 100%);
    color: white;
    border-color: transparent;
    font-weight: 700;

    &:hover {
      background: linear-gradient(135deg, #ff6b6b 0%, ${theme.colors.red} 100%);
      transform: translateY(-2px) scale(1.05);
      box-shadow: 0 8px 25px rgba(239, 68, 68, 0.3);
    }
  }
`;

const Header: React.FC = () => {
  const location = useLocation();

  const [isSearchFocused, setIsSearchFocused] = useState(false);

  const isActive = (path: string) => {
    return location.pathname === path;
  };

  return (
    <HeaderContainer>
      <HeaderContent>
        <Logo to="/">
          <LogoIcon className="logo-icon">⚽</LogoIcon>
          Premier League Hub
        </Logo>

        <Navigation>
          <NavSection>
            <NavItem to="/" active={isActive("/")}>
              <NavIcon className="nav-icon">⚽</NavIcon>
              Football
            </NavItem>
          </NavSection>
        </Navigation>

        <SearchContainer>
          <SearchIcon className="search-icon">🔍</SearchIcon>
          <SearchInput
            placeholder="Search matches, competitions, teams, players, and more"
            onFocus={() => setIsSearchFocused(true)}
            onBlur={() => setIsSearchFocused(false)}
          />
        </SearchContainer>

        <RightSection>
          <IconButton title="Favorites">⭐</IconButton>
          <IconButton title="Help">❓</IconButton>
          <IconButton title="Settings">⚙️</IconButton>
          <IconButton className="profile-btn" title="Profile">
            B
          </IconButton>
        </RightSection>
      </HeaderContent>
    </HeaderContainer>
  );
};

export default Header;
