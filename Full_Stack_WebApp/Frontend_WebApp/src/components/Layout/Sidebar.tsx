import React, { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/router";
import { motion, AnimatePresence } from "framer-motion";
import styles from "./Sidebar.module.css";

const navLinks = [
  { href: "/matches", label: "Matches" },
  { href: "/teams", label: "Teams" },
  { href: "/predictions", label: "Predictions" },
];

const Sidebar: React.FC = () => {
  const [open, setOpen] = useState(false);
  const router = useRouter();

  return (
    <>
      <div className={styles.hamburger} onClick={() => setOpen((o) => !o)}>
        <span className={open ? styles.open : ""}></span>
        <span className={open ? styles.open : ""}></span>
        <span className={open ? styles.open : ""}></span>
      </div>
      <AnimatePresence>
        {(open || typeof window === "undefined" || window.innerWidth > 900) && (
          <motion.aside
            className={styles.sidebar}
            initial={{ x: -260, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            exit={{ x: -260, opacity: 0 }}
            transition={{ type: "spring", stiffness: 200, damping: 30 }}
          >
            <div className={styles.logo}>
              <Link href="/">
                EPL <span>Predictions</span>
              </Link>
            </div>
            <nav className={styles.nav}>
              {navLinks.map((link) => (
                <Link
                  key={link.href}
                  href={link.href}
                  className={
                    router.pathname.startsWith(link.href)
                      ? `${styles.navLink} ${styles.active}`
                      : styles.navLink
                  }
                  onClick={() => setOpen(false)}
                >
                  {link.label}
                </Link>
              ))}
            </nav>
          </motion.aside>
        )}
      </AnimatePresence>
    </>
  );
};

export default Sidebar;
