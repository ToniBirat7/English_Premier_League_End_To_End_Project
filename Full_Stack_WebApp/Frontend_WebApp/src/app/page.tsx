import Link from "next/link";
import styles from "./page.module.css";

export default function Home() {
  return (
    <div className={styles.page}>
      <main className={styles.main}>
        <h1 className={styles.title}>English Premier League Predictions</h1>
        <p className={styles.description}>
          Get AI-powered predictions for upcoming Premier League matches
        </p>

        <div className={styles.grid}>
          <Link href="/teams" className={styles.card}>
            <h2>Teams &rarr;</h2>
            <p>View all Premier League teams and their statistics.</p>
          </Link>

          <Link href="/predictions" className={styles.card}>
            <h2>Predictions &rarr;</h2>
            <p>See match predictions and create new ones.</p>
          </Link>

          <Link href="/matches" className={styles.card}>
            <h2>Matches &rarr;</h2>
            <p>Browse upcoming and past matches.</p>
          </Link>
        </div>
      </main>
    </div>
  );
}
