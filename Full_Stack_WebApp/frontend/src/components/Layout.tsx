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
`;

const ContentArea = styled.div`
  padding: ${theme.spacing.lg};
  max-width: 1200px;
  margin: 0 auto;
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
              <Route
                path="/champions-league"
                element={<div>Champions League coming soon...</div>}
              />
              <Route
                path="/europa-league"
                element={<div>Europa League coming soon...</div>}
              />
              <Route
                path="/laliga"
                element={<div>LaLiga coming soon...</div>}
              />
              <Route
                path="/bundesliga"
                element={<div>Bundesliga coming soon...</div>}
              />
            </Routes>
          </ContentArea>
        </MainContent>
      </LayoutContainer>
    </Router>
  );
};

export default Layout;
