// In frontend/src/components/ProtectedRoute.jsx

import React from 'react';
import { Navigate } from 'react-router-dom';

// This component now accepts "children" as a prop.
// "children" will be your <Dashboard /> component.
function ProtectedRoute({ children }) {

  // 1. Get the token from localStorage
  // Make sure 'token' is the *exact* name you used in your login function!
  const token = localStorage.getItem('token'); 

  // 2. Check if the token exists
  if (!token) {
    // 3. If no token, redirect to the login page
    return <Navigate to="/login" replace />;
  }

  // 4. If a token *does* exist, show the children (the <Dashboard />)
  return children;
}

export default ProtectedRoute;