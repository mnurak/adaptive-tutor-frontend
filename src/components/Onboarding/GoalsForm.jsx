import React from 'react';
import styles from './GoalsForm.module.css';

const GoalsForm = ({ goals, onChange }) => {
  const handleChange = (field, value) => {
    onChange({
      ...goals,
      [field]: value
    });
  };

  return (
    <div className={styles.container}>
      <h2>Finally, tell us about your learning goals</h2>
      
      <div className={styles.formGroup}>
        <label htmlFor="learning_goal">What do you want to learn?</label>
        <textarea
          id="learning_goal"
          className={styles.textarea}
          value={goals.learning_goal}
          onChange={(e) => handleChange('learning_goal', e.target.value)}
          placeholder="E.g., Master data structures and algorithms for technical interviews"
          rows={4}
          required
        />
      </div>

      <div className={styles.formGroup}>
        <label htmlFor="available_hours">
          How many hours per week can you dedicate to learning?
        </label>
        <input
          type="number"
          id="available_hours"
          className={styles.input}
          value={goals.available_hours_per_week}
          onChange={(e) => handleChange('available_hours_per_week', parseInt(e.target.value))}
          min="1"
          max="40"
        />
        <span className={styles.hint}>{goals.available_hours_per_week} hours/week</span>
      </div>

      <div className={styles.formGroup}>
        <label htmlFor="session_duration">
          Preferred session duration (minutes)
        </label>
        <input
          type="number"
          id="session_duration"
          className={styles.input}
          value={goals.preferred_session_duration}
          onChange={(e) => handleChange('preferred_session_duration', parseInt(e.target.value))}
          min="15"
          max="120"
          step="15"
        />
        <span className={styles.hint}>{goals.preferred_session_duration} minutes per session</span>
      </div>
    </div>
  );
};

export default GoalsForm;

