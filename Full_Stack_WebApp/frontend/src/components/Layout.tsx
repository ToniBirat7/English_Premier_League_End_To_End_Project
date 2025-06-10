import React from "react";
import styled from "styled-components";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Header from "./Header";
import Sidebar from "./Sidebar";
import HomePage from "../pages/HomePage";
import PremierLeaguePage from "../pages/PremierLeaguePage";
import MatchDetailPage from "../pages/MatchDetailPage";
import { theme } from "../styles/GlobalStyles";

const LayoutContainer = styled.div`
  min-height: 100vh;
  background: ${theme.colors.primary};
`;

const MainContent = styled.main`
  margin-left: 280px;
  margin-top: 60px;
  min-height: calc(100vh - 60px);
  background: ${theme.colors.primary};

  @media (max-width: ${theme.breakpoints.tablet}) {
    margin-left: 0;
  }
`;

const ContentArea = styled.div`
  max-width: 1400px; /* Increased max-width for 12-column layout */
  margin: 0 auto;
  padding: ${theme.spacing.lg} ${theme.spacing.xl};

  /* 12-column grid system with side margins */
  @media (min-width: 1600px) {
    max-width: 1200px; /* Content centered with margins on larger screens */
  }

  @media (max-width: ${theme.breakpoints.desktop}) {
    padding: ${theme.spacing.lg} ${theme.spacing.lg};
  }

  @media (max-width: ${theme.breakpoints.tablet}) {
    padding: ${theme.spacing.md} ${theme.spacing.md};
  }

  @media (max-width: ${theme.breakpoints.mobile}) {
    padding: ${theme.spacing.sm} ${theme.spacing.sm};
  }
`;

interface LayoutProps {}

const Layout: React.FC<LayoutProps> = () => {
  return (
    <Router>
      <LayoutContainer>
        <Header />
        <Sidebar />
        <MainContent>
          <ContentArea>
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/premier-league" element={<PremierLeaguePage />} />
              <Route path="/match/:matchId" element={<MatchDetailPage />} />
            </Routes>
          </ContentArea>
        </MainContent>
      </LayoutContainer>
    </Router>
  );
};

export default Layout;
