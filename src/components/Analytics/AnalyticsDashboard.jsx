import React, { useState, useEffect } from 'react';
import api from '../../api/api';
import styles from './AnalyticsDashboard.module.css';

const AnalyticsDashboard = () => {
  const [resourcePrefs, setResourcePrefs] = useState(null);
  const [learningPatterns, setLearningPatterns] = useState(null);
  const [masteryProgression, setMasteryProgression] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    setLoading(true);
    setError(null);

    try {
      const [prefsRes, patternsRes, masteryRes] = await Promise.all([
        api.get('/api/v1/analytics/resource-preferences'),
        api.get('/api/v1/analytics/learning-patterns'),
        api.get('/api/v1/analytics/mastery-progression')
      ]);

      setResourcePrefs(prefsRes.data);
      setLearningPatterns(patternsRes.data);
      setMasteryProgression(masteryRes.data);
    } catch (err) {
      console.error('Failed to fetch analytics:', err);
      setError('Failed to load analytics. You may need to complete some learning sessions first.');
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateProfile = async () => {
    try {
      await api.post('/api/v1/analytics/update-profile');
      alert('Profile updated successfully based on your learning behavior!');
      fetchAnalytics(); // Refresh data
    } catch (err) {
      console.error('Failed to update profile:', err);
      alert('Failed to update profile. Please try again.');
    }
  };

  if (loading) {
    return (
      <div className={styles.container}>
        <div className={styles.loading}>Loading analytics...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={styles.container}>
        <div className={styles.error}>{error}</div>
        <button onClick={fetchAnalytics} className={styles.retryButton}>
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h1>Learning Analytics</h1>
        <button onClick={handleUpdateProfile} className={styles.updateButton}>
          Update Profile from Behavior
        </button>
      </div>

      {/* Resource Preferences */}
      {resourcePrefs && (
        <div className={styles.section}>
          <h2>Resource Preferences</h2>
          <div className={styles.cards}>
            <div className={styles.card}>
              <div className={styles.cardLabel}>Video to Text Ratio</div>
              <div className={styles.cardValue}>
                {resourcePrefs.video_to_text_ratio?.toFixed(2) || 'N/A'}
              </div>
            </div>
            <div className={styles.card}>
              <div className={styles.cardLabel}>Preferred Type</div>
              <div className={styles.cardValue}>
                {resourcePrefs.preferred_resource_type || 'N/A'}
              </div>
            </div>
            <div className={styles.card}>
              <div className={styles.cardLabel}>Avg Engagement</div>
              <div className={styles.cardValue}>
                {resourcePrefs.avg_engagement_score?.toFixed(1) || 'N/A'}/5
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Learning Patterns */}
      {learningPatterns && (
        <div className={styles.section}>
          <h2>Learning Patterns</h2>
          <div className={styles.cards}>
            <div className={styles.card}>
              <div className={styles.cardLabel}>Avg Session Duration</div>
              <div className={styles.cardValue}>
                {learningPatterns.avg_session_duration_minutes?.toFixed(0) || 'N/A'} min
              </div>
            </div>
            <div className={styles.card}>
              <div className={styles.cardLabel}>Avg Focus Score</div>
              <div className={styles.cardValue}>
                {learningPatterns.avg_focus_score?.toFixed(2) || 'N/A'}
              </div>
            </div>
            <div className={styles.card}>
              <div className={styles.cardLabel}>Total Sessions</div>
              <div className={styles.cardValue}>
                {learningPatterns.total_sessions || 0}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Mastery Progression */}
      {masteryProgression && (
        <div className={styles.section}>
          <h2>Mastery Progression</h2>
          <div className={styles.cards}>
            <div className={styles.card}>
              <div className={styles.cardLabel}>Avg Learning Velocity</div>
              <div className={styles.cardValue}>
                {masteryProgression.avg_learning_velocity?.toFixed(2) || 'N/A'}
              </div>
            </div>
            <div className={styles.card}>
              <div className={styles.cardLabel}>Avg Retention</div>
              <div className={styles.cardValue}>
                {masteryProgression.avg_retention_score?.toFixed(2) || 'N/A'}
              </div>
            </div>
            <div className={styles.card}>
              <div className={styles.cardLabel}>Concepts Tracked</div>
              <div className={styles.cardValue}>
                {masteryProgression.total_concepts || 0}
              </div>
            </div>
          </div>

          {masteryProgression.mastery_distribution && (
            <div className={styles.masteryDistribution}>
              <h3>Mastery Distribution</h3>
              <div className={styles.distributionBars}>
                {Object.entries(masteryProgression.mastery_distribution).map(([level, count]) => (
                  <div key={level} className={styles.distributionItem}>
                    <span className={styles.distributionLabel}>{level}</span>
                    <div className={styles.distributionBar}>
                      <div 
                        className={styles.distributionFill}
                        style={{ 
                          width: `${(count / masteryProgression.total_concepts) * 100}%` 
                        }}
                      />
                    </div>
                    <span className={styles.distributionCount}>{count}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default AnalyticsDashboard;

