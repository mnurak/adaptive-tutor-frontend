import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '../../api/api.js';
import styles from './Register.module.css';
import Loader from '../Common/Loader.jsx';

const initialProfile = {
  instruction_flow: 'sequential',
  input_preference: 'verbal',
  engagement_style: 'reflective',
  concept_type: 'intuitive',
  learning_autonomy: 'guided',
  motivation_type: 'intrinsic',
  feedback_preference: 'delayed',
  complexity_tolerance: 'high',
};

const Register = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    cognitive_profile: initialProfile,
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleProfileChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      cognitive_profile: { ...prev.cognitive_profile, [name]: value },
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setLoading(true);
    try {
      await api.post('/api/v1/login/register', formData);
      setSuccess('Registration successful! Redirecting to login...');
      setTimeout(() => navigate('/login'), 2000);
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.authContainer}>
      <form onSubmit={handleSubmit} className={styles.authForm}>
        <h2>Register</h2>
        {error && <p className={styles.error}>{error}</p>}
        {success && <p className={styles.success}>{success}</p>}
        <div className={styles.formGroup}>
          <label htmlFor="email">Email</label>
          <input type="email" id="email" name="email" onChange={handleChange} required />
        </div>
        <div className={styles.formGroup}>
          <label htmlFor="password">Password</label>
          <input type="password" id="password" name="password" onChange={handleChange} required />
        </div>
        <h3>Cognitive Profile (Initial Setup)</h3>
        {Object.keys(initialProfile).map((key) => (
          <div className={styles.formGroup} key={key}>
            <label htmlFor={key}>{key.replace(/_/g, ' ')}</label>
            <input id={key} name={key} value={formData.cognitive_profile[key]} onChange={handleProfileChange} />
          </div>
        ))}
        <button type="submit" className={styles.submitButton} disabled={loading}>
          {loading ? <Loader /> : 'Register'}
        </button>
        <p className={styles.redirectText}>
          Already have an account? <Link to="/login">Login here</Link>
        </p>
      </form>
    </div>
  );
};
export default Register;