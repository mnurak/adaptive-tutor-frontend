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
          <p>Review your cognitive learning profile, which adapts as you chat with the tutor.</p>
          <Link to="/profile" className={styles.ctaButton}>Go to Profile</Link>
        </div>
        <div className={styles.card}>
          {/* Update this card to point to the new chat feature */}
          <h3>💬 Chat with your Tutor</h3>
          <p>Start a conversation with your personal AI tutor to learn any concept adaptively.</p>
          <Link to="/chat" className={styles.ctaButton}>Start Chatting</Link>
        </div>
      </div>
    </div>
  );
};
export default Dashboard;