import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './components/Login';
import Signup from './components/Signup';
import Dashboard from './components/Dashboard';
import ProtectedRoute from './components/ProtectedRoute';
import Header from './components/Header'; // Correct import

function App() {
  
  // --- FIX 1 ---
  // The function must be defined *before* the return statement.
  const handleLogout = () => {
    // Replace 'token' with the name of your auth token in localStorage
    localStorage.removeItem('token'); 
    window.location.reload(); // Easiest way to force a redirect to login
  };

  return (
    // --- FIX 2 ---
    // The <Router> should wrap your entire application.
    <Router>
      <div className="App">
        
        {/* The Header is inside <Router> but *outside* <Routes>.
          This makes it appear on EVERY page. This is correct.
        */}
        <Header onLogout={handleLogout} />

        <Routes>
          {/* Public Routes */}
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          
          {/* Protected Route - This is a cleaner way to do it.
            It wraps your Dashboard component inside the ProtectedRoute.
          */}
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />

          {/* Fallback route if no other route matches */}
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
        
      </div>
    </Router>
  );
}

export default App;