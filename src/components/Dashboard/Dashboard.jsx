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
      <p>Choose your preferred way to learn today.</p>
      <div className={styles.cardContainer}>
        <div className={styles.card}>
          <h3>💬 Conversational Tutor</h3>
          <p>Start a dynamic conversation. The tutor adapts to your questions in real-time.</p>
          <Link to="/chat" className={styles.ctaButton}>Start Chatting</Link>
        </div>
        <div className={styles.card}>
          <h3>📚 Structured Lesson</h3>
          <p>Request a complete, structured lesson on a specific topic based on your profile.</p>
          <Link to="/lesson" className={styles.ctaButton}>Generate Lesson</Link>
        </div>
        <div className={styles.card}>
          <h3>🧠 Your Profile</h3>
          <p>Review your cognitive learning profile, which updates as you interact with the tutor.</p>
          <Link to="/profile" className={styles.ctaButton}>View Profile</Link>
        </div>
      </div>
    </div>
  );
};
export default Dashboard;