import React from "react";
import styled from "styled-components";
import { theme } from "../styles/GlobalStyles";

const MenuToggleButton = styled.button<{ isOpen?: boolean }>`
  display: none;
  background: transparent;
  border: none;
  color: ${theme.colors.textPrimary};
  font-size: 20px;
  cursor: pointer;
  padding: ${theme.spacing.sm};
  border-radius: ${theme.borderRadius.sm};
  transition: all 0.2s ease;

  &:hover {
    background: ${theme.colors.secondary};
  }

  @media (max-width: ${theme.breakpoints.tablet}) {
    display: flex;
    align-items: center;
    justify-content: center;
  }
`;

interface MobileMenuToggleProps {
  isOpen: boolean;
  onToggle: () => void;
}

const MobileMenuToggle: React.FC<MobileMenuToggleProps> = ({ isOpen, onToggle }) => {
  return (
    <MenuToggleButton isOpen={isOpen} onClick={onToggle} aria-label="Toggle menu">
      {isOpen ? "✕" : "☰"}
    </MenuToggleButton>
  );
};

export default MobileMenuToggle;
