import React, { useState } from 'react';

// The component is now simpler, no longer a modal.
function Login({ onLoginSuccess, switchToRegister }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    
    try {
      const response = await fetch('http://127.0.0.1:5000/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      });
      const data = await response.json();

      if (response.ok) {
        onLoginSuccess(data.access_token, data.username);
      } else {
        setError(data.msg || 'Login failed.');
      }
    } catch (err) {
      setError('Server is not reachable.');
    }
  };

  return (
    <div className="auth-form-container">
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} placeholder="Username" required />
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" required />
        {error && <p className="error-message" style={{marginTop: '1rem'}}>{error}</p>}
        <button type="submit">Login</button>
      </form>
      <p className="switch-auth-text">
        Don't have an account? <button onClick={switchToRegister}>Register</button>
      </p>
    </div>
  );
}

export default Login;
