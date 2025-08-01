import React, { useState, useEffect } from 'react';
import './App.css';
import VenuesModal from './VenuesModal';

const AppContent = ({ username, onLogout, isDarkMode, setIsDarkMode }) => {
  const [cityResults, setCityResults] = useState([]);
  const [savedDestinations, setSavedDestinations] = useState([]);
  const [message, setMessage] = useState('');
  const [travelerType, setTravelerType] = useState('solo');
  const [tripScope, setTripScope] = useState('international');
  const [budget, setBudget] = useState('any');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedCity, setSelectedCity] = useState(null);
  const [view, setView] = useState('search'); // 'search' or 'saved'

  const fetchSaved = async () => {
    const token = localStorage.getItem('token');
    if (!token) return;
    try {
      const response = await fetch('https://escape-genie.onrender.com/api/saved', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const data = await response.json();
      if (response.ok) {
        setSavedDestinations(data);
      }
    } catch (err) {
      console.error("Failed to fetch saved destinations", err);
    }
  };

  useEffect(() => {
    fetchSaved();
  }, []);

  const handleSave = async (destinationId, isSaved) => {
    const token = localStorage.getItem('token');
    const endpoint = isSaved ? `/api/saved/${destinationId}` : '/api/saved';
    const method = isSaved ? 'DELETE' : 'POST';

    try {
      const response = await fetch(`https://escape-genie.onrender.com${endpoint}`, {
        method: method,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: isSaved ? null : JSON.stringify({ destination_id: destinationId }),
      });

      if (response.ok) {
        fetchSaved(); // Re-fetch to update the state
      } else {
        const data = await response.json();
        alert(data.msg || 'An error occurred.');
      }
    } catch (err) {
      alert('Server error.');
    }
  };


  const handleSearch = async (e) => {
    e.preventDefault();
    if (!message.trim()) return;
    setIsLoading(true);
    setError('');
    setCityResults([]);
    setView('search');
    try {
      const response = await fetch('https://escape-genie.onrender.com/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message, travelerType, tripScope, budget }),
      });
      const data = await response.json();
      if (response.ok && data && data.length > 0) {
        setCityResults(data);
      } else {
        setError("No matching cities found. Try a different search.");
      }
    } catch (err) {
      setError("Failed to connect to the server. Is the backend running?");
    } finally {
      setIsLoading(false);
    }
  };

  const handleCityClick = (city) => {
    setSelectedCity(city);
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setSelectedCity(null);
  };

  const savedDestinationIds = new Set(savedDestinations.map(d => d.id));
  const resultsToDisplay = view === 'saved' ? savedDestinations : cityResults;

  return (
    <>
      <div className="app-container">
        <div className="results-panel">
          <div className="cities-header">
              <h2>{view === 'saved' ? 'My Saved Destinations' : 'Recommended Cities'}</h2>
              <button onClick={() => setView(view === 'search' ? 'saved' : 'search')} className="view-toggle-btn">
                  {view === 'search' ? 'View Saved' : '🤍'}
              </button>
          </div>
          {isLoading && <p>Finding the best cities for you...</p>}
          {error && <p className="error-message">{error}</p>}
          <div className="results-grid">
            {resultsToDisplay.map((city) => {
              const isSaved = savedDestinationIds.has(city.id);
              return (
                <div key={city.id} className="destination-card" >
                   <div className="card-content" onClick={() => handleCityClick(city)}>
                      <h3>{city.name}</h3>
                      <p>{city.description}</p>
                  </div>
                  <button onClick={() => handleSave(city.id, isSaved)} className={`save-btn ${isSaved ? 'saved' : ''}`}>
                      {isSaved ? '❤️' : '🤍'}
                  </button>
                </div>
              )
            })}
             {view === 'saved' && savedDestinations.length === 0 && (
                  <p>You haven't saved any destinations yet.</p>
              )}
          </div>
        </div>

        <div className="chat-panel">
          <div className="chat-panel-header">
            <div className="user-info">
              <span>Welcome, {username}!</span>
              <button onClick={onLogout}>Logout</button>
            </div>
            <button className="mode-toggle" onClick={() => setIsDarkMode(prev => !prev)} aria-label="Toggle theme">
              <div className="toggle-thumb">{isDarkMode ? '🌙' : '☀️'}</div>
            </button>
          </div>
          
          <div className="chat-greeting">
            <h1>Escape Genie</h1>
            <p>Find Your Ideal Destination</p>
          </div>
          
          <fieldset className="chat-fieldset">
            <div className="chat-filters">
              <div className="filter-group">
                <label>Who is traveling?</label>
                <select value={travelerType} onChange={(e) => setTravelerType(e.target.value)}>
                  <option value="solo">Solo</option>
                  <option value="couple">Couple</option>
                  <option value="family">Family</option>
                  <option value="student">Student</option>
                </select>
              </div>
              <div className="filter-group">
                <label>Trip Scope</label>
                <select value={tripScope} onChange={(e) => setTripScope(e.target.value)}>
                  <option value="international">International</option>
                  <option value="domestic">Domestic</option>
                </select>
              </div>
              <div className="filter-group">
                <label>Budget</label>
                <select value={budget} onChange={(e) => setBudget(e.target.value)}>
                  <option value="any">Any</option>
                  <option value="budget">Budget ($)</option>
                  <option value="mid-range">Mid-Range ($$)</option>
                  <option value="luxury">Luxury ($$$)</option>
                </select>
              </div>
            </div>

            <div className="chat-interface">
              <form onSubmit={handleSearch} className="chat-form">
                <input
                  type="text"
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  placeholder="e.g., a romantic trip to Italy..."
                />
                <button type="submit" disabled={isLoading}>
                  {isLoading ? 'Searching...' : 'Send'}
                </button>
              </form>
            </div>
          </fieldset>
        </div>
      </div>

      {isModalOpen && selectedCity && (
        <VenuesModal 
          city={selectedCity} 
          onClose={closeModal} 
          isDarkMode={isDarkMode} 
        />
      )}
    </>
  );
};

export default AppContent;