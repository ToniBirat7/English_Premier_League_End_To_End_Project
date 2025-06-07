import React from "react";
import "./Header.css";

interface HeaderProps {
  activeSection: string;
  onSectionChange: (section: string) => void;
}

const Header: React.FC<HeaderProps> = ({ activeSection, onSectionChange }) => {
  const navigation = [
    { id: "home", label: "Home", icon: "🏠" },
    { id: "fixtures", label: "Fixtures", icon: "📅" },
    { id: "table", label: "Table", icon: "📊" },
    { id: "teams", label: "Teams", icon: "👥" },
  ];

  return (
    <header className="header">
      <div className="header-container">
        <div className="header-brand">
          <h1 className="brand-title">
            <span className="brand-icon">⚽</span>
            Premier League Hub
          </h1>
        </div>

        <nav className="header-nav">
          <ul className="nav-list">
            {navigation.map((item) => (
              <li key={item.id} className="nav-item">
                <button
                  className={`nav-button ${
                    activeSection === item.id ? "active" : ""
                  }`}
                  onClick={() => onSectionChange(item.id)}
                >
                  <span className="nav-icon">{item.icon}</span>
                  <span className="nav-label">{item.label}</span>
                </button>
              </li>
            ))}
          </ul>
        </nav>

        <div className="header-season">
          <span className="season-badge">2024-25</span>
        </div>
      </div>
    </header>
  );
};

export default Header;
