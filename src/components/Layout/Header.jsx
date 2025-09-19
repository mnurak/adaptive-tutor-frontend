import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth.js';
import styles from './Header.module.css';

const Header = () => {
  const { isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <header className={styles.header}>
      <div className={`${styles.headerContent} container`}>
        <NavLink to="/" className={styles.logo}>
          🎓 Adaptive Tutor
        </NavLink>
        <nav>
          {isAuthenticated ? (
            <>
              <NavLink to="/" className={({ isActive }) => (isActive ? styles.active : '')}>Dashboard</NavLink>
              <NavLink to="/profile" className={({ isActive }) => (isActive ? styles.active : '')}>Profile</NavLink>
              <NavLink to="/lesson" className={({ isActive }) => (isActive ? styles.active : '')}>Lesson</NavLink>
              <button onClick={handleLogout} className={styles.logoutButton}>Logout</button>
            </>
          ) : (
            <>
              <NavLink to="/login" className={({ isActive }) => (isActive ? styles.active : '')}>Login</NavLink>
              <NavLink to="/register" className={({ isActive }) => (isActive ? styles.active : '')}>Register</NavLink>
            </>
          )}
        </nav>
      </div>
    </header>
  );
};
export default Header;
