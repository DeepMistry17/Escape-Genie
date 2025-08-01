import React, { useState } from 'react';

// The component is now simpler, no longer a modal.
function Register({ onRegisterSuccess, switchToLogin }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (password.length < 5) {
      setError('Password must be at least 5 characters long.');
      return;
    }

    try {
      const response = await fetch('http://127.0.0.1:5000/api/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      });
      const data = await response.json();

      if (response.ok) {
        onRegisterSuccess();
      } else {
        setError(data.msg || 'Registration failed.');
      }
    } catch (err) {
      setError('Server is not reachable.');
    }
  };

  return (
    <div className="auth-form-container">
      <h2>Register</h2>
      <form onSubmit={handleSubmit}>
        <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} placeholder="Username" required />
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" required />
        {error && <p className="error-message" style={{marginTop: '1rem'}}>{error}</p>}
        <button type="submit">Create Account</button>
      </form>
       <p className="switch-auth-text">
        Already have an account? <button onClick={switchToLogin}>Login</button>
      </p>
    </div>
  );
}

export default Register;
