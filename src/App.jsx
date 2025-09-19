import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Login from './components/Auth/Login.jsx';
import Register from './components/Auth/Register.jsx';
import Dashboard from './components/Dashboard/Dashboard.jsx';
import Chat from './components/Chat/Chat.jsx';
import Lesson from './components/Lesson/Lesson.jsx';
import Profile from './components/Profile/Profile.jsx';
import ProtectedRoute from './components/Common/ProtectedRoute.jsx';
import Header from './components/Layout/Header.jsx';

function App() {
  return (
    <div className="App">
      <Header />
      <main className="container">
        <Routes>
          {/* Public Routes */}
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />

          {/* Protected Routes */}
          {/* THIS IS THE FIX: Ensure this route for the root path exists. */}
          <Route path="/" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />

          <Route path="/profile" element={<ProtectedRoute><Profile /></ProtectedRoute>} />
          <Route path="/chat" element={<ProtectedRoute><Chat /></ProtectedRoute>} />
          <Route path="/lesson" element={<ProtectedRoute><Lesson /></ProtectedRoute>} />
        </Routes>
      </main>
    </div>
  );
}

export default App;