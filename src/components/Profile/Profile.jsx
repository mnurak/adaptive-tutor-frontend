import React, { useState } from 'react';
import { useAuth } from '../../hooks/useAuth.js';
import api from '../../api/api.js';
import styles from './Profile.module.css';
import Loader from '../Common/Loader.jsx';

const Profile = () => {
  const { user, setUser } = useAuth();
  const [prompt, setPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [messageType, setMessageType] = useState('');

  const handleAnalyze = async (e) => {
    e.preventDefault();
    if (!prompt) return;
    setLoading(true);
    setMessage('');
    try {
      const response = await api.post('/api/v1/student/me/analyze/preview', { prompt });
      setUser((prevUser) => ({ ...prevUser, cognitive_profile: response.data }));
      setMessage('Success! Your profile has been updated.');
      setMessageType('success');
      setPrompt('');
    } catch (error) {
      setMessage('Failed to update profile. Please try again.');
      setMessageType('error');
    } finally {
      setLoading(false);
    }
  };

  if (!user) return <p>Loading...</p>;

  return (
    <div className={styles.profileContainer}>
      <h2>Your Cognitive Profile</h2>
      <p>This profile helps us tailor lessons specifically for you.</p>
      <div className={styles.profileGrid}>
        {Object.entries(user.cognitive_profile).map(([key, value]) => (
          key !== 'id' && key !== 'user_id' && (
            <div className={styles.profileItem} key={key}>
              <span className={styles.profileKey}>{key.replace(/_/g, ' ')}:</span>
              <span className={styles.profileValue}>{String(value)}</span>
            </div>
          )
        ))}
      </div>
      <div className={styles.analyzer}>
        <h3>Refine Your Learning Style</h3>
        <form onSubmit={handleAnalyze}>
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="e.g., Explain this with a diagram..."
            rows="4"
          />
          <button type="submit" disabled={loading || !prompt}>
            {loading ? <Loader /> : 'Analyze & Update'}
          </button>
        </form>
        {message && <p className={`${styles.message} ${styles[messageType]}`}>{message}</p>}
      </div>
    </div>
  );
};
export default Profile;