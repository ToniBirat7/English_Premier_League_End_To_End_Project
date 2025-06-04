import React from "react";
import Link from "next/link";
import { Team } from "../../types";
import { motion } from "framer-motion";
import styles from "./TeamCard.module.css";

interface TeamCardProps {
  team: Team;
}

const TeamCard: React.FC<TeamCardProps> = ({ team }) => {
  return (
    <motion.div
      className={`${styles.card} glass shadow`}
      whileHover={{
        scale: 1.04,
        boxShadow: "0 8px 32px 0 rgba(124,58,237,0.25)",
      }}
      whileTap={{ scale: 0.98 }}
      initial={{ opacity: 0, y: 40 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ type: "spring", stiffness: 120, damping: 18 }}
    >
      <Link href={`/teams/${team.id}`} className={styles.cardLink}>
        <div className={styles.logoContainer}>
          <img
            src={
              team.logo ||
              "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%23666'%3E%3Cpath d='M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-13h2v6h-2zm0 8h2v2h-2z'/%3E%3C/svg%3E"
            }
            alt={team.name}
            className={styles.logo}
          />
        </div>
        <div className={styles.info}>
          <h2 className={styles.name}>{team.name}</h2>
          <p className={styles.shortName}>{team.short_name}</p>
          <div className={styles.details}>
            <div className={styles.detail}>
              <span className={styles.label}>Stadium:</span>
              <span className={styles.value}>{team.stadium}</span>
            </div>
            <div className={styles.detail}>
              <span className={styles.label}>City:</span>
              <span className={styles.value}>{team.city}</span>
            </div>
            <div className={styles.detail}>
              <span className={styles.label}>Founded:</span>
              <span className={styles.value}>{team.founded_year}</span>
            </div>
          </div>
        </div>
      </Link>
      {team.website && (
        <a
          href={team.website}
          target="_blank"
          rel="noopener noreferrer"
          className={styles.website}
        >
          Visit Website
        </a>
      )}
    </motion.div>
  );
};

export default TeamCard;
