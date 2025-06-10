import React from "react";
import styled, { keyframes } from "styled-components";
import { theme } from "../styles/GlobalStyles";

// Football loading animations
const footballSpin = keyframes`
  0% { 
    transform: rotate(0deg) scale(1);
    box-shadow: 0 0 0 0 rgba(139, 92, 246, 0.7);
  }
  25% { 
    transform: rotate(90deg) scale(1.1);
    box-shadow: 0 0 0 10px rgba(139, 92, 246, 0.3);
  }
  50% { 
    transform: rotate(180deg) scale(1.2);
    box-shadow: 0 0 0 20px rgba(139, 92, 246, 0.1);
  }
  75% { 
    transform: rotate(270deg) scale(1.1);
    box-shadow: 0 0 0 10px rgba(139, 92, 246, 0.3);
  }
  100% { 
    transform: rotate(360deg) scale(1);
    box-shadow: 0 0 0 0 rgba(139, 92, 246, 0.7);
  }
`;

const footballBounce = keyframes`
  0%, 20%, 50%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-20px);
  }
  60% {
    transform: translateY(-10px);
  }
`;

const textGlow = keyframes`
  0%, 100% {
    text-shadow: 0 0 5px rgba(139, 92, 246, 0.5);
  }
  50% {
    text-shadow: 0 0 20px rgba(139, 92, 246, 0.8), 0 0 30px rgba(139, 92, 246, 0.6);
  }
`;

const dotsAnimation = keyframes`
  0%, 80%, 100% {
    opacity: 0;
    transform: scale(0.8);
  }
  40% {
    opacity: 1;
    transform: scale(1);
  }
`;

const progressSlide = keyframes`
  0% { left: -100%; }
  100% { left: 100%; }
`;

const LoadingContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: ${theme.spacing.xxl};
  min-height: 200px;
`;

const FootballContainer = styled.div`
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: ${theme.spacing.xl};
`;

const Football = styled.div`
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #ffffff 0%, #f0f0f0 50%, #e0e0e0 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 30px;
  animation: ${footballSpin} 2s ease-in-out infinite;
  position: relative;

  &::before {
    content: "";
    position: absolute;
    top: 10%;
    left: 10%;
    right: 10%;
    bottom: 10%;
    border: 2px solid #333;
    border-radius: 50%;
  }

  &::after {
    content: "";
    position: absolute;
    top: 20%;
    left: 20%;
    right: 20%;
    bottom: 20%;
    background: radial-gradient(circle at 30% 30%, #ffffff 0%, transparent 50%);
    border-radius: 50%;
  }
`;

const LoadingText = styled.div`
  color: ${theme.colors.textPrimary};
  font-size: 18px;
  font-weight: 600;
  margin-bottom: ${theme.spacing.md};
  animation: ${textGlow} 2s ease-in-out infinite;
`;

const LoadingDots = styled.div`
  display: flex;
  gap: ${theme.spacing.sm};
`;

const Dot = styled.div<{ delay: number }>`
  width: 8px;
  height: 8px;
  background: ${theme.colors.purple};
  border-radius: 50%;
  animation: ${dotsAnimation} 1.4s infinite ease-in-out;
  animation-delay: ${(props) => props.delay}s;
`;

const ProgressBar = styled.div`
  width: 200px;
  height: 4px;
  background: ${theme.colors.tertiary};
  border-radius: 2px;
  margin-top: ${theme.spacing.lg};
  overflow: hidden;
  position: relative;

  &::after {
    content: "";
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(
      90deg,
      ${theme.colors.purple},
      ${theme.colors.blue}
    );
    animation: ${progressSlide} 2s ease-in-out infinite;
  }
`;

interface LoadingSpinnerProps {
  text?: string;
  showProgress?: boolean;
}

const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
  text = "Loading matches...",
  showProgress = false,
}) => {
  return (
    <LoadingContainer>
      <FootballContainer>
        <Football>⚽</Football>
      </FootballContainer>

      <LoadingText>{text}</LoadingText>

      <LoadingDots>
        <Dot delay={0} />
        <Dot delay={0.2} />
        <Dot delay={0.4} />
      </LoadingDots>

      {showProgress && <ProgressBar />}
    </LoadingContainer>
  );
};

export default LoadingSpinner;
