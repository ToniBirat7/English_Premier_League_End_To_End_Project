import React, { useState } from "react";
import Header from "./components/Header";
import Home from "./pages/Home";
import Fixtures from "./pages/Fixtures";
import LeagueTablePage from "./pages/LeagueTable";
import Teams from "./pages/Teams";
import "./App.css";

function App() {
  const [activeSection, setActiveSection] = useState("home");

  const renderActiveSection = () => {
    switch (activeSection) {
      case "home":
        return <Home />;
      case "fixtures":
        return <Fixtures />;
      case "table":
        return <LeagueTablePage />;
      case "teams":
        return <Teams />;
      default:
        return <Home />;
    }
  };

  return (
    <div className="App">
      <Header
        activeSection={activeSection}
        onSectionChange={setActiveSection}
      />
      <main className="main-content">{renderActiveSection()}</main>
    </div>
  );
}

export default App;
