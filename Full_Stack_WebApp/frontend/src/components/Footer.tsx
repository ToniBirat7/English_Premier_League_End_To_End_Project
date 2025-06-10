import React from "react";
import styled from "styled-components";
import { Link } from "react-router-dom";
import { theme } from "../styles/GlobalStyles";

const FooterContainer = styled.footer`
  background: ${theme.colors.primary};
  border-top: 1px solid ${theme.colors.border};
  margin-top: ${theme.spacing.xxl};
`;

const FooterContent = styled.div`
  max-width: 1400px;
  margin: 0 auto;
  padding: ${theme.spacing.xl};
  
  @media (max-width: ${theme.breakpoints.desktop}) {
    padding: ${theme.spacing.lg};
  }
  
  @media (max-width: ${theme.breakpoints.tablet}) {
    padding: ${theme.spacing.md};
  }
  
  @media (max-width: ${theme.breakpoints.mobile}) {
    padding: ${theme.spacing.sm};
  }
`;

const FooterGrid = styled.div`
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  gap: ${theme.spacing.xl};
  
  @media (max-width: ${theme.breakpoints.tablet}) {
    grid-template-columns: 1fr 1fr;
    gap: ${theme.spacing.lg};
  }
  
  @media (max-width: ${theme.breakpoints.mobile}) {
    grid-template-columns: 1fr;
    gap: ${theme.spacing.md};
  }
`;

const FooterSection = styled.div`
  display: flex;
  flex-direction: column;
  gap: ${theme.spacing.md};
`;

const FooterTitle = styled.h3`
  color: ${theme.colors.textPrimary};
  font-size: 16px;
  font-weight: bold;
  margin: 0;
`;

const FooterLink = styled(Link)`
  color: ${theme.colors.textSecondary};
  font-size: 14px;
  text-decoration: none;
  transition: color 0.2s ease;
  
  &:hover {
    color: ${theme.colors.purple};
  }
`;

const FooterText = styled.p`
  color: ${theme.colors.textSecondary};
  font-size: 14px;
  margin: 0;
  line-height: 1.5;
`;

const FooterBottom = styled.div`
  border-top: 1px solid ${theme.colors.border};
  margin-top: ${theme.spacing.xl};
  padding-top: ${theme.spacing.lg};
  display: flex;
  justify-content: space-between;
  align-items: center;
  
  @media (max-width: ${theme.breakpoints.mobile}) {
    flex-direction: column;
    gap: ${theme.spacing.md};
    text-align: center;
  }
`;

const Copyright = styled.p`
  color: ${theme.colors.textTertiary};
  font-size: 12px;
  margin: 0;
`;

const SocialLinks = styled.div`
  display: flex;
  gap: ${theme.spacing.md};
`;

const SocialLink = styled.a`
  color: ${theme.colors.textSecondary};
  font-size: 18px;
  text-decoration: none;
  transition: color 0.2s ease;
  
  &:hover {
    color: ${theme.colors.purple};
  }
`;

const Footer: React.FC = () => {
  return (
    <FooterContainer>
      <FooterContent>
        <FooterGrid>
          <FooterSection>
            <FooterTitle>Premier League Hub</FooterTitle>
            <FooterText>
              Your ultimate destination for Premier League scores, fixtures, standings, 
              and statistics. Stay updated with the latest from England's top football league.
            </FooterText>
          </FooterSection>
          
          <FooterSection>
            <FooterTitle>Quick Links</FooterTitle>
            <FooterLink to="/premier-league">Premier League</FooterLink>
            <FooterLink to="/">Live Scores</FooterLink>
            <FooterLink to="/premier-league">Fixtures</FooterLink>
            <FooterLink to="/premier-league">Standings</FooterLink>
          </FooterSection>
          
          <FooterSection>
            <FooterTitle>Statistics</FooterTitle>
            <FooterLink to="/premier-league">Team Stats</FooterLink>
            <FooterLink to="/premier-league">Player Stats</FooterLink>
            <FooterLink to="/premier-league">Season Records</FooterLink>
            <FooterLink to="/premier-league">Historical Data</FooterLink>
          </FooterSection>
          
          <FooterSection>
            <FooterTitle>About</FooterTitle>
            <FooterLink to="/">About Us</FooterLink>
            <FooterLink to="/">Contact</FooterLink>
            <FooterLink to="/">Privacy Policy</FooterLink>
            <FooterLink to="/">Terms of Service</FooterLink>
          </FooterSection>
        </FooterGrid>
        
        <FooterBottom>
          <Copyright>
            © {new Date().getFullYear()} Premier League Hub. All rights reserved.
          </Copyright>
          <SocialLinks>
            <SocialLink href="#" aria-label="Twitter">🐦</SocialLink>
            <SocialLink href="#" aria-label="Facebook">📘</SocialLink>
            <SocialLink href="#" aria-label="Instagram">📷</SocialLink>
            <SocialLink href="#" aria-label="YouTube">📺</SocialLink>
          </SocialLinks>
        </FooterBottom>
      </FooterContent>
    </FooterContainer>
  );
};

export default Footer;
