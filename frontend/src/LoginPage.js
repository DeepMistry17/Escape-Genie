import React, { useState } from 'react';
import Login from './Login';
import Register from './Register';
import './App.css'; // We will reuse some styles

function LoginPage({ onLoginSuccess }) {
  const [showLogin, setShowLogin] = useState(true);

  const handleRegisterSuccess = () => {
    setShowLogin(true); // Switch back to login form after a successful registration
    alert('Registration successful! Please log in.');
  };

  return (
    <div className="login-page-container">
      <div className="login-form-wrapper">
        <div className="login-greeting">
          <h1>Welcome to AI Travel Assistant</h1>
          <p>Your personal guide to the world awaits. Please log in or register to continue.</p>
        </div>
        {showLogin ? (
          <Login 
            onLoginSuccess={onLoginSuccess} 
            switchToRegister={() => setShowLogin(false)} 
          />
        ) : (
          <Register 
            onRegisterSuccess={handleRegisterSuccess} 
            switchToLogin={() => setShowLogin(true)} 
          />
        )}
      </div>
    </div>
  );
}

export default LoginPage;
