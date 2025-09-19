import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth.js';
import styles from './Dashboard.module.css';

const Dashboard = () => {
  const { user } = useAuth();
  if (!user) return <p>Loading user data...</p>;
  return (
    <div className={styles.dashboard}>
      <h1>Welcome back, {user.email}! 👋</h1>
      <p>This is your central hub for learning. What would you like to do today?</p>
      <div className={styles.cardContainer}>
        <div className={styles.card}>
          <h3>🧠 Your Profile</h3>
          <p>Review and dynamically update your cognitive learning profile based on your feedback.</p>
          <Link to="/profile" className={styles.ctaButton}>Go to Profile</Link>
        </div>
        <div className={styles.card}>
          <h3>📚 Generate a Lesson</h3>
          <p>Enter a concept you want to learn and get a lesson personalized just for you.</p>
          <Link to="/lesson" className={styles.ctaButton}>Start Learning</Link>
        </div>
      </div>
    </div>
  );
};
export default Dashboard;