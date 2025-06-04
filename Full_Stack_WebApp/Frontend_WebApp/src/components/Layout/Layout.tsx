import React from "react";
import Header from "./Header";
import Footer from "./Footer";
import Sidebar from "./Sidebar";
import styles from "./Layout.module.css";

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className={styles.layout}>
      <Sidebar />
      <div className={styles.contentArea}>
        <Header />
        <main className={styles.main}>{children}</main>
        <Footer />
      </div>
    </div>
  );
};

export default Layout;
