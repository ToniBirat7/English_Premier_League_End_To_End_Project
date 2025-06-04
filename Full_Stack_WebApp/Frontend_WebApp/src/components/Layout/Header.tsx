import React from "react";
import Link from "next/link";
import styles from "./Header.module.css";

const Header: React.FC = () => {
  return (
    <header className={styles.header}>
      <div className={styles.container}>
        <Link href="/" className={styles.logo}>
          EPL Predictions
        </Link>
        <nav className={styles.nav}>
          <Link href="/matches" className={styles.navLink}>
            Matches
          </Link>
          <Link href="/teams" className={styles.navLink}>
            Teams
          </Link>
          <Link href="/predictions" className={styles.navLink}>
            Predictions
          </Link>
        </nav>
      </div>
    </header>
  );
};

export default Header;
