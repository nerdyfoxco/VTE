import React, { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import './index.css';
import App from './App.tsx';
import axios from 'axios';

// Globally attach environment URL for Production (Vercel) vs Dev (Vite Proxy)
axios.defaults.baseURL = import.meta.env.VITE_API_URL || '';

// VTE 3.0 Identity Components
import Login from './pages/auth/Login';
import Signup from './pages/auth/Signup';
import MFAChallenge from './pages/auth/MFAChallenge';
import Landing from './pages/Landing';

// VTE Fail-Closed Route Guardian
const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
  const token = localStorage.getItem('vte_session');
  // If no secure session token exists in local storage, kick to login.
  if (!token) {
    return <Navigate to="/login" replace />;
  }
  return children;
};

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        {/* Public Identity Routes */}
        <Route path="/" element={<Landing />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/mfa" element={<MFAChallenge />} />

        {/* Private Operator OS Routes */}
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <App />
            </ProtectedRoute>
          }
        />

        {/* Fallback */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  </StrictMode>,
);
