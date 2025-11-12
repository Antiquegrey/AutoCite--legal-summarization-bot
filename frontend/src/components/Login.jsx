// In frontend/src/components/Login.jsx

import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
// You will want to style this. Make a Login.css file and import it.
// import './Login.css'; 

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate(); // Hook for redirecting

  const handleSubmit = async (e) => {
    e.preventDefault(); // Stop the form from refreshing the page

    try {
      const response = await fetch('http://127.0.0.1:8000/token', {
        method: 'POST',
        headers: {
          // --- CRITICAL PART 1 ---
          // FastAPI's OAuth2 form *requires* this content type
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        // And *this* data format
        body: new URLSearchParams({
          username: username,
          password: password,
        }),
      });

      if (!response.ok) {
        // If login failed (401, etc.)
        alert('Login failed: Incorrect username or password');
        return;
      }

      // If login was successful (200 OK)
      const data = await response.json();

      // --- CRITICAL PART 2 ---
      // 1. Save the token
      localStorage.setItem('token', data.access_token); 

      // 2. Redirect to the dashboard
      navigate('/');
      // --------------------------

    } catch (error) {
      console.error('Login error:', error);
      alert('An error occurred during login.');
    }
  };

  // --- This is the JSX that matches your screenshot ---
  // Make sure your form and inputs are linked to the state and submit function
  return (
    <div className="login-container">
      <div className="login-box">
        <h2>Login to Your Account</h2>
        <form onSubmit={handleSubmit}>
          <div className="input-group">
            <label htmlFor="username">Username</label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Username"
              required
            />
          </div>
          <div className="input-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Password"
              required
            />
          </div>
          <button type="submit" className="login-button">Login</button>
        </form>
        <div className="signup-link">
          Don't have an account? <Link to="/signup">Sign up</Link>
        </div>
      </div>
    </div>
  );
}

export default Login;