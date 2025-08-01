from flask import Flask, request, jsonify
from flask_cors import CORS
import spacy
import sqlite3
import os
from dotenv import load_dotenv
import requests
import urllib.parse
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager
import sqlalchemy

load_dotenv()
app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "your-super-secret-key-change-this" 
# Allow requests from your Render frontend and local development environment
origins = [
    "https://escape-genie-frontend.onrender.com",
    "http://localhost:3000"
]
CORS(app, resources={r"/api/*": {"origins": origins}})
jwt = JWTManager(app)

# --- Configuration & Setup ---
GEOAPIFY_API_KEY = os.getenv("GEOAPIFY_API_KEY")
DB_NAME = 'travel.db'
# We will "lazy-load" the model inside the /chat endpoint to ensure a fast and stable server startup.
nlp = None


SYNONYM_MAP = {"romantic": "romance", "historical": "history", "adventurous": "adventure", "relaxing": "relaxation", "cultural": "culture", "mountains": "mountain"}
STOP_WORDS = {"trip", "vacation", "holiday", "getaway", "journey", "tour", "destination", "place"}

def get_db_connection():
    db_url = os.environ.get('DATABASE_URL')
    if db_url:
        # Use PostgreSQL on Render
        engine = sqlalchemy.create_engine(db_url)
        conn = engine.connect()
    else:
        # Use SQLite for local development
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
    return conn

# --- Authentication Endpoints ---
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({"msg": "Username and password are required"}), 400
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    if user:
        conn.close()
        return jsonify({"msg": "Username already exists"}), 409
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
    conn.commit()
    conn.close()
    return jsonify({"msg": "User created successfully"}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({"msg": "Username and password are required"}), 400
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    if user and bcrypt.check_password_hash(user['password'], password):
        access_token = create_access_token(identity=str(user['id']))
        return jsonify(access_token=access_token, username=username)
    return jsonify({"msg": "Bad username or password"}), 401

# --- Main App Endpoints ---
# app.py

@app.route('/api/chat', methods=['POST'])
def chat():
    global nlp # Use the global nlp variable

    # Lazy load the model only if it hasn't been loaded yet
    if nlp is None:
        try:
            print("Loading SpaCy model for the first time...")
            nlp = spacy.load("en_core_web_sm")
            print("SpaCy model loaded successfully.")
        except IOError:
            print("Fatal: SpaCy model not found on server.")
            # Return a 503 Service Unavailable error if the model can't be loaded
            return jsonify({"error": "Language model is temporarily unavailable"}), 503

    data = request.json
    user_message, traveler_type, trip_scope, budget = data.get('message', ''), data.get('travelerType', 'solo'), data.get('tripScope', 'international'), data.get('budget', 'any')
    if not user_message: return jsonify([])

    doc = nlp(user_message.lower())
    search_terms = {SYNONYM_MAP.get(token.lemma_, token.lemma_) for token in doc if token.lemma_ not in STOP_WORDS}
    conn = get_db_connection()
    query = "SELECT * FROM destinations WHERE tags LIKE ? AND tags LIKE ?"
    params = [f"%{trip_scope}%", f"%{traveler_type}%"]
    if budget != 'any':
        query += " AND cost_tier = ?"
        params.append(budget)
    if search_terms:
        keyword_filters = " AND (" + " OR ".join(["tags LIKE ?"] * len(search_terms)) + ")"
        query += keyword_filters
        params.extend([f"%{term}%" for term in search_terms])
    query += " ORDER BY name LIMIT 30"
    results = conn.execute(query, tuple(params)).fetchall()
    conn.close()
    return jsonify([dict(row) for row in results])

def fetch_venues_by_category(lon, lat, categories, limit=10):
    places_url = f"https://api.geoapify.com/v2/places?categories={categories}&filter=circle:{lon},{lat},15000&bias=proximity:{lon},{lat}&limit={limit}&apiKey={GEOAPIFY_API_KEY}"
    try:
        response = requests.get(places_url)
        response.raise_for_status()
        features = response.json().get('features', [])
        venues = [{'id': prop.get('place_id'),'name': prop.get('name'),'address': prop.get('address_line2', 'Address not available'),'lon': coords[0],'lat': coords[1]} for venue in features if (prop := venue.get('properties', {})) and (coords := venue.get('geometry', {}).get('coordinates')) and prop.get('name')]
        return venues
    except requests.exceptions.RequestException as e:
        print(f"API call to Geoapify failed: {e}")
        return []

# --- CORRECTED get_venues function ---
@app.route('/api/venues', methods=['POST'])
def get_venues():
    data = request.json
    city = data.get('city', {})
    city_id, lat, lon = city.get('id'), city.get('lat'), city.get('lon')

    if not all([city_id, lat, lon]):
        return jsonify({"error": "City ID and coordinates are required"}), 400

    categorized_venues = {"attractions": [], "restaurants": []}
    
    def add_maps_url(venue):
        base_url = "https://www.google.com/maps/search/?api=1&query="
        # Prefer using name and address for a more accurate search
        if 'name' in venue and 'address' in venue and 'not available' not in venue.get('address', '').lower():
            search_query = f"{venue['name']}, {venue['address']}"
            venue['Maps_url'] = f"{base_url}{urllib.parse.quote_plus(search_query)}"
        # Fallback to coordinates if address is missing or invalid
        elif 'lat' in venue and 'lon' in venue:
            venue['Maps_url'] = f"{base_url}{venue['lat']},{venue['lon']}"
        return venue

    conn = get_db_connection()
    curated_results = conn.execute('SELECT * FROM landmarks WHERE destination_id = ?', (city_id,)).fetchall()
    conn.close()

    existing_venue_names = set()
    if curated_results:
        for landmark in curated_results:
            venue_data = add_maps_url(dict(landmark))
            category_key = f"{venue_data['category']}s"
            if category_key in categorized_venues:
                categorized_venues[category_key].append(venue_data)
                existing_venue_names.add(venue_data['name'].lower())

    if GEOAPIFY_API_KEY:
        api_attractions = fetch_venues_by_category(lon, lat, "tourism.sights")
        api_restaurants = fetch_venues_by_category(lon, lat, "catering.restaurant")

        for attraction in api_attractions:
            if attraction['name'].lower() not in existing_venue_names:
                categorized_venues["attractions"].append(add_maps_url(attraction))
        for restaurant in api_restaurants:
            if restaurant['name'].lower() not in existing_venue_names:
                categorized_venues["restaurants"].append(add_maps_url(restaurant))

    return jsonify(categorized_venues)
# app.py

@app.route('/api/saved', methods=['GET', 'POST'])
@jwt_required()
def handle_saved_destinations():
    current_user_id = get_jwt_identity()
    conn = get_db_connection()

    if request.method == 'POST':
        data = request.json
        destination_id = data.get('destination_id')
        if not destination_id:
            return jsonify({"msg": "Destination ID is required"}), 400

        # Check if already saved
        existing = conn.execute('SELECT id FROM saved_destinations WHERE user_id = ? AND destination_id = ?',
                                (current_user_id, destination_id)).fetchone()
        if existing:
            return jsonify({"msg": "Destination already saved"}), 409

        conn.execute('INSERT INTO saved_destinations (user_id, destination_id) VALUES (?, ?)',
                     (current_user_id, destination_id))
        conn.commit()
        conn.close()
        return jsonify({"msg": "Destination saved successfully"}), 201

    # GET request
    saved_query = """
        SELECT d.* FROM destinations d
        JOIN saved_destinations sd ON d.id = sd.destination_id
        WHERE sd.user_id = ?
    """
    saved = conn.execute(saved_query, (current_user_id,)).fetchall()
    conn.close()
    return jsonify([dict(row) for row in saved])


@app.route('/api/saved/<string:destination_id>', methods=['DELETE'])
@jwt_required()
def delete_saved_destination(destination_id):
    current_user_id = get_jwt_identity()
    conn = get_db_connection()
    conn.execute('DELETE FROM saved_destinations WHERE user_id = ? AND destination_id = ?',
                 (current_user_id, destination_id))
    conn.commit()
    conn.close()
    return jsonify({"msg": "Destination removed"}), 200

@app.route('/api/reviews/<string:destination_id>', methods=['GET'])
def get_reviews(destination_id):
    conn = get_db_connection()
    reviews = conn.execute(
        'SELECT * FROM reviews WHERE destination_id = ? ORDER BY timestamp DESC',
        (destination_id,)
    ).fetchall()
    conn.close()
    return jsonify([dict(row) for row in reviews])


@app.route('/api/reviews', methods=['POST'])
@jwt_required()
def add_review():
    current_user_id = get_jwt_identity()
    data = request.json
    destination_id = data.get('destination_id')
    rating = data.get('rating')
    comment = data.get('comment')
    username = data.get('username')

    if not all([destination_id, rating, username]):
        return jsonify({"msg": "Missing required fields"}), 400

    conn = get_db_connection()
    conn.execute(
        'INSERT INTO reviews (destination_id, user_id, rating, comment, username) VALUES (?, ?, ?, ?, ?)',
        (destination_id, current_user_id, rating, comment, username)
    )
    conn.commit()
    conn.close()

    return jsonify({"msg": "Review added successfully"}), 201

if __name__ == '__main__':
    # The 'port' line is important for hosting services
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)