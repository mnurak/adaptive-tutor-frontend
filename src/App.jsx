import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Login from './components/Auth/Login.jsx';
import Register from './components/Auth/Register.jsx';
import Dashboard from './components/Dashboard/Dashboard.jsx';
import Chat from './components/Chat/Chat.jsx'; // Import Chat instead of Lesson
import Profile from './components/Profile/Profile.jsx';
import ProtectedRoute from './components/Common/ProtectedRoute.jsx';
import Header from './components/Layout/Header.jsx';

function App() {
  return (
    <div className="App">
      <Header />
      <main className="container">
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
          <Route path="/profile" element={<ProtectedRoute><Profile /></ProtectedRoute>} />
          {/* Replace /lesson route with /chat */}
          <Route path="/chat" element={<ProtectedRoute><Chat /></ProtectedRoute>} /> 
        </Routes>
      </main>
    </div>
  );
}

export default App;