import React from "react";
import styles from "./Footer.module.css";

const Footer: React.FC = () => {
  return (
    <footer className={styles.footer}>
      <div className={styles.container}>
        <p className={styles.copyright}>
          © {new Date().getFullYear()} EPL Predictions. All rights reserved.
        </p>
        <div className={styles.links}>
          <a href="/about" className={styles.link}>
            About
          </a>
          <a href="/privacy" className={styles.link}>
            Privacy Policy
          </a>
          <a href="/terms" className={styles.link}>
            Terms of Service
          </a>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
