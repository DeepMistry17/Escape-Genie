Team
Deep Mistry
Hetvi Joshi
Kush Gohel
Prami Shah

# Escape Genie

Unlock Adventure, Discover Anywhere Instantly.

Escape Genie is a full-stack travel planning application that combines a React-based frontend with a Flask backend, enabling developers to create engaging, location-aware experiences. It features interactive maps, user authentication, and venue reviews, all designed for scalability and performance.

## Core Features

  * **Map Visualization**: Render interactive Google Maps with customizable markers and styling options.
  * **User Authentication**: Secure login, registration, and session management for personalized experiences.
  * **Performance Monitoring**: Collect web vitals metrics to optimize frontend responsiveness.
  * **Venue Exploration**: Discover city attractions with reviews, ratings, and map integration.
  * **Full-Stack Integration**: Seamless connection between React frontend and Flask backend for scalable deployment.

## Tech Stack

  * **Frontend**: React, React Google Maps API
  * **Backend**: Flask, Python, Spacy, SQLAlchemy
  * **Database**: PostgreSQL / SQLite

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed and configured:

  * **Node.js and npm**: For running the React frontend.
  * **Python and pip**: For running the Flask backend.
  * **API Keys**:
      * **Google Maps API Key**: For `REACT_APP_Maps_API_KEY`
      * **Geoapify API Key**: For `GEOAPIFY_API_KEY`
  * **Render Account** (Optional): For PostgreSQL hosting, or you can use a local SQLite database.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/DeepMistry17/Escape-Genie
    ```
2.  **Navigate to the project directory:**
    ```bash
    cd Escape-Genie
    ```

### Environment Variables

You will need to create `.env` files for both the frontend and backend.

**Frontend (`/frontend/.env`):**

```
REACT_APP_Maps_API_KEY=YOUR_GOOGLE_MAPS_API_KEY
```

**Backend (`/backend/.env`):**

```
GEOAPIFY_API_KEY=YOUR_GEOAPIFY_API_KEY
JWT_SECRET_KEY=YOUR_SUPER_SECRET_KEY
DATABASE_URL=YOUR_DATABASE_URL
```

*Note: For local development, you can omit the `DATABASE_URL` to use the default SQLite database.*

### Backend Setup

1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```
2.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Initialize the database:**
    ```bash
    python create_db.py
    ```
4.  **Run the backend server:**
    ```bash
    flask run
    ```
    The backend will be running at `http://localhost:5000`.

### Frontend Setup

1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```
2.  **Install the dependencies:**
    ```bash
    npm install
    ```
3.  **Run the frontend development server:**
    ```bash
    npm start
    ```
    The application will open in your browser at `http://localhost:3000`.

## Usage

Once both the frontend and backend servers are running, you can:

  * Register for a new account or log in with the default credentials (`testuser`/`password`).
  * Search for destinations based on your travel preferences.
  * View recommended cities and their locations on the map.
  * Save your favorite destinations.
  * Explore venues and add reviews for cities.

## Testing

  * **Frontend**: `npm test`
  * **Backend**: `pytest`
