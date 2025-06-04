import React from "react";
import styles from "./Loading.module.css";

interface LoadingProps {
  message?: string;
}

const Loading: React.FC<LoadingProps> = ({ message = "Loading..." }) => {
  return (
    <div className={styles.loading}>
      <div className={styles.spinner}></div>
      <p className={styles.message}>{message}</p>
    </div>
  );
};

export default Loading;
