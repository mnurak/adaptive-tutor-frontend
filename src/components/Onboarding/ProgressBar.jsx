import React from 'react';
import styles from './ProgressBar.module.css';

const ProgressBar = ({ progress, currentStep, totalSteps }) => {
  return (
    <div className={styles.container}>
      <div className={styles.info}>
        <span>Step {currentStep} of {totalSteps}</span>
        <span>{Math.round(progress)}%</span>
      </div>
      <div className={styles.barContainer}>
        <div 
          className={styles.bar} 
          style={{ width: `${progress}%` }}
        />
      </div>
    </div>
  );
};

export default ProgressBar;

