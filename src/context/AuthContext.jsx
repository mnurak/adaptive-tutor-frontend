import React, { createContext, useState, useEffect } from 'react';
import api from '../api/api.js';
import { getToken, setToken, removeToken } from '../utils/storage.js';

export const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(!!getToken());
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const validateToken = async () => {
      if (getToken()) {
        try {
          const response = await api.get('/api/v1/student/me');
          setUser(response.data);
          setIsAuthenticated(true);
        } catch (error) {
          removeToken();
          setIsAuthenticated(false);
        }
      }
      setLoading(false);
    };
    validateToken();
  }, []);

  const login = async (email, password) => {
    const params = new URLSearchParams();
    params.append('username', email);
    params.append('password', password);
    const response = await api.post('/api/v1/login/access-token', params);
    setToken(response.data.access_token);
    const userProfile = await api.get('/api/v1/student/me');
    setUser(userProfile.data);
    setIsAuthenticated(true);
  };

  const register = (userData) => api.post('/api/v1/login/register', userData);

  const logout = () => {
    removeToken();
    setUser(null);
    setIsAuthenticated(false);
  };

  const value = { user, setUser, isAuthenticated, loading, login, register, logout };

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
};