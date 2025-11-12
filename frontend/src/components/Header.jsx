// In frontend/src/components/Header.jsx

import React from 'react';
import './Header.css';
import logoUrl from '../components/assets/mce.jpeg'; // Our new, local logo

function Header({ onLogout }) { // Notice "onLogout" is received here
  return (
    <header className="main-header">
      
      {/* Left Side: Logo and College Title */}
      <div className="header-logo-container">
        <img src={logoUrl} alt="MCE Logo" className="header-logo" />
        <div className="header-title-block">
          <h1 className="college-name">Malnad College of Engineering</h1>
          <h2 className="department-name">Department of CSE - AIML</h2>
        </div>
      </div>

      {/* Center: App Title */}
      <div className="header-app-title">
        Legal AI Advisor
      </div>

      {/* Right Side: Logout Button */}
      <nav className="header-nav">
        <button onClick={onLogout} className="logout-button">
          Logout
        </button>
      </nav>

    </header>
  );
}

export default Header;