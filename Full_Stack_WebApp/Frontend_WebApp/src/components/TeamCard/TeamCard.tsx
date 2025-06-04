import React from "react";
import Link from "next/link";
import { Team } from "../../types";
import styles from "./TeamCard.module.css";

interface TeamCardProps {
  team: Team;
}

const TeamCard: React.FC<TeamCardProps> = ({ team }) => {
  return (
    <Link href={`/teams/${team.id}`} className={styles.card}>
      <div className={styles.logoContainer}>
        <img
          src={team.logo || "/placeholder-team.png"}
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
  );
};

export default TeamCard;
