import sqlite3

def create_and_populate_db():
    """
    Creates and populates the travel.db SQLite database.
    This script defines two tables:
    1. destinations: Contains all the travel destinations with a new 'cost_tier'.
    2. landmarks: Contains curated, must-see landmarks for each destination.
    """
    conn = sqlite3.connect('travel.db')
    cursor = conn.cursor()

    # --- Table 1: Destinations (with cost_tier added) ---
    cursor.execute('DROP TABLE IF EXISTS destinations')
    cursor.execute('''
    CREATE TABLE destinations (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        city TEXT NOT NULL,
        country TEXT NOT NULL,
        description TEXT,
        tags TEXT NOT NULL,
        lat REAL NOT NULL,
        lon REAL NOT NULL,
        cost_tier TEXT NOT NULL DEFAULT 'mid-range'
    )''')

    # --- Table 2: Curated Landmarks ---
    cursor.execute('DROP TABLE IF EXISTS landmarks')
    cursor.execute('''
    CREATE TABLE landmarks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        destination_id TEXT NOT NULL,
        name TEXT NOT NULL,
        category TEXT NOT NULL, -- 'attraction' or 'restaurant'
        address TEXT,
        lat REAL NOT NULL,
        lon REAL NOT NULL,
        FOREIGN KEY (destination_id) REFERENCES destinations (id)
    )''')

     # --- Table 3: Users ---
    cursor.execute('DROP TABLE IF EXISTS users')
    cursor.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )''')

    # --- Table 4: Saved Destinations ---
    cursor.execute('DROP TABLE IF EXISTS saved_destinations')
    cursor.execute('''
    CREATE TABLE saved_destinations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        destination_id TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (destination_id) REFERENCES destinations(id)
    )''')

     # --- Table 5: Reviews ---
    cursor.execute('DROP TABLE IF EXISTS reviews')
    cursor.execute('''
    CREATE TABLE reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        destination_id TEXT NOT NULL,
        user_id INTEGER NOT NULL,
        rating INTEGER NOT NULL,
        comment TEXT,
        username TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (destination_id) REFERENCES destinations (id),
        FOREIGN KEY (user_id) REFERENCES users (id)
    )''')

    # --- Data for 'destinations' Table (Your Full List with Cost Tiers) ---
    curated_data = [
        # --- India (Domestic) ---
        {'id': 'goa001', 'name': 'Goa', 'city': 'Goa', 'country': 'India', 'lat': 15.345, 'lon': 74.08, 'description': 'A coastal paradise known for its vibrant nightlife, serene beaches, and Portuguese heritage.', 'tags': 'beach,party,nightlife,relaxation,food,domestic,couple,student,family,solo', 'cost_tier': 'mid-range'},
        {'id': 'udai001', 'name': 'Udaipur, City of Lakes', 'city': 'Udaipur', 'country': 'India', 'lat': 24.5854, 'lon': 73.7125, 'description': 'An incredibly romantic city of shimmering lakes, magnificent palaces, and rich history.', 'tags': 'romance,history,luxury,lake,palace,domestic,couple,family,solo', 'cost_tier': 'luxury'},
        {'id': 'jai001', 'name': 'Jaipur, The Pink City', 'city': 'Jaipur', 'country': 'India', 'lat': 26.9124, 'lon': 75.7873, 'description': 'A vibrant city of majestic forts, royal palaces, and bustling markets rich in culture.', 'tags': 'history,culture,fort,palace,shopping,domestic,family,couple,solo', 'cost_tier': 'budget'},
        {'id': 'rish001', 'name': 'Rishikesh', 'city': 'Rishikesh', 'country': 'India', 'lat': 30.0869, 'lon': 78.2676, 'description': 'The yoga capital of the world, offering spiritual solace and thrilling adventures like river rafting.', 'tags': 'spiritual,yoga,adventure,mountain,nature,domestic,solo,student,couple,family', 'cost_tier': 'budget'},
        {'id': 'manali001', 'name': 'Manali', 'city': 'Manali', 'country': 'India', 'lat': 32.2432, 'lon': 77.1892, 'description': 'A Himalayan resort town offering snowy peaks, adventure sports, and serene natural beauty.', 'tags': 'mountain,adventure,hiking,skiing,nature,domestic,couple,student,solo,family', 'cost_tier': 'budget'},
        {'id': 'kera001', 'name': 'Kerala Backwaters', 'city': 'Alleppey', 'country': 'India', 'lat': 9.4981, 'lon': 76.3388, 'description': 'Cruise through a serene network of lagoons and lakes on a traditional houseboat.', 'tags': 'nature,relaxation,lake,backwater,domestic,family,couple,solo', 'cost_tier': 'mid-range'},
        {'id': 'darj001', 'name': 'Darjeeling', 'city': 'Darjeeling', 'country': 'India', 'lat': 27.0410, 'lon': 88.2627, 'description': 'Home to rolling tea plantations and panoramic views of the mighty Kanchenjunga peak.', 'tags': 'mountain,nature,tea,relaxation,domestic,couple,family,solo', 'cost_tier': 'budget'},
        {'id': 'ladakh001', 'name': 'Leh-Ladakh', 'city': 'Leh', 'country': 'India', 'lat': 34.1526, 'lon': 77.5771, 'description': 'A breathtaking high-altitude desert with dramatic landscapes and ancient monasteries.', 'tags': 'adventure,mountain,nature,spiritual,road-trip,domestic,solo,student,couple', 'cost_tier': 'mid-range'},
        {'id': 'varan001', 'name': 'Varanasi', 'city': 'Varanasi', 'country': 'India', 'lat': 25.3176, 'lon': 82.9739, 'description': 'A spiritual epicenter of India, one of the world\'s oldest living cities on the banks of the Ganges.', 'tags': 'spiritual,culture,history,domestic,solo,student,unesco', 'cost_tier': 'budget'},
        {'id': 'mumbai001', 'name': 'Mumbai', 'city': 'Mumbai', 'country': 'India', 'lat': 19.0760, 'lon': 72.8777, 'description': 'A bustling metropolis of dreams, known for Bollywood, colonial architecture, and vibrant street food.', 'tags': 'metropolis,sightseeing,food,party,shopping,domestic,family,couple,solo,student', 'cost_tier': 'mid-range'},
        {'id': 'delhi001', 'name': 'Delhi', 'city': 'Delhi', 'country': 'India', 'lat': 28.7041, 'lon': 77.1025, 'description': 'The heart of India, where ancient history and modern life blend seamlessly among monuments and markets.', 'tags': 'history,culture,food,shopping,metropolis,domestic,family,couple,solo,student', 'cost_tier': 'budget'},
        {'id': 'amrit001', 'name': 'Amritsar', 'city': 'Amritsar', 'country': 'India', 'lat': 31.6340, 'lon': 74.8723, 'description': 'Home to the magnificent Golden Temple, a serene and spiritual center for the Sikh faith.', 'tags': 'spiritual,history,culture,food,domestic,family,couple,solo', 'cost_tier': 'budget'},
        {'id': 'agra001', 'name': 'Agra', 'city': 'Agra', 'country': 'India', 'lat': 27.1767, 'lon': 78.0081, 'description': 'Home to the iconic Taj Mahal, a testament to eternal love and a wonder of the world.', 'tags': 'history,landmark,romance,sightseeing,unesco,domestic,family,couple,solo', 'cost_tier': 'budget'},
        {'id': 'jaisalmer001', 'name': 'Jaisalmer, The Golden City', 'city': 'Jaisalmer', 'country': 'India', 'lat': 26.9157, 'lon': 70.9083, 'description': 'A stunning sandstone city rising from the Thar Desert, known for its majestic fort and desert safaris.', 'tags': 'desert,history,fort,adventure,culture,domestic,couple,solo', 'cost_tier': 'budget'},
        {'id': 'andaman001', 'name': 'Andaman & Nicobar Islands', 'city': 'Port Blair', 'country': 'India', 'lat': 11.6234, 'lon': 92.7265, 'description': 'A tropical archipelago in the Bay of Bengal, with pristine beaches, coral reefs, and lush rainforests.', 'tags': 'beach,diving,nature,relaxation,adventure,domestic,couple,family,solo', 'cost_tier': 'mid-range'},
        {'id': 'coorg001', 'name': 'Coorg, Scotland of India', 'city': 'Coorg', 'country': 'India', 'lat': 12.3375, 'lon': 75.8069, 'description': 'A hilly region known for its sprawling coffee plantations, mist-covered hills, and stunning waterfalls.', 'tags': 'nature,relaxation,coffee,mountain,hiking,domestic,couple,family,solo', 'cost_tier': 'mid-range'},
        {'id': 'shillong001', 'name': 'Shillong', 'city': 'Shillong', 'country': 'India', 'lat': 25.5788, 'lon': 91.8933, 'description': 'Known as the "Scotland of the East," a beautiful hill station with rolling hills and crystal clear lakes.', 'tags': 'nature,lake,mountain,relaxation,road-trip,domestic,couple,family,solo', 'cost_tier': 'budget'},
        {'id': 'hampi001', 'name': 'Hampi', 'city': 'Hampi', 'country': 'India', 'lat': 15.3350, 'lon': 76.4600, 'description': 'An ancient village filled with the stunning ruins of the Vijayanagara Empire, a UNESCO World Heritage site.', 'tags': 'history,culture,ruin,sightseeing,unesco,domestic,solo,student,couple', 'cost_tier': 'budget'},
        {'id': 'jodhpur001', 'name': 'Jodhpur, The Blue City', 'city': 'Jodhpur', 'country': 'India', 'lat': 26.2389, 'lon': 73.0243, 'description': 'A historic city in the Thar Desert, famed for its blue buildings and the imposing Mehrangarh Fort.', 'tags': 'history,fort,culture,desert,domestic,family,couple,solo', 'cost_tier': 'budget'},
        {'id': 'spiti001', 'name': 'Spiti Valley', 'city': 'Kaza', 'country': 'India', 'lat': 32.2279, 'lon': 78.0731, 'description': 'A cold desert mountain valley in the Himalayas, known for its stark beauty, monasteries, and trekking routes.', 'tags': 'adventure,mountain,nature,spiritual,road-trip,hiking,domestic,solo,student', 'cost_tier': 'budget'},
        {'id': 'pondy001', 'name': 'Pondicherry', 'city': 'Pondicherry', 'country': 'India', 'lat': 11.9416, 'lon': 79.8083, 'description': 'A coastal town with a unique Franco-Tamil culture, known for its serene ashrams and colonial architecture.', 'tags': 'domestic,beach,spiritual,culture,relaxation,food,couple,solo,family', 'cost_tier': 'mid-range'},
        {'id': 'munnar001', 'name': 'Munnar', 'city': 'Munnar', 'country': 'India', 'lat': 10.0889, 'lon': 77.0595, 'description': 'A breathtaking hill station in the Western Ghats, famous for its emerald-green tea plantations.', 'tags': 'domestic,mountain,nature,tea,relaxation,hiking,couple,family', 'cost_tier': 'mid-range'},
        {'id': 'kolkata001', 'name': 'Kolkata, City of Joy', 'city': 'Kolkata', 'country': 'India', 'lat': 22.5726, 'lon': 88.3639, 'description': 'India\'s cultural capital, known for its grand colonial architecture, literary heritage, and vibrant street food.', 'tags': 'culture,history,food,metropolis,art,domestic,family,solo', 'cost_tier': 'budget'},
        {'id': 'ahmedabad001', 'name': 'Ahmedabad', 'city': 'Ahmedabad', 'country': 'India', 'lat': 23.0225, 'lon': 72.5714, 'description': 'A UNESCO World Heritage City famed for its Indo-Islamic architecture, textile industry, and Sabarmati Ashram.', 'tags': 'history,culture,unesco,architecture,food,domestic,family,solo', 'cost_tier': 'budget'},
        {'id': 'shimla001', 'name': 'Shimla', 'city': 'Shimla', 'country': 'India', 'lat': 31.1048, 'lon': 77.1734, 'description': 'The former summer capital of British India, this Himalayan hill station is known for its colonial architecture and scenic views.', 'tags': 'mountain,history,nature,relaxation,domestic,family,couple', 'cost_tier': 'mid-range'},
        {'id': 'mysore001', 'name': 'Mysore', 'city': 'Mysore', 'country': 'India', 'lat': 12.2958, 'lon': 76.6394, 'description': 'A city of palaces, most famously the grand Mysore Palace, and a center for yoga and sandalwood.', 'tags': 'history,palace,culture,yoga,domestic,family,couple', 'cost_tier': 'budget'},
        {'id': 'kutch001', 'name': 'Rann of Kutch', 'city': 'Bhuj', 'country': 'India', 'lat': 23.7313, 'lon': 69.8597, 'description': 'A vast salt marsh in the Thar Desert, famous for its surreal white landscape during the Rann Utsav festival.', 'tags': 'desert,nature,culture,festival,road-trip,domestic,solo,couple', 'cost_tier': 'mid-range'},
        {'id': 'gokarna001', 'name': 'Gokarna', 'city': 'Gokarna', 'country': 'India', 'lat': 14.5479, 'lon': 74.3188, 'description': 'A quieter alternative to Goa, this temple town offers pristine beaches and a laid-back, spiritual atmosphere.', 'tags': 'beach,spiritual,relaxation,temple,domestic,solo,student,couple', 'cost_tier': 'budget'},
        {'id': 'kaziranga001', 'name': 'Kaziranga National Park', 'city': 'Kaziranga', 'country': 'India', 'lat': 26.5775, 'lon': 93.3639, 'description': 'A UNESCO World Heritage site, home to two-thirds of the world\'s great one-horned rhinoceroses.', 'tags': 'nature,wildlife,safari,unesco,domestic,family,adventure', 'cost_tier': 'mid-range'},
        {'id': 'chennai001', 'name': 'Chennai', 'city': 'Chennai', 'country': 'India', 'lat': 13.0827, 'lon': 80.2707, 'description': 'A coastal metropolis known for its temples, beaches, and rich South Indian cultural and culinary traditions.', 'tags': 'metropolis,culture,food,beach,temple,domestic,family,business', 'cost_tier': 'budget'},
        {'id': 'bengaluru001', 'name': 'Bengaluru (Bangalore)', 'city': 'Bengaluru', 'country': 'India', 'lat': 12.9716, 'lon': 77.5946, 'description': 'Known as the "Silicon Valley of India," a bustling tech hub with vibrant parks, pubs, and a modern culture.', 'tags': 'metropolis,modern,party,food,tech,business,domestic,student,solo', 'cost_tier': 'mid-range'},
        {'id': 'hyderabad001', 'name': 'Hyderabad', 'city': 'Hyderabad', 'country': 'India', 'lat': 17.3850, 'lon': 78.4867, 'description': 'A city of pearls and Nizams, famous for historic sites like the Charminar and world-renowned biryani.', 'tags': 'history,culture,food,landmark,domestic,family,couple', 'cost_tier': 'budget'},

        # --- International - Asia & Oceania ---
        {'id': 'kyoto001', 'name': 'Kyoto', 'city': 'Kyoto', 'country': 'Japan', 'lat': 35.0116, 'lon': 135.7681, 'description': 'Experience traditional Japan in this city of classical temples, serene gardens, and graceful geishas.', 'tags': 'culture,history,nature,temple,food,international,solo,couple,family,unesco', 'cost_tier': 'luxury'},
        {'id': 'tokyo001', 'name': 'Tokyo', 'city': 'Tokyo', 'country': 'Japan', 'lat': 35.6762, 'lon': 139.6503, 'description': 'A dazzling megacity where ultramodern technology, pop culture, and ancient traditions collide.', 'tags': 'modern,food,culture,shopping,metropolis,sightseeing,international,family,solo,student', 'cost_tier': 'luxury'},
        {'id': 'bali001', 'name': 'Bali', 'city': 'Denpasar', 'country': 'Indonesia', 'lat': -8.6705, 'lon': 115.2126, 'description': 'An island paradise offering a perfect blend of spiritual culture, lush nature, and vibrant beach life.', 'tags': 'beach,nature,spiritual,relaxation,yoga,party,international,couple,solo,family,student', 'cost_tier': 'mid-range'},
        {'id': 'bkk001', 'name': 'Bangkok', 'city': 'Bangkok', 'country': 'Thailand', 'lat': 13.7563, 'lon': 100.5018, 'description': 'A city of contrasts with action at every turn, from ornate shrines to vibrant street life and modern malls.', 'tags': 'party,food,shopping,culture,temple,metropolis,international,student,solo,couple', 'cost_tier': 'budget'},
        {'id': 'phuket001', 'name': 'Phuket', 'city': 'Phuket', 'country': 'Thailand', 'lat': 7.8804, 'lon': 98.3923, 'description': 'Thailand’s largest island, offering stunning beaches, clear waters, and a lively party scene.', 'tags': 'beach,party,relaxation,diving,food,international,couple,student,family', 'cost_tier': 'mid-range'},
        {'id': 'singapore001', 'name': 'Singapore', 'city': 'Singapore', 'country': 'Singapore', 'lat': 1.3521, 'lon': 103.8198, 'description': 'A "City in a Garden," where stunning modern architecture blends with lush green spaces and a diverse food culture.', 'tags': 'modern,shopping,food,garden,family,international,luxury,couple,solo', 'cost_tier': 'luxury'},
        {'id': 'seoul001', 'name': 'Seoul', 'city': 'Seoul', 'country': 'South Korea', 'lat': 37.5665, 'lon': 126.9780, 'description': 'A dynamic metropolis where high-tech innovation and pop culture meet ancient palaces and temples.', 'tags': 'modern,food,shopping,culture,party,metropolis,international,student,solo,couple', 'cost_tier': 'mid-range'},
        {'id': 'siemreap001', 'name': 'Siem Reap', 'city': 'Siem Reap', 'country': 'Cambodia', 'lat': 13.3619, 'lon': 103.8606, 'description': 'The gateway to the magnificent ancient temple ruins of Angkor Wat, a wonder of the world.', 'tags': 'history,temple,culture,nature,sightseeing,unesco,international,solo,couple,family', 'cost_tier': 'budget'},
        {'id': 'beijing001', 'name': 'Beijing', 'city': 'Beijing', 'country': 'China', 'lat': 39.9042, 'lon': 116.4074, 'description': 'China’s sprawling capital, blending ancient imperial history with modern ambition at sites like the Forbidden City.', 'tags': 'history,culture,food,sightseeing,palace,unesco,international,family,solo', 'cost_tier': 'mid-range'},
        {'id': 'sydney001', 'name': 'Sydney', 'city': 'Sydney', 'country': 'Australia', 'lat': -33.8688, 'lon': 151.2093, 'description': 'Famous for its iconic Opera House and Harbour Bridge, offering a vibrant mix of city life and stunning beaches.', 'tags': 'beach,sightseeing,metropolis,party,nature,unesco,international,family,couple,student,solo', 'cost_tier': 'luxury'},
        {'id': 'hanoi001', 'name': 'Hanoi', 'city': 'Hanoi', 'country': 'Vietnam', 'lat': 21.0278, 'lon': 105.8342, 'description': 'A charming capital known for its centuries-old architecture, rich culture, and bustling Old Quarter.', 'tags': 'culture,history,food,lake,exotic,international,student,solo,couple', 'cost_tier': 'budget'},
        {'id': 'kathmandu001', 'name': 'Kathmandu', 'city': 'Kathmandu', 'country': 'Nepal', 'lat': 27.7172, 'lon': 85.3240, 'description': 'A spiritual city set in a valley surrounded by the Himalayan mountains, a hub for trekkers and adventurers.', 'tags': 'mountain,history,culture,temple,hiking,adventure,spiritual,unesco,international,solo,student', 'cost_tier': 'budget'},
        {'id': 'busan001', 'name': 'Busan', 'city': 'Busan', 'country': 'South Korea', 'lat': 35.1796, 'lon': 129.0756, 'description': 'A large port city in South Korea, known for its beautiful beaches, fresh seafood, and mountainside temples.', 'tags': 'beach,mountain,temple,food,city-trip,international,family,couple,solo', 'cost_tier': 'mid-range'},
        {'id': 'melbourne001', 'name': 'Melbourne', 'city': 'Melbourne', 'country': 'Australia', 'lat': -37.8136, 'lon': 144.9631, 'description': 'Renowned for its vibrant laneway culture, street art, exceptional coffee, and major sporting events.', 'tags': 'international,metropolis,art,culture,food,coffee,sports,student,solo,couple', 'cost_tier': 'luxury'},
        {'id': 'halong001', 'name': 'Ha Long Bay', 'city': 'Ha Long', 'country': 'Vietnam', 'lat': 20.9102, 'lon': 107.1839, 'description': 'Famous for its emerald waters and thousands of towering limestone islands topped with rainforests.', 'tags': 'international,nature,cruise,scenic,kayaking,relaxation,couple,family,sightseeing,unesco', 'cost_tier': 'mid-range'},
        {'id': 'shanghai001', 'name': 'Shanghai', 'city': 'Shanghai', 'country': 'China', 'lat': 31.2304, 'lon': 121.4737, 'description': 'A global financial hub famed for its futuristic skyline, historic Bund waterfront, and vibrant culinary scene.', 'tags': 'metropolis,modern,shopping,food,business,nightlife,international,family,couple', 'cost_tier': 'mid-range'},
        {'id': 'kl001', 'name': 'Kuala Lumpur', 'city': 'Kuala Lumpur', 'country': 'Malaysia', 'lat': 3.1390, 'lon': 101.6869, 'description': 'A bustling capital known for the iconic Petronas Twin Towers, colonial architecture, and a rich cultural melting pot.', 'tags': 'metropolis,modern,shopping,food,culture,sightseeing,international,family,couple', 'cost_tier': 'budget'},
        {'id': 'chiangmai001', 'name': 'Chiang Mai', 'city': 'Chiang Mai', 'country': 'Thailand', 'lat': 18.7883, 'lon': 98.9853, 'description': 'The cultural heart of northern Thailand, filled with historic temples, lush mountains, and ethical elephant sanctuaries.', 'tags': 'culture,temple,nature,relaxation,food,adventure,international,solo,couple,family', 'cost_tier': 'budget'},
        {'id': 'fiji001', 'name': 'Fiji', 'city': 'Nadi', 'country': 'Fiji', 'lat': -17.7813, 'lon': 177.4452, 'description': 'An archipelago of more than 300 islands, famed for its rugged landscapes, palm-lined beaches, and vibrant coral reefs.', 'tags': 'beach,romance,diving,relaxation,luxury,family,honeymoon,international', 'cost_tier': 'luxury'},
        {'id': 'uluru001', 'name': 'Uluru', 'city': 'Uluru', 'country': 'Australia', 'lat': -25.3444, 'lon': 131.0369, 'description': 'A massive sandstone monolith in the heart of the Australian Outback, sacred to Indigenous Australians.', 'tags': 'nature,spiritual,culture,desert,outback,sightseeing,unesco,international,solo,couple', 'cost_tier': 'mid-range'},
        {'id': 'osaka001', 'name': 'Osaka', 'city': 'Osaka', 'country': 'Japan', 'lat': 34.6937, 'lon': 135.5023, 'description': 'Japan\'s vibrant food capital, known for its electrifying nightlife, modern architecture, and historic castle.', 'tags': 'food,party,nightlife,culture,shopping,metropolis,international,student,solo', 'cost_tier': 'luxury'},
        {'id': 'hochiminh001', 'name': 'Ho Chi Minh City', 'city': 'Ho Chi Minh City', 'country': 'Vietnam', 'lat': 10.8231, 'lon': 106.6297, 'description': 'A bustling, dynamic city in southern Vietnam, known for its French colonial landmarks and Vietnam War history.', 'tags': 'metropolis,history,culture,food,party,international,student,solo', 'cost_tier': 'budget'},
        {'id': 'manila001', 'name': 'Manila', 'city': 'Manila', 'country': 'Philippines', 'lat': 14.5995, 'lon': 120.9842, 'description': 'The historic capital of the Philippines, a dense city of Spanish colonial architecture and modern skyscrapers.', 'tags': 'history,culture,metropolis,food,shopping,international,solo,family', 'cost_tier': 'budget'},
        {'id': 'boracay001', 'name': 'Boracay', 'city': 'Boracay', 'country': 'Philippines', 'lat': 11.9804, 'lon': 121.9189, 'description': 'A world-famous island known for its stunning white sand beaches, clear blue waters, and vibrant nightlife.', 'tags': 'beach,party,relaxation,diving,romance,international,couple,student', 'cost_tier': 'mid-range'},
        {'id': 'palawan001', 'name': 'Palawan', 'city': 'Puerto Princesa', 'country': 'Philippines', 'lat': 9.7392, 'lon': 118.7354, 'description': 'An archipelagic province known for its breathtaking seascapes, karst cliffs, and the underground river.', 'tags': 'nature,beach,diving,adventure,unesco,international,couple,solo', 'cost_tier': 'mid-range'},
        {'id': 'auckland001', 'name': 'Auckland', 'city': 'Auckland', 'country': 'New Zealand', 'lat': -36.8485, 'lon': 174.7633, 'description': 'New Zealand\'s largest city, centered around two large harbors and known for its vibrant culture and stunning nature.', 'tags': 'city-trip,sailing,nature,volcano,food,international,family,couple', 'cost_tier': 'luxury'},
        {'id': 'christchurch001', 'name': 'Christchurch', 'city': 'Christchurch', 'country': 'New Zealand', 'lat': -43.5321, 'lon': 172.6362, 'description': 'The "Garden City," known for its English heritage and resilience, rebuilding itself with innovative architecture.', 'tags': 'garden,culture,art,nature,city-trip,international,family,solo', 'cost_tier': 'luxury'},
        {'id': 'greatbarrier001', 'name': 'Great Barrier Reef', 'city': 'Cairns', 'country': 'Australia', 'lat': -18.2871, 'lon': 147.6992, 'description': 'The world\'s largest coral reef system, a breathtaking underwater world of incredible marine biodiversity.', 'tags': 'nature,diving,snorkeling,beach,unesco,international,family,couple', 'cost_tier': 'luxury'},
        {'id': 'perth001', 'name': 'Perth', 'city': 'Perth', 'country': 'Australia', 'lat': -31.9505, 'lon': 115.8605, 'description': 'A dynamic, sunny city on Australia\'s west coast, known for its beautiful beaches, wineries, and relaxed vibe.', 'tags': 'beach,relaxation,wine,nature,city-trip,international,family,solo', 'cost_tier': 'luxury'},
        {'id': 'xian001', 'name': 'Xi\'an', 'city': 'Xi\'an', 'country': 'China', 'lat': 34.3416, 'lon': 108.9398, 'description': 'An ancient capital of China, home to the world-famous Terracotta Army and the starting point of the Silk Road.', 'tags': 'history,culture,unesco,food,sightseeing,international,family,solo', 'cost_tier': 'mid-range'},
        {'id': 'luangprabang001', 'name': 'Luang Prabang', 'city': 'Luang Prabang', 'country': 'Laos', 'lat': 19.8856, 'lon': 102.1347, 'description': 'A tranquil UNESCO town of glistening temples, French colonial architecture, and spiritual saffron-robed monks.', 'tags': 'culture,spiritual,history,relaxation,unesco,international,solo,couple', 'cost_tier': 'budget'},
        {'id': 'pokhara001', 'name': 'Pokhara', 'city': 'Pokhara', 'country': 'Nepal', 'lat': 28.2096, 'lon': 83.9856, 'description': 'A beautiful lakeside city that serves as the gateway to the Annapurna trekking circuit in the Himalayas.', 'tags': 'lake,mountain,adventure,hiking,relaxation,nature,international,solo,student', 'cost_tier': 'budget'},
        {'id': 'paronepal001', 'name': 'Paro', 'city': 'Paro', 'country': 'Bhutan', 'lat': 27.4287, 'lon': 89.4169, 'description': 'Home to the iconic Tiger\'s Nest Monastery, this valley town is the spiritual heart of Bhutan.', 'tags': 'spiritual,mountain,hiking,culture,monastery,nature,international,solo,couple', 'cost_tier': 'luxury'},
        {'id': 'colombo001', 'name': 'Colombo', 'city': 'Colombo', 'country': 'Sri Lanka', 'lat': 6.9271, 'lon': 79.8612, 'description': 'A bustling coastal capital with a long history as a port on ancient trade routes, mixing colonial buildings with modern life.', 'tags': 'city-trip,history,culture,food,shopping,international,family,business', 'cost_tier': 'budget'},
        {'id': 'kandy001', 'name': 'Kandy', 'city': 'Kandy', 'country': 'Sri Lanka', 'lat': 7.2906, 'lon': 80.6337, 'description': 'A large city in central Sri Lanka, set on a plateau surrounded by mountains, home to the sacred Temple of the Tooth.', 'tags': 'culture,history,spiritual,temple,nature,unesco,international,family,couple', 'cost_tier': 'budget'},
        {'id': 'maldives001', 'name': 'Maldives', 'city': 'Malé', 'country': 'Maldives', 'lat': 4.1755, 'lon': 73.5093, 'description': 'A tropical nation of countless coral islands, known for its luxurious overwater bungalows, beaches, and blue lagoons.', 'tags': 'luxury,beach,romance,relaxation,diving,honeymoon,international,couple,family', 'cost_tier': 'luxury'},
        {'id': 'jeju001', 'name': 'Jeju Island', 'city': 'Jeju City', 'country': 'South Korea', 'lat': 33.4996, 'lon': 126.5312, 'description': 'A stunning volcanic island, famous for its beach resorts, scenic coastline, and a landscape of craters and lava tubes.', 'tags': 'nature,beach,hiking,volcano,romance,unesco,international,couple,family', 'cost_tier': 'mid-range'},
        {'id': 'jakarta001', 'name': 'Jakarta', 'city': 'Jakarta', 'country': 'Indonesia', 'lat': -6.2088, 'lon': 106.8456, 'description': 'The massive, bustling capital of Indonesia, a dynamic melting pot of cultures with a vibrant nightlife.', 'tags': 'metropolis,culture,food,party,shopping,business,international,solo', 'cost_tier': 'budget'},
        {'id': 'taipei001', 'name': 'Taipei', 'city': 'Taipei', 'country': 'Taiwan', 'lat': 25.0330, 'lon': 121.5654, 'description': 'A modern metropolis known for its lively street-food scene, bustling night markets, and the iconic Taipei 101 tower.', 'tags': 'modern,food,shopping,metropolis,night-market,international,solo,student', 'cost_tier': 'mid-range'},
        {'id': 'hongkong001', 'name': 'Hong Kong', 'city': 'Hong Kong', 'country': 'China', 'lat': 22.3193, 'lon': 114.1694, 'description': 'A vibrant and densely populated urban center, a major global financial hub with a world-class culinary scene.', 'tags': 'metropolis,shopping,food,modern,sightseeing,luxury,international,family,business', 'cost_tier': 'luxury'},
        {'id': 'phnompenh001', 'name': 'Phnom Penh', 'city': 'Phnom Penh', 'country': 'Cambodia', 'lat': 11.5564, 'lon': 104.9282, 'description': 'Cambodia\'s bustling capital, situated at the confluence of three rivers, rich in history and culture.', 'tags': 'history,culture,city-trip,international,solo', 'cost_tier': 'budget'},
        {'id': 'guilin001', 'name': 'Guilin', 'city': 'Guilin', 'country': 'China', 'lat': 25.2809, 'lon': 110.2872, 'description': 'Famed for its dramatic landscape of limestone karst hills and the picturesque Li River.', 'tags': 'nature,scenic,river,cruise,international,family,couple', 'cost_tier': 'mid-range'},
        {'id': 'tashkent001', 'name': 'Tashkent', 'city': 'Tashkent', 'country': 'Uzbekistan', 'lat': 41.2995, 'lon': 69.2401, 'description': 'The capital of Uzbekistan, a modern city with a blend of Soviet-era architecture and Islamic heritage.', 'tags': 'history,culture,architecture,international,solo', 'cost_tier': 'budget'},
        {'id': 'wellington001', 'name': 'Wellington', 'city': 'Wellington', 'country': 'New Zealand', 'lat': -41.2865, 'lon': 174.7762, 'description': 'New Zealand\'s cool little capital, known for its vibrant arts scene, cafe culture, and scenic harbour.', 'tags': 'culture,art,food,city-trip,international,solo,couple', 'cost_tier': 'luxury'},
        {'id': 'adelaide001', 'name': 'Adelaide', 'city': 'Adelaide', 'country': 'Australia', 'lat': -34.9285, 'lon': 138.6007, 'description': 'A charming city known for its vibrant food and wine scene, festivals, and proximity to the Barossa Valley.', 'tags': 'wine,food,culture,festival,international,couple,family', 'cost_tier': 'luxury'},

        # --- International - Europe ---
        {'id': 'paris001', 'name': 'Paris', 'city': 'Paris', 'country': 'France', 'lat': 48.8566, 'lon': 2.3522, 'description': 'The iconic "City of Love," celebrated for its world-class art, fashion, gastronomy, and historic landmarks.', 'tags': 'romance,art,luxury,food,history,sightseeing,unesco,international,couple,family,solo,student', 'cost_tier': 'luxury'},
        {'id': 'rome001', 'name': 'Rome', 'city': 'Rome', 'country': 'Italy', 'lat': 41.9028, 'lon': 12.4964, 'description': 'A city steeped in 3,000 years of history, from the ancient Colosseum to the splendor of the Vatican.', 'tags': 'history,art,culture,food,sightseeing,unesco,international,couple,family,solo,student', 'cost_tier': 'mid-range'},
        {'id': 'london001', 'name': 'London', 'city': 'London', 'country': 'UK', 'lat': 51.5074, 'lon': -0.1278, 'description': 'A global hub of history, culture, and finance, where royal tradition meets modern energy.', 'tags': 'history,culture,sightseeing,shopping,metropolis,art,international,family,couple,student,solo', 'cost_tier': 'luxury'},
        {'id': 'barca001', 'name': 'Barcelona', 'city': 'Barcelona', 'country': 'Spain', 'lat': 41.3851, 'lon': 2.1734, 'description': 'A masterpiece of architectural wonders by Gaudí, combined with sun-soaked beaches and a vibrant culinary scene.', 'tags': 'art,architecture,party,beach,food,international,couple,student,solo,family', 'cost_tier': 'mid-range'},
        {'id': 'amsterdam001', 'name': 'Amsterdam', 'city': 'Amsterdam', 'country': 'Netherlands', 'lat': 52.3676, 'lon': 4.9041, 'description': 'A charming city of elaborate canals, artistic heritage, and a vibrant, open-minded culture.', 'tags': 'culture,art,history,canal,party,city-trip,international,student,solo,couple', 'cost_tier': 'luxury'},
        {'id': 'prague001', 'name': 'Prague', 'city': 'Prague', 'country': 'Czech Republic', 'lat': 50.0755, 'lon': 14.4378, 'description': 'A fairytale city of a hundred spires, with a medieval Old Town Square and the historic Charles Bridge.', 'tags': 'history,culture,architecture,romance,castle,unesco,international,couple,student,solo', 'cost_tier': 'budget'},
        {'id': 'venice001', 'name': 'Venice', 'city': 'Venice', 'country': 'Italy', 'lat': 45.4408, 'lon': 12.3155, 'description': 'A unique and timelessly romantic city of canals, gondolas, and magnificent Renaissance architecture.', 'tags': 'romance,history,art,culture,sightseeing,unesco,international,couple,solo', 'cost_tier': 'luxury'},
        {'id': 'santorini001', 'name': 'Santorini', 'city': 'Fira', 'country': 'Greece', 'lat': 36.3932, 'lon': 25.4615, 'description': 'A breathtaking volcanic island known for its cliffside white-washed villages and dramatic sunsets over the Aegean Sea.', 'tags': 'romance,beach,luxury,relaxation,sightseeing,international,couple,honeymoon', 'cost_tier': 'luxury'},
        {'id': 'interlaken001', 'name': 'Interlaken', 'city': 'Interlaken', 'country': 'Switzerland', 'lat': 46.6863, 'lon': 7.8632, 'description': 'Nestled between two emerald lakes, this town is the ultimate gateway for alpine adventures and stunning hikes.', 'tags': 'mountain,adventure,nature,hiking,lake,international,solo,student,couple', 'cost_tier': 'luxury'},
        {'id': 'zermatt001', 'name': 'Zermatt', 'city': 'Zermatt', 'country': 'Switzerland', 'lat': 46.0207, 'lon': 7.7491, 'description': 'A charming, car-free village at the foot of the iconic Matterhorn, a paradise for skiing, climbing, and hiking.', 'tags': 'mountain,skiing,hiking,adventure,luxury,nature,international,couple,family,solo', 'cost_tier': 'luxury'},
        {'id': 'reykjavik001', 'name': 'Reykjavik', 'city': 'Reykjavik', 'country': 'Iceland', 'lat': 64.1466, 'lon': -21.9426, 'description': 'The gateway to Iceland\'s otherworldly landscapes of glaciers, geysers, and the magical Northern Lights.', 'tags': 'nature,adventure,northern-lights,lagoons,road-trip,international,solo,student,couple', 'cost_tier': 'luxury'},
        {'id': 'florence001', 'name': 'Florence', 'city': 'Florence', 'country': 'Italy', 'lat': 43.7696, 'lon': 11.2558, 'description': 'The birthplace of the Renaissance, a city that is a living museum of art and architectural masterpieces.', 'tags': 'art,history,culture,romance,food,architecture,unesco,international,couple,solo,family', 'cost_tier': 'mid-range'},
        {'id': 'lisbon001', 'name': 'Lisbon', 'city': 'Lisbon', 'country': 'Portugal', 'lat': 38.7223, 'lon': -9.1393, 'description': 'A coastal capital of colorful tiled buildings, historic trams, and melancholic Fado music.', 'tags': 'history,culture,food,coast,city-trip,international,couple,solo,student', 'cost_tier': 'budget'},
        {'id': 'budapest001', 'name': 'Budapest', 'city': 'Budapest', 'country': 'Hungary', 'lat': 47.4979, 'lon': 19.0402, 'description': 'The "Pearl of the Danube," known for its stunning parliament building, historic thermal baths, and vibrant ruin bars.', 'tags': 'history,culture,thermal-baths,architecture,party,international,student,couple,solo', 'cost_tier': 'budget'},
        {'id': 'edinburgh001', 'name': 'Edinburgh', 'city': 'Edinburgh', 'country': 'Scotland', 'lat': 55.9533, 'lon': -3.1883, 'description': 'A historic capital with a medieval Old Town and the iconic Edinburgh Castle perched on a dormant volcano.', 'tags': 'history,culture,castle,architecture,hiking,unesco,international,family,couple,solo', 'cost_tier': 'mid-range'},
        {'id': 'dublin001', 'name': 'Dublin', 'city': 'Dublin', 'country': 'Ireland', 'lat': 53.3498, 'lon': -6.2603, 'description': 'A vibrant capital city known for its rich literary history, friendly pubs, and the Guinness brewery.', 'tags': 'history,culture,pub,music,city-trip,international,student,solo,couple', 'cost_tier': 'mid-range'},
        {'id': 'berlin001', 'name': 'Berlin', 'city': 'Berlin', 'country': 'Germany', 'lat': 52.5200, 'lon': 13.4050, 'description': 'A city defined by its intense history, avant-garde art scene, and energetic nightlife.', 'tags': 'history,art,party,culture,modern,international,student,solo,couple', 'cost_tier': 'mid-range'},
        {'id': 'moscow001', 'name': 'Moscow', 'city': 'Moscow', 'country': 'Russia', 'lat': 55.7558, 'lon': 37.6173, 'description': 'Home to the iconic Kremlin and Red Square, Russia’s capital is a city of grand, opulent architecture.', 'tags': 'history,culture,art,architecture,sightseeing,unesco,international,family,couple', 'cost_tier': 'mid-range'},
        {'id': 'istanbul001', 'name': 'Istanbul', 'city': 'Istanbul', 'country': 'Turkey', 'lat': 41.0082, 'lon': 28.9784, 'description': 'Where East meets West, a city of stunning mosques, bustling bazaars, and rich imperial history.', 'tags': 'international,history,culture,food,shopping,mosque,sightseeing,couple,solo,family', 'cost_tier': 'budget'},
        {'id': 'dubrovnik001', 'name': 'Dubrovnik', 'city': 'Dubrovnik', 'country': 'Croatia', 'lat': 42.6507, 'lon': 18.0944, 'description': 'The "Pearl of the Adriatic," an ancient walled city with stunning sea views and historic charm.', 'tags': 'international,history,beach,coast,sailing,sightseeing,unesco,couple,family,romance', 'cost_tier': 'mid-range'},
        {'id': 'vienna001', 'name': 'Vienna', 'city': 'Vienna', 'country': 'Austria', 'lat': 48.2082, 'lon': 16.3738, 'description': 'An imperial city of palaces, classical music, and artistic legacies from Mozart, Beethoven, and Freud.', 'tags': 'history,culture,art,music,palace,luxury,unesco,international,couple,family', 'cost_tier': 'luxury'},
        {'id': 'munich001', 'name': 'Munich', 'city': 'Munich', 'country': 'Germany', 'lat': 48.1351, 'lon': 11.5820, 'description': 'The capital of Bavaria, famous for its annual Oktoberfest, beautiful parks, and grand museums.', 'tags': 'culture,festival,beer,history,art,party,international,student,couple', 'cost_tier': 'mid-range'},
        {'id': 'madrid001', 'name': 'Madrid', 'city': 'Madrid', 'country': 'Spain', 'lat': 40.4168, 'lon': -3.7038, 'description': 'Spain\'s central capital, a city of elegant boulevards, manicured parks, and rich repositories of European art.', 'tags': 'art,culture,food,party,nightlife,history,international,couple,solo', 'cost_tier': 'mid-range'},
        {'id': 'copenhagen001', 'name': 'Copenhagen', 'city': 'Copenhagen', 'country': 'Denmark', 'lat': 55.6761, 'lon': 12.5683, 'description': 'A cool and compact capital known for its high-end design, cycling culture, and the magical Tivoli Gardens.', 'tags': 'culture,design,food,city-trip,family,international,couple', 'cost_tier': 'luxury'},
        {'id': 'krakow001', 'name': 'Kraków', 'city': 'Kraków', 'country': 'Poland', 'lat': 50.0647, 'lon': 19.9450, 'description': 'A beautifully preserved medieval city with a stunning market square and a poignant history.', 'tags': 'history,culture,architecture,budget,unesco,student,international,solo,couple', 'cost_tier': 'budget'},
        {'id': 'amalfi001', 'name': 'Amalfi Coast', 'city': 'Amalfi', 'country': 'Italy', 'lat': 40.6346, 'lon': 14.6027, 'description': 'A stunning stretch of coastline featuring sheer cliffs, a rugged shoreline, and pastel-colored fishing villages.', 'tags': 'romance,luxury,beach,coast,food,scenic,road-trip,unesco,international,couple', 'cost_tier': 'luxury'},
        {'id': 'bergen001', 'name': 'Bergen & Norwegian Fjords', 'city': 'Bergen', 'country': 'Norway', 'lat': 60.3913, 'lon': 5.3221, 'description': 'The gateway to Norway\'s majestic fjords, a city surrounded by mountains and breathtaking natural beauty.', 'tags': 'nature,fjord,hiking,scenic,cruise,adventure,unesco,international,family,solo', 'cost_tier': 'luxury'},
        {'id': 'athens001', 'name': 'Athens', 'city': 'Athens', 'country': 'Greece', 'lat': 37.9838, 'lon': 23.7275, 'description': 'The cradle of Western civilization, home to ancient landmarks like the Acropolis and a vibrant modern city.', 'tags': 'history,culture,art,philosophy,ruin,unesco,international,family,solo', 'cost_tier': 'budget'},
        {'id': 'stockholm001', 'name': 'Stockholm', 'city': 'Stockholm', 'country': 'Sweden', 'lat': 59.3293, 'lon': 18.0686, 'description': 'A stunning capital built on 14 islands, known for its charming Old Town (Gamla Stan), museums, and modern design.', 'tags': 'culture,history,design,archipelago,city-trip,international,family,couple', 'cost_tier': 'luxury'},
        {'id': 'helsinki001', 'name': 'Helsinki', 'city': 'Helsinki', 'country': 'Finland', 'lat': 60.1699, 'lon': 24.9384, 'description': 'A vibrant seaside city of stunning design and architecture, with beautiful islands and great green urban areas.', 'tags': 'design,architecture,nature,sea,sauna,international,couple,solo', 'cost_tier': 'luxury'},
        {'id': 'brussels001', 'name': 'Brussels', 'city': 'Brussels', 'country': 'Belgium', 'lat': 50.8503, 'lon': 4.3517, 'description': 'The capital of the European Union, famous for its Grand-Place, comic strip art, chocolates, and beer.', 'tags': 'culture,history,food,beer,politics,international,city-trip,couple', 'cost_tier': 'mid-range'},
        {'id': 'geneva001', 'name': 'Geneva', 'city': 'Geneva', 'country': 'Switzerland', 'lat': 46.2044, 'lon': 6.1432, 'description': 'A global city of diplomacy and banking, set on a beautiful lake with a backdrop of the Alps.', 'tags': 'lake,mountain,luxury,business,nature,international,couple,family', 'cost_tier': 'luxury'},
        {'id': 'nice001', 'name': 'Nice', 'city': 'Nice', 'country': 'France', 'lat': 43.7102, 'lon': 7.2620, 'description': 'The vibrant heart of the French Riviera, offering stunning beaches, a charming old town, and a rich artistic heritage.', 'tags': 'beach,luxury,art,culture,relaxation,international,couple,family', 'cost_tier': 'luxury'},
        {'id': 'seville001', 'name': 'Seville', 'city': 'Seville', 'country': 'Spain', 'lat': 37.3891, 'lon': -5.9845, 'description': 'The heart of Andalusia, the birthplace of flamenco, known for its historic landmarks and vibrant festivals.', 'tags': 'culture,history,flamenco,architecture,food,romance,international,couple,solo', 'cost_tier': 'mid-range'},
        {'id': 'porto001', 'name': 'Porto', 'city': 'Porto', 'country': 'Portugal', 'lat': 41.1579, 'lon': -8.6291, 'description': 'A charming coastal city famous for its stately bridges, port wine production, and medieval Ribeira district.', 'tags': 'wine,history,culture,river,food,unesco,international,couple,solo', 'cost_tier': 'budget'},
        {'id': 'hamburg001', 'name': 'Hamburg', 'city': 'Hamburg', 'country': 'Germany', 'lat': 53.5511, 'lon': 9.9937, 'description': 'Germany\'s "Gateway to the World," a major port city with numerous canals and a futuristic concert hall.', 'tags': 'port,canal,architecture,music,nightlife,international,city-trip', 'cost_tier': 'mid-range'},
        {'id': 'warsaw001', 'name': 'Warsaw', 'city': 'Warsaw', 'country': 'Poland', 'lat': 52.2297, 'lon': 21.0122, 'description': 'Poland\'s resilient capital, a city that has risen from the ashes with a meticulously reconstructed Old Town.', 'tags': 'history,culture,modern,city-trip,international,student,solo', 'cost_tier': 'budget'},
        {'id': 'oslo001', 'name': 'Oslo', 'city': 'Oslo', 'country': 'Norway', 'lat': 59.9139, 'lon': 10.7522, 'description': 'Norway\'s capital, a city of green spaces and museums, including the Munch Museum and Viking Ship Museum.', 'tags': 'nature,art,museum,culture,fjord,international,family,couple', 'cost_tier': 'luxury'},
        {'id': 'mykonos001', 'name': 'Mykonos', 'city': 'Mykonos', 'country': 'Greece', 'lat': 37.4467, 'lon': 25.3289, 'description': 'A cosmopolitan Greek island famous for its vibrant nightlife, picturesque windmills, and beautiful beaches.', 'tags': 'party,nightlife,beach,luxury,lgbt,international,couple,student', 'cost_tier': 'luxury'},
        {'id': 'valencia001', 'name': 'Valencia', 'city': 'Valencia', 'country': 'Spain', 'lat': 39.4699, 'lon': -0.3763, 'description': 'Home of paella, this vibrant Spanish city boasts futuristic architecture, a wide beach, and a thriving cultural scene.', 'tags': 'food,architecture,beach,culture,family,international,city-trip', 'cost_tier': 'mid-range'},
        {'id': 'stpetersburg001', 'name': 'Saint Petersburg', 'city': 'Saint Petersburg', 'country': 'Russia', 'lat': 59.9311, 'lon': 30.3609, 'description': 'Russia\'s cultural heart, famed for its grand imperial palaces, the State Hermitage Museum, and romantic canals.', 'tags': 'art,history,culture,palace,museum,unesco,international,couple,family', 'cost_tier': 'mid-range'},
        {'id': 'bruges001', 'name': 'Bruges', 'city': 'Bruges', 'country': 'Belgium', 'lat': 51.2093, 'lon': 3.2247, 'description': 'A fairytale medieval town with picturesque canals, cobbled streets, and stunning architecture.', 'tags': 'history,romance,architecture,canal,unesco,international,couple,family', 'cost_tier': 'mid-range'},
        {'id': 'salzburg001', 'name': 'Salzburg', 'city': 'Salzburg', 'country': 'Austria', 'lat': 47.8095, 'lon': 13.0550, 'description': 'Birthplace of Mozart and setting for "The Sound of Music," this city is famed for its baroque architecture.', 'tags': 'music,history,culture,architecture,unesco,international,family,couple', 'cost_tier': 'luxury'},
        {'id': 'lucerne001', 'name': 'Lucerne', 'city': 'Lucerne', 'country': 'Switzerland', 'lat': 47.0502, 'lon': 8.3093, 'description': 'A picturesque city in central Switzerland, known for its medieval architecture and stunning lakeside setting.', 'tags': 'lake,mountain,history,scenic,relaxation,international,family,couple', 'cost_tier': 'luxury'},
        {'id': 'ibiza001', 'name': 'Ibiza', 'city': 'Ibiza', 'country': 'Spain', 'lat': 38.9067, 'lon': 1.4206, 'description': 'A world-renowned destination for nightlife and electronic music, with beautiful beaches and a bohemian vibe.', 'tags': 'party,nightlife,beach,music,bohemian,international,student,couple', 'cost_tier': 'luxury'},
        {'id': 'frankfurt001', 'name': 'Frankfurt', 'city': 'Frankfurt', 'country': 'Germany', 'lat': 50.1109, 'lon': 8.6821, 'description': 'A major financial hub with a futuristic skyline, contrasted with a charming old town square (Römerberg).', 'tags': 'business,modern,history,city-trip,international,solo', 'cost_tier': 'mid-range'},
        {'id': 'lyon001', 'name': 'Lyon', 'city': 'Lyon', 'country': 'France', 'lat': 45.7640, 'lon': 4.8357, 'description': 'Considered the gastronomic capital of France, known for its historic old town and vibrant culinary scene.', 'tags': 'food,culture,history,unesco,international,couple,solo', 'cost_tier': 'mid-range'},
        {'id': 'split001', 'name': 'Split', 'city': 'Split', 'country': 'Croatia', 'lat': 43.5081, 'lon': 16.4402, 'description': 'A bustling city on the Dalmatian Coast, known for the ancient Diocletian\'s Palace and vibrant seaside promenade.', 'tags': 'history,beach,port,sailing,unesco,international,couple,student', 'cost_tier': 'mid-range'},
        {'id': 'bologna001', 'name': 'Bologna', 'city': 'Bologna', 'country': 'Italy', 'lat': 44.4949, 'lon': 11.3426, 'description': 'A historic university city known for its rich culinary traditions, beautiful arcades, and medieval towers.', 'tags': 'food,history,culture,university,international,solo,couple', 'cost_tier': 'mid-range'},
        {'id': 'glasgow001', 'name': 'Glasgow', 'city': 'Glasgow', 'country': 'Scotland', 'lat': 55.8642, 'lon': -4.2518, 'description': 'A vibrant city famed for its Victorian and art nouveau architecture, a thriving music scene, and friendly locals.', 'tags': 'music,art,culture,architecture,international,student,solo', 'cost_tier': 'mid-range'},
        {'id': 'tallinn001', 'name': 'Tallinn', 'city': 'Tallinn', 'country': 'Estonia', 'lat': 59.4370, 'lon': 24.7536, 'description': 'A beautifully preserved medieval city with a charming Old Town, combined with a modern, tech-savvy culture.', 'tags': 'history,medieval,unesco,tech,international,solo,couple', 'cost_tier': 'budget'},
        {'id': 'riga001', 'name': 'Riga', 'city': 'Riga', 'country': 'Latvia', 'lat': 56.9496, 'lon': 24.1052, 'description': 'The largest city in the Baltics, celebrated for its extensive Art Nouveau architecture and historic Old Town.', 'tags': 'architecture,art,history,unesco,international,solo,couple', 'cost_tier': 'budget'},
        {'id': 'vilnius001', 'name': 'Vilnius', 'city': 'Vilnius', 'country': 'Lithuania', 'lat': 54.6872, 'lon': 25.2797, 'description': 'Known for its baroque architecture in the medieval Old Town, a city with a quirky and artistic soul.', 'tags': 'history,art,baroque,unesco,international,solo,couple', 'cost_tier': 'budget'},
        {'id': 'ljubljana001', 'name': 'Ljubljana', 'city': 'Ljubljana', 'country': 'Slovenia', 'lat': 46.0569, 'lon': 14.5058, 'description': 'A charming and green capital, with a picturesque river, a hilltop castle, and a lively cafe culture.', 'tags': 'green-city,culture,castle,river,international,couple,family', 'cost_tier': 'mid-range'},

        # --- International - Americas ---
        {'id': 'nyc001', 'name': 'New York City', 'city': 'New York', 'country': 'USA', 'lat': 40.7128, 'lon': -74.0060, 'description': 'The "City That Never Sleeps," an iconic center of art, theatre, food, and boundless energy.', 'tags': 'metropolis,sightseeing,shopping,art,food,party,international,couple,family,student,solo', 'cost_tier': 'luxury'},
        {'id': 'queen001', 'name': 'Queenstown', 'city': 'Queenstown', 'country': 'New Zealand', 'lat': -45.0312, 'lon': 168.6626, 'description': 'The adventure capital of the world, set against a backdrop of majestic mountains and crystal-clear lakes.', 'tags': 'adventure,mountain,nature,hiking,skiing,lake,international,solo,student,couple,family', 'cost_tier': 'luxury'},
        {'id': 'machupicchu001', 'name': 'Machu Picchu', 'city': 'Aguas Calientes', 'country': 'Peru', 'lat': -13.1631, 'lon': -72.5450, 'description': 'An ancient Incan citadel set high in the Andes Mountains, renowned for its astronomical alignments and panoramic views.', 'tags': 'history,adventure,mountain,nature,sightseeing,spiritual,international,solo,couple,unesco', 'cost_tier': 'mid-range'},
        {'id': 'galapagos001', 'name': 'Galapagos Islands', 'city': 'Baltra', 'country': 'Ecuador', 'lat': -0.8283, 'lon': -90.2801, 'description': 'A volcanic archipelago renowned for its fearless wildlife and as the source of Darwin\'s theory of evolution.', 'tags': 'nature,wildlife,adventure,beach,diving,unesco,international,family,solo,couple', 'cost_tier': 'luxury'},
        {'id': 'havana001', 'name': 'Havana', 'city': 'Havana', 'country': 'Cuba', 'lat': 23.1136, 'lon': -82.3666, 'description': 'A city frozen in time, with vintage cars, colorful colonial architecture, and an infectious rhythm of music and dance.', 'tags': 'history,culture,music,exotic,city-trip,unesco,international,couple,solo,student', 'cost_tier': 'budget'},
        {'id': 'rio001', 'name': 'Rio de Janeiro', 'city': 'Rio de Janeiro', 'country': 'Brazil', 'lat': -22.9068, 'lon': -43.1729, 'description': 'A city of breathtaking beauty, from the heights of Christ the Redeemer to the sands of Copacabana beach.', 'tags': 'beach,party,nature,mountain,sightseeing,unesco,international,couple,student,solo', 'cost_tier': 'mid-range'},
        {'id': 'vancouver001', 'name': 'Vancouver', 'city': 'Vancouver', 'country': 'Canada', 'lat': 49.2827, 'lon': -123.1207, 'description': 'A city where the mountains meet the sea, offering a perfect balance of urban life and outdoor adventure.', 'tags': 'mountain,nature,city-trip,food,hiking,adventure,international,family,couple,solo', 'cost_tier': 'luxury'},
        {'id': 'banff001', 'name': 'Banff National Park', 'city': 'Banff', 'country': 'Canada', 'lat': 51.1784, 'lon': -115.5708, 'description': 'Canada\'s oldest national park, known for its turquoise glacial lakes, towering peaks, and abundant wildlife.', 'tags': 'nature,mountain,lake,hiking,adventure,wildlife,unesco,international,family,couple,solo', 'cost_tier': 'luxury'},
        {'id': 'yosemite001', 'name': 'Yosemite National Park', 'city': 'Yosemite Valley', 'country': 'USA', 'lat': 37.8651, 'lon': -119.5383, 'description': 'Famed for its giant sequoia trees and the iconic vistas of El Capitan and Half Dome.', 'tags': 'park,nature,mountain,hiking,adventure,road-trip,unesco,international,family,couple,solo', 'cost_tier': 'mid-range'},
        {'id': 'vegas001', 'name': 'Las Vegas', 'city': 'Las Vegas', 'country': 'USA', 'lat': 36.1699, 'lon': -115.1398, 'description': 'A resort city famed for its vibrant nightlife, 24-hour casinos, and spectacular entertainment.', 'tags': 'party,entertainment,luxury,shopping,metropolis,international,couple,student,solo', 'cost_tier': 'mid-range'},
        {'id': 'buenosaires001', 'name': 'Buenos Aires', 'city': 'Buenos Aires', 'country': 'Argentina', 'lat': -34.6037, 'lon': -58.3816, 'description': 'The passionate heart of Argentina, known for its sensuous tango, European architecture, and vibrant steakhouses.', 'tags': 'culture,food,tango,party,architecture,international,couple,solo,student', 'cost_tier': 'budget'},
        {'id': 'limaperu001', 'name': 'Lima', 'city': 'Lima', 'country': 'Peru', 'lat': -12.0464, 'lon': -77.0428, 'description': 'The culinary capital of South America, offering a rich history and a world-class food scene.', 'tags': 'history,culture,food,coast,ruin,unesco,international,family,couple,solo', 'cost_tier': 'budget'},
        {'id': 'mexicocity001', 'name': 'Mexico City', 'city': 'Mexico City', 'country': 'Mexico', 'lat': 19.4326, 'lon': -99.1332, 'description': 'A bustling, high-altitude capital with Aztec ruins, baroque cathedrals, and a world-renowned art scene.', 'tags': 'history,culture,food,art,ruin,metropolis,unesco,international,family,couple,solo', 'cost_tier': 'budget'},
        {'id': 'losangeles001', 'name': 'Los Angeles', 'city': 'Los Angeles', 'country': 'USA', 'lat': 34.0522, 'lon': -118.2437, 'description': 'The entertainment capital of the world, a sprawling city of movie studios, beaches, and diverse neighborhoods.', 'tags': 'entertainment,beach,shopping,food,city-trip,international,family,couple,student,solo', 'cost_tier': 'luxury'},
        {'id': 'chicago001', 'name': 'Chicago', 'city': 'Chicago', 'country': 'USA', 'lat': 41.8781, 'lon': -87.6298, 'description': 'Famed for its bold architecture, vibrant music scene, and stunning skyline on the shores of Lake Michigan.', 'tags': 'architecture,culture,food,music,city-trip,lake,international,family,couple,solo', 'cost_tier': 'mid-range'},
        {'id': 'patagonia001', 'name': 'Patagonia', 'city': 'El Calafate', 'country': 'Argentina', 'lat': -50.3394, 'lon': -72.2758, 'description': 'A vast, wild region of dramatic ice fields, glaciers, and towering peaks, perfect for trekking.', 'tags': 'international,nature,mountain,hiking,adventure,glacier,road-trip,solo,couple', 'cost_tier': 'mid-range'},
        {'id': 'cancun001', 'name': 'Cancún', 'city': 'Cancún', 'country': 'Mexico', 'lat': 21.1619, 'lon': -86.8515, 'description': 'World-famous for its white-sand beaches, vibrant nightlife, and proximity to ancient Mayan ruins.', 'tags': 'international,beach,party,ruin,diving,luxury,couple,student,family', 'cost_tier': 'mid-range'},
        {'id': 'toronto001', 'name': 'Toronto', 'city': 'Toronto', 'country': 'Canada', 'lat': 43.6532, 'lon': -79.3832, 'description': 'Canada\'s largest city, a dynamic multicultural hub with iconic landmarks, diverse cuisine, and a vibrant arts scene.', 'tags': 'metropolis,culture,food,sightseeing,art,international,family,couple,solo', 'cost_tier': 'luxury'},
        {'id': 'miami001', 'name': 'Miami', 'city': 'Miami', 'country': 'USA', 'lat': 25.7617, 'lon': -80.1918, 'description': 'A vibrant city known for its glamorous beaches, Art Deco architecture, and rich Latin-American cultural influences.', 'tags': 'beach,party,art,culture,nightlife,luxury,international,couple,student', 'cost_tier': 'luxury'},
        {'id': 'cartagena001', 'name': 'Cartagena', 'city': 'Cartagena', 'country': 'Colombia', 'lat': 10.3910, 'lon': -75.4794, 'description': 'A stunning colonial walled city on the Caribbean coast, boasting colorful streets, historic forts, and lively plazas.', 'tags': 'history,culture,beach,romance,architecture,unesco,international,couple,family', 'cost_tier': 'budget'},
        {'id': 'costarica001', 'name': 'Costa Rica', 'city': 'San José', 'country': 'Costa Rica', 'lat': 9.7489, 'lon': -83.7534, 'description': 'A paradise of biodiversity, offering lush rainforests, towering volcanoes, and a world-renowned ecotourism scene.', 'tags': 'nature,adventure,wildlife,eco-tourism,rainforest,volcano,beach,international,family,solo', 'cost_tier': 'mid-range'},
        {'id': 'amazon001', 'name': 'Amazon Rainforest', 'city': 'Manaus', 'country': 'Brazil', 'lat': -3.4653, 'lon': -62.2159, 'description': 'The world\'s largest tropical rainforest, a realm of immense biodiversity and unforgettable river adventures.', 'tags': 'nature,rainforest,adventure,wildlife,eco-tourism,cruise,international,solo,couple', 'cost_tier': 'mid-range'},
        {'id': 'sanfrancisco001', 'name': 'San Francisco', 'city': 'San Francisco', 'country': 'USA', 'lat': 37.7749, 'lon': -122.4194, 'description': 'An iconic city known for the Golden Gate Bridge, cable cars, Alcatraz, and its vibrant tech culture.', 'tags': 'city-trip,landmark,culture,food,tech,lgbt,international,family,couple,solo', 'cost_tier': 'luxury'},
        {'id': 'neworleans001', 'name': 'New Orleans', 'city': 'New Orleans', 'country': 'USA', 'lat': 29.9511, 'lon': -90.0715, 'description': 'The birthplace of jazz, famous for its vibrant nightlife, spicy cuisine, and festive atmosphere, especially during Mardi Gras.', 'tags': 'music,jazz,food,party,culture,history,international,student,solo,couple', 'cost_tier': 'mid-range'},
        {'id': 'washingtondc001', 'name': 'Washington, D.C.', 'city': 'Washington, D.C.', 'country': 'USA', 'lat': 38.9072, 'lon': -77.0369, 'description': 'The U.S. capital, a city of iconic monuments, memorials, and a wealth of free world-class museums.', 'tags': 'history,politics,museum,sightseeing,monument,international,family,student,solo', 'cost_tier': 'mid-range'},
        {'id': 'boston001', 'name': 'Boston', 'city': 'Boston', 'country': 'USA', 'lat': 42.3601, 'lon': -71.0589, 'description': 'A city steeped in American history, known for its Freedom Trail, prestigious universities, and charming neighborhoods.', 'tags': 'history,university,culture,food,city-trip,international,family,student', 'cost_tier': 'luxury'},
        {'id': 'seattle001', 'name': 'Seattle', 'city': 'Seattle', 'country': 'USA', 'lat': 47.6062, 'lon': -122.3321, 'description': 'Home of the Space Needle and grunge music, a city on Puget Sound surrounded by mountains and evergreen forests.', 'tags': 'music,tech,coffee,nature,city-trip,international,solo,couple', 'cost_tier': 'luxury'},
        {'id': 'montreal001', 'name': 'Montreal', 'city': 'Montreal', 'country': 'Canada', 'lat': 45.5017, 'lon': -73.5673, 'description': 'A captivating blend of North American energy and European charm, known for its French heritage and arts scene.', 'tags': 'culture,history,food,festival,art,international,student,couple', 'cost_tier': 'mid-range'},
        {'id': 'quebeccity001', 'name': 'Quebec City', 'city': 'Quebec City', 'country': 'Canada', 'lat': 46.8139, 'lon': -71.2080, 'description': 'A stunning fortified colonial city with a rich French-Canadian heritage and a fairytale-like atmosphere.', 'tags': 'history,culture,architecture,romance,unesco,international,family,couple', 'cost_tier': 'mid-range'},
        {'id': 'cusco001', 'name': 'Cusco', 'city': 'Cusco', 'country': 'Peru', 'lat': -13.5320, 'lon': -71.9675, 'description': 'A beautiful high-altitude city that was the capital of the Inca Empire, now the gateway to Machu Picchu.', 'tags': 'history,culture,ruin,adventure,unesco,international,solo,student', 'cost_tier': 'budget'},
        {'id': 'bogota001', 'name': 'Bogotá', 'city': 'Bogotá', 'country': 'Colombia', 'lat': 4.7110, 'lon': -74.0721, 'description': 'Colombia\'s high-altitude capital, a city of contrasts with a historic center, vibrant street art, and world-class museums.', 'tags': 'culture,art,history,museum,city-trip,international,solo', 'cost_tier': 'budget'},
        {'id': 'medellin001', 'name': 'Medellín', 'city': 'Medellín', 'country': 'Colombia', 'lat': 6.2442, 'lon': -75.5812, 'description': 'Known as the "City of Eternal Spring," a story of urban transformation with innovative transport and a vibrant culture.', 'tags': 'modern,culture,city-trip,nightlife,international,solo,student', 'cost_tier': 'budget'},
        {'id': 'santiago001', 'name': 'Santiago', 'city': 'Santiago', 'country': 'Chile', 'lat': -33.4489, 'lon': -70.6693, 'description': 'Chile\'s sophisticated capital, nestled in a valley surrounded by the Andes, a gateway to wine regions and skiing.', 'tags': 'city-trip,wine,mountain,food,culture,international,couple,solo', 'cost_tier': 'mid-range'},
        {'id': 'lapaz001', 'name': 'La Paz', 'city': 'La Paz', 'country': 'Bolivia', 'lat': -16.4897, 'lon': -68.1193, 'description': 'The world\'s highest administrative capital, set in a dramatic bowl-shaped canyon in the Andes.', 'tags': 'mountain,culture,adventure,high-altitude,indigenous,international,solo,student', 'cost_tier': 'budget'},
        {'id': 'uyuni001', 'name': 'Salar de Uyuni', 'city': 'Uyuni', 'country': 'Bolivia', 'lat': -20.4633, 'lon': -66.8251, 'description': 'The world\'s largest salt flat, a surreal and otherworldly landscape that creates stunning mirror effects.', 'tags': 'nature,desert,salt-flat,scenic,adventure,road-trip,international,solo,couple', 'cost_tier': 'budget'},
        {'id': 'quito001', 'name': 'Quito', 'city': 'Quito', 'country': 'Ecuador', 'lat': -0.1807, 'lon': -78.4678, 'description': 'Ecuador\'s capital, perched high in the Andes, with one of the best-preserved historic centers in the Americas.', 'tags': 'history,culture,architecture,mountain,unesco,international,solo,couple', 'cost_tier': 'budget'},
        {'id': 'easterisland001', 'name': 'Easter Island', 'city': 'Hanga Roa', 'country': 'Chile', 'lat': -27.1127, 'lon': -109.3497, 'description': 'One of the most remote inhabited islands on Earth, famous for its monumental statues called moai.', 'tags': 'history,mystery,culture,nature,unesco,international,solo,couple', 'cost_tier': 'luxury'},
        {'id': 'iguazufalls001', 'name': 'Iguazu Falls', 'city': 'Foz do Iguaçu', 'country': 'Brazil', 'lat': -25.6953, 'lon': -54.4367, 'description': 'A magnificent system of waterfalls on the border of Brazil and Argentina, a true wonder of the natural world.', 'tags': 'nature,waterfall,adventure,sightseeing,unesco,international,family,couple', 'cost_tier': 'mid-range'},
        {'id': 'torresdelpaine001', 'name': 'Torres del Paine', 'city': 'Puerto Natales', 'country': 'Chile', 'lat': -50.9423, 'lon': -72.9934, 'description': 'A national park in Chilean Patagonia, celebrated for its soaring mountains, blue icebergs, and golden pampas.', 'tags': 'nature,hiking,mountain,adventure,glacier,patagonia,international,solo,couple', 'cost_tier': 'luxury'},
        {'id': 'grandcanyon001', 'name': 'Grand Canyon', 'city': 'Grand Canyon Village', 'country': 'USA', 'lat': 36.1069, 'lon': -112.1129, 'description': 'A colossal canyon carved by the Colorado River, offering breathtaking vistas and a rich geological history.', 'tags': 'nature,park,hiking,sightseeing,road-trip,adventure,unesco,international,family,solo', 'cost_tier': 'mid-range'},
        {'id': 'yellowstone001', 'name': 'Yellowstone', 'city': 'West Yellowstone', 'country': 'USA', 'lat': 44.4280, 'lon': -110.5885, 'description': 'The world\'s first national park, famous for its geysers (like Old Faithful), hot springs, and abundant wildlife.', 'tags': 'nature,park,wildlife,geyser,hiking,adventure,unesco,international,family', 'cost_tier': 'mid-range'},
        {'id': 'zion001', 'name': 'Zion National Park', 'city': 'Springdale', 'country': 'USA', 'lat': 37.2982, 'lon': -113.0263, 'description': 'A stunning national park in Utah featuring massive sandstone cliffs, narrow canyons, and the Virgin River.', 'tags': 'nature,park,hiking,canyoneering,adventure,road-trip,international,family,solo', 'cost_tier': 'mid-range'},
        
        # --- International - Middle East & Africa ---
        {'id': 'dubai001', 'name': 'Dubai', 'city': 'Dubai', 'country': 'UAE', 'lat': 25.2048, 'lon': 55.2708, 'description': 'A dazzling city of futuristic skyscrapers, luxury shopping, and ambitious, ultramodern attractions.', 'tags': 'luxury,shopping,modern,desert,sightseeing,metropolis,international,family,couple', 'cost_tier': 'luxury'},
        {'id': 'cairo001', 'name': 'Cairo', 'city': 'Cairo', 'country': 'Egypt', 'lat': 30.0444, 'lon': 31.2357, 'description': 'A bustling metropolis on the Nile, gateway to the ancient Pyramids of Giza and a treasure trove of antiquities.', 'tags': 'history,desert,landmark,museum,culture,unesco,international,family,solo,student', 'cost_tier': 'budget'},
        {'id': 'petra001', 'name': 'Petra', 'city': 'Wadi Musa', 'country': 'Jordan', 'lat': 30.3285, 'lon': 35.4444, 'description': 'An ancient city of rose-red rock, famous for its treasury carved directly into the sandstone cliffs.', 'tags': 'history,adventure,desert,sightseeing,landmark,unesco,international,solo,couple', 'cost_tier': 'mid-range'},
        {'id': 'marrakech001', 'name': 'Marrakech', 'city': 'Marrakech', 'country': 'Morocco', 'lat': 31.6295, 'lon': -7.9811, 'description': 'An exotic city of maze-like souks, vibrant spices, and stunning palaces, with a unique blend of Berber, Arab, and French cultures.', 'tags': 'culture,history,shopping,exotic,desert,unesco,international,couple,solo,student', 'cost_tier': 'budget'},
        {'id': 'cappadocia001', 'name': 'Cappadocia', 'city': 'Göreme', 'country': 'Turkey', 'lat': 38.6431, 'lon': 34.8285, 'description': 'A magical landscape of "fairy chimneys" and rock-cut houses, best seen from a hot air balloon at sunrise.', 'tags': 'nature,history,adventure,hot-air-balloon,romance,sightseeing,unesco,international,couple,solo', 'cost_tier': 'mid-range'},
        {'id': 'serengeti001', 'name': 'Serengeti National Park', 'city': 'Arusha', 'country': 'Tanzania', 'lat': -2.3333, 'lon': 34.8333, 'description': 'A vast ecosystem famous for the annual migration of millions of wildebeest and zebra.', 'tags': 'nature,wildlife,safari,adventure,unesco,international,family,couple,solo', 'cost_tier': 'luxury'},
        {'id': 'capetown001', 'name': 'Cape Town', 'city': 'Cape Town', 'country': 'South Africa', 'lat': -33.9249, 'lon': 18.4241, 'description': 'A stunning coastal city set beneath the iconic Table Mountain, offering a mix of nature, history, and vibrant culture.', 'tags': 'mountain,nature,beach,wine,history,adventure,international,family,couple,solo', 'cost_tier': 'mid-range'},
        {'id': 'jerusalem001', 'name': 'Jerusalem', 'city': 'Jerusalem', 'country': 'Israel', 'lat': 31.7683, 'lon': 35.2137, 'description': 'A holy city central to Judaism, Christianity, and Islam, with immense historical and spiritual significance.', 'tags': 'international,history,spiritual,culture,religious,sightseeing,unesco,solo,family', 'cost_tier': 'mid-range'},
        {'id': 'vicfalls001', 'name': 'Victoria Falls', 'city': 'Livingstone', 'country': 'Zambia', 'lat': -17.9243, 'lon': 25.8572, 'description': 'One of the Seven Natural Wonders of the World, forming the largest curtain of falling water on the planet.', 'tags': 'international,nature,waterfall,adventure,wildlife,sightseeing,unesco,couple,family', 'cost_tier': 'mid-range'},
        {'id': 'zanzibar001', 'name': 'Zanzibar', 'city': 'Zanzibar City', 'country': 'Tanzania', 'lat': -6.1659, 'lon': 39.199, 'description': 'A stunning archipelago off the coast of East Africa, known for its historic Stone Town, spice farms, and idyllic beaches.', 'tags': 'beach,history,culture,spice,relaxation,diving,romance,unesco,international,couple,family', 'cost_tier': 'mid-range'},
        {'id': 'abudhabi001', 'name': 'Abu Dhabi', 'city': 'Abu Dhabi', 'country': 'UAE', 'lat': 24.4539, 'lon': 54.3773, 'description': 'The capital of the UAE, blending modern marvels like the Sheikh Zayed Grand Mosque with cultural landmarks and luxury experiences.', 'tags': 'luxury,culture,modern,architecture,desert,family,sightseeing,international', 'cost_tier': 'luxury'},
        {'id': 'kruger001', 'name': 'Kruger National Park', 'city': 'Skukuza', 'country': 'South Africa', 'lat': -24.9945, 'lon': 31.5872, 'description': 'One of Africa\'s largest and most famous game reserves, offering an unparalleled wildlife safari experience.', 'tags': 'safari,wildlife,nature,adventure,family,photography,international,couple,solo', 'cost_tier': 'mid-range'},
        {'id': 'luxor001', 'name': 'Luxor', 'city': 'Luxor', 'country': 'Egypt', 'lat': 25.6872, 'lon': 32.6396, 'description': 'Often called the world\'s greatest open-air museum, home to the temples of Karnak and Luxor, and the Valley of the Kings.', 'tags': 'history,temple,ruin,ancient,unesco,international,family,solo', 'cost_tier': 'budget'},
        {'id': 'fes001', 'name': 'Fes', 'city': 'Fes', 'country': 'Morocco', 'lat': 34.0181, 'lon': -5.0078, 'description': 'A captivating medieval city with a sprawling, maze-like medina, vibrant souks, and ancient leather tanneries.', 'tags': 'history,culture,medieval,artisan,unesco,international,solo,couple', 'cost_tier': 'budget'},
        {'id': 'doha001', 'name': 'Doha', 'city': 'Doha', 'country': 'Qatar', 'lat': 25.2854, 'lon': 51.5310, 'description': 'A futuristic capital on the Persian Gulf, known for its ultramodern architecture, Museum of Islamic Art, and traditional souq.', 'tags': 'modern,luxury,art,culture,architecture,desert,international,family,business', 'cost_tier': 'luxury'},
        {'id': 'muscat001', 'name': 'Muscat', 'city': 'Muscat', 'country': 'Oman', 'lat': 23.5880, 'lon': 58.3829, 'description': 'A charming capital set between mountains and the sea, known for its beautiful mosques, souqs, and rugged coastline.', 'tags': 'culture,history,nature,sea,mountain,relaxation,international,family,couple', 'cost_tier': 'mid-range'},
        {'id': 'telaviv001', 'name': 'Tel Aviv', 'city': 'Tel Aviv', 'country': 'Israel', 'lat': 32.0853, 'lon': 34.7818, 'description': 'A vibrant Mediterranean city known for its buzzing nightlife, beautiful beaches, and UNESCO-recognized Bauhaus architecture.', 'tags': 'beach,party,nightlife,modern,culture,food,lgbt,international,student,solo', 'cost_tier': 'luxury'},
        {'id': 'nairobi001', 'name': 'Nairobi', 'city': 'Nairobi', 'country': 'Kenya', 'lat': -1.2921, 'lon': 36.8219, 'description': 'East Africa\'s vibrant hub, a gateway to safari adventures with its own unique urban wildlife park.', 'tags': 'safari,wildlife,city-trip,culture,business,international,solo', 'cost_tier': 'mid-range'},
        {'id': 'maasaimara001', 'name': 'Maasai Mara', 'city': 'Narok', 'country': 'Kenya', 'lat': -1.5000, 'lon': 35.0000, 'description': 'A world-renowned reserve famous for its exceptional population of big cats and the Great Migration.', 'tags': 'safari,wildlife,nature,adventure,culture,international,family,couple', 'cost_tier': 'luxury'},
        {'id': 'okavango001', 'name': 'Okavango Delta', 'city': 'Maun', 'country': 'Botswana', 'lat': -19.4333, 'lon': 23.3167, 'description': 'A vast inland river delta in northern Botswana, a unique oasis where wildlife thrives in a water-logged landscape.', 'tags': 'safari,wildlife,nature,river,luxury,unesco,international,couple,solo', 'cost_tier': 'luxury'},
        {'id': 'addisababa001', 'name': 'Addis Ababa', 'city': 'Addis Ababa', 'country': 'Ethiopia', 'lat': 9.0054, 'lon': 38.7578, 'description': 'Ethiopia\'s bustling capital, a high-altitude city rich in history and the diplomatic capital of Africa.', 'tags': 'history,culture,city-trip,museum,international,solo,business', 'cost_tier': 'budget'},
        {'id': 'seychelles001', 'name': 'Seychelles', 'city': 'Victoria', 'country': 'Seychelles', 'lat': -4.6796, 'lon': 55.4920, 'description': 'An archipelago of 115 islands in the Indian Ocean, home to stunning beaches, giant tortoises, and lush nature reserves.', 'tags': 'beach,luxury,romance,nature,relaxation,diving,honeymoon,international,couple,family', 'cost_tier': 'luxury'},
        {'id': 'mauritius001', 'name': 'Mauritius', 'city': 'Port Louis', 'country': 'Mauritius', 'lat': -20.3484, 'lon': 57.5522, 'description': 'An Indian Ocean island nation, known for its beaches, lagoons, reefs, and mountainous interior with lush rainforests.', 'tags': 'beach,luxury,nature,waterfall,hiking,family,romance,international', 'cost_tier': 'luxury'},
        {'id': 'windhoek001', 'name': 'Windhoek', 'city': 'Windhoek', 'country': 'Namibia', 'lat': -22.5594, 'lon': 17.0832, 'description': 'The clean and safe capital of Namibia, a starting point for adventures into the country\'s dramatic desert landscapes.', 'tags': 'city-trip,culture,desert,safari-gateway,international,solo', 'cost_tier': 'mid-range'},
        {'id': 'sossusvlei001', 'name': 'Sossusvlei', 'city': 'Sesriem', 'country': 'Namibia', 'lat': -24.7333, 'lon': 15.3500, 'description': 'A stunning salt and clay pan surrounded by giant red sand dunes, located in the Namib-Naufluft National Park.', 'tags': 'desert,nature,dunes,scenic,adventure,photography,unesco,international,solo,couple', 'cost_tier': 'mid-range'},
        {'id': 'chefchaouen001', 'name': 'Chefchaouen', 'city': 'Chefchaouen', 'country': 'Morocco', 'lat': 35.1688, 'lon': -5.2685, 'description': 'The famous "Blue Pearl" of Morocco, a beautiful town in the Rif Mountains with a striking blue-washed old town.', 'tags': 'scenic,culture,relaxation,mountain,photography,international,solo,couple', 'cost_tier': 'budget'},
        {'id': 'dakar001', 'name': 'Dakar', 'city': 'Dakar', 'country': 'Senegal', 'lat': 14.7167, 'lon': -17.4677, 'description': 'A vibrant coastal city on the Cap-Vert peninsula, known for its lively arts scene, music, and markets.', 'tags': 'culture,music,art,coast,city-trip,international,solo', 'cost_tier': 'budget'},
        {'id': 'accra001', 'name': 'Accra', 'city': 'Accra', 'country': 'Ghana', 'lat': 5.6037, 'lon': -0.1870, 'description': 'Ghana\'s dynamic capital, a hub of culture, history, and nightlife on the Atlantic coast.', 'tags': 'history,culture,music,beach,city-trip,international,solo', 'cost_tier': 'budget'},
        {'id': 'lagos001', 'name': 'Lagos', 'city': 'Lagos', 'country': 'Nigeria', 'lat': 6.5244, 'lon': 3.3792, 'description': 'Africa\'s largest city, an energetic and chaotic metropolis at the forefront of music, fashion, and tech.', 'tags': 'metropolis,music,culture,party,business,international,solo', 'cost_tier': 'budget'},
        {'id': 'antananarivo001', 'name': 'Antananarivo', 'city': 'Antananarivo', 'country': 'Madagascar', 'lat': -18.8792, 'lon': 47.5079, 'description': 'The capital of Madagascar, a city of hills, palaces, churches, and a gateway to the island\'s unique wildlife.', 'tags': 'city-trip,history,culture,wildlife-gateway,international,solo', 'cost_tier': 'budget'},
        {'id': 'gorillatrek001', 'name': 'Volcanoes National Park', 'city': 'Ruhengeri', 'country': 'Rwanda', 'lat': -1.4725, 'lon': 29.5936, 'description': 'A breathtaking national park offering the life-changing experience of trekking to see mountain gorillas in their natural habitat.', 'tags': 'wildlife,gorilla,hiking,nature,adventure,unesco,international,couple,solo', 'cost_tier': 'luxury'},
    ]

    # --- Data for 'landmarks' Table (Fully Populated) ---
    curated_landmarks = [
        # --- Indian Cities ---
        {'dest_id': 'goa001', 'name': 'Baga Beach', 'category': 'attraction', 'address': 'Baga Beach, North Goa, Goa', 'lat': 15.5583, 'lon': 73.7518},
        {'dest_id': 'goa001', 'name': 'Basilica of Bom Jesus', 'category': 'attraction', 'address': 'Old Goa Rd, Bainguinim, Goa 403402', 'lat': 15.5009, 'lon': 73.9116},
        {'dest_id': 'goa001', 'name': 'Fort Aguada', 'category': 'attraction', 'address': 'Fort Aguada Rd, Candolim, Goa 403515', 'lat': 15.4932, 'lon': 73.7735},
        {'dest_id': 'goa001', 'name': 'Britto\'s Restaurant & Bar', 'category': 'restaurant', 'address': 'Baga Beach, Santo Vaddo, Calangute, Goa 403516', 'lat': 15.5596, 'lon': 73.7503},

        {'dest_id': 'udai001', 'name': 'City Palace', 'category': 'attraction', 'address': 'Old City, Udaipur, Rajasthan 313001', 'lat': 24.5760, 'lon': 73.6835},
        {'dest_id': 'udai001', 'name': 'Lake Pichola', 'category': 'attraction', 'address': 'Udaipur, Rajasthan', 'lat': 24.5721, 'lon': 73.6766},
        {'dest_id': 'udai001', 'name': 'Jag Mandir', 'category': 'attraction', 'address': 'Pichola, Udaipur, Rajasthan 313001', 'lat': 24.5700, 'lon': 73.6780},
        {'dest_id': 'udai001', 'name': 'Ambrai Restaurant', 'category': 'restaurant', 'address': 'Amet Haveli, Hanuman Ghat, Udaipur, Rajasthan 313001', 'lat': 24.5794, 'lon': 73.6806},
        
        {'dest_id': 'jai001', 'name': 'Hawa Mahal', 'category': 'attraction', 'address': 'Hawa Mahal Rd, Badi Choupad, J.D.A. Market, Pink City, Jaipur, Rajasthan 302002', 'lat': 26.9239, 'lon': 75.8267},
        {'dest_id': 'jai001', 'name': 'Amber Palace', 'category': 'attraction', 'address': 'Devisinghpura, Amer, Jaipur, Rajasthan 302028', 'lat': 26.9855, 'lon': 75.8513},
        {'dest_id': 'jai001', 'name': 'City Palace, Jaipur', 'category': 'attraction', 'address': 'Tulsi Marg, Gangori Bazaar, J.D.A. Market, Pink City, Jaipur, Rajasthan 302002', 'lat': 26.9257, 'lon': 75.8237},
        {'dest_id': 'jai001', 'name': 'Chokhi Dhani Village', 'category': 'restaurant', 'address': '12 Miles Tonk Road, Via Vatika, Jaipur, Rajasthan 303905', 'lat': 26.7622, 'lon': 75.8062},

        {'dest_id': 'rish001', 'name': 'Laxman Jhula', 'category': 'attraction', 'address': 'Laxman Jhula, Tapovan, Rishikesh, Uttarakhand 249192', 'lat': 30.1264, 'lon': 78.3292},
        {'dest_id': 'rish001', 'name': 'Ram Jhula', 'category': 'attraction', 'address': 'Ram Jhula, Rishikesh, Uttarakhand 249304', 'lat': 30.1197, 'lon': 78.3204},
        {'dest_id': 'rish001', 'name': 'Triveni Ghat', 'category': 'attraction', 'address': 'Mayakund, Rishikesh, Uttarakhand 249201', 'lat': 30.1098, 'lon': 78.3129},
        {'dest_id': 'rish001', 'name': 'The Beatles Cafe', 'category': 'restaurant', 'address': 'Laxman Jhula, Tapovan, Rishikesh, Uttarakhand 249192', 'lat': 30.1278, 'lon': 78.3283},

        {'dest_id': 'manali001', 'name': 'Hidimba Devi Temple', 'category': 'attraction', 'address': 'Hadimba Temple Rd, Old Manali, Manali, Himachal Pradesh 175131', 'lat': 32.2494, 'lon': 77.1804},
        {'dest_id': 'manali001', 'name': 'Solang Valley', 'category': 'attraction', 'address': 'Solang Valley, Burwa, Himachal Pradesh 175131', 'lat': 32.3168, 'lon': 77.1583},
        {'dest_id': 'manali001', 'name': 'Jogini Falls', 'category': 'attraction', 'address': 'Vashist, Bashisht, Himachal Pradesh 175103', 'lat': 32.2619, 'lon': 77.1853},
        {'dest_id': 'manali001', 'name': 'Johnson\'s Cafe', 'category': 'restaurant', 'address': 'Circuit House Rd, Siyal, Manali, Himachal Pradesh 175131', 'lat': 32.2464, 'lon': 77.1843},

        {'dest_id': 'kera001', 'name': 'Alappuzha Beach', 'category': 'attraction', 'address': 'Alappuzha Beach, Alleppey, Kerala', 'lat': 9.5020, 'lon': 76.3195},
        {'dest_id': 'kera001', 'name': 'Vembanad Lake', 'category': 'attraction', 'address': 'Vembanad Lake, Kerala', 'lat': 9.8458, 'lon': 76.3756},
        {'dest_id': 'kera001', 'name': 'Marari Beach', 'category': 'attraction', 'address': 'Marari Beach, Alappuzha, Kerala', 'lat': 9.6015, 'lon': 76.2954},
        {'dest_id': 'kera001', 'name': 'Thaff Restaurant', 'category': 'restaurant', 'address': 'Thaff Restaurant, Mullackal, Alleppey, Kerala 688011', 'lat': 9.4996, 'lon': 76.3400},
        
        {'dest_id': 'darj001', 'name': 'Tiger Hill', 'category': 'attraction', 'address': 'Tiger Hill, Darjeeling, West Bengal', 'lat': 27.0118, 'lon': 88.2730},
        {'dest_id': 'darj001', 'name': 'Batasia Loop', 'category': 'attraction', 'address': 'Ghoom, Darjeeling, West Bengal 734102', 'lat': 27.0163, 'lon': 88.2494},
        {'dest_id': 'darj001', 'name': 'Padmaja Naidu Himalayan Zoological Park', 'category': 'attraction', 'address': 'Jawahar Parbat, Darjeeling, West Bengal 734101', 'lat': 27.0543, 'lon': 88.2583},
        {'dest_id': 'darj001', 'name': 'Glenary\'s Restaurant & Bar', 'category': 'restaurant', 'address': 'Nehru Road, Darjeeling, West Bengal 734101', 'lat': 27.0423, 'lon': 88.2652},
        
        {'dest_id': 'ladakh001', 'name': 'Pangong Tso Lake', 'category': 'attraction', 'address': 'Pangong Tso, Leh, Ladakh', 'lat': 33.7588, 'lon': 78.6633},
        {'dest_id': 'ladakh001', 'name': 'Khardung La Pass', 'category': 'attraction', 'address': 'Khardung La, Leh, Ladakh', 'lat': 34.2986, 'lon': 77.6042},
        {'dest_id': 'ladakh001', 'name': 'Shanti Stupa', 'category': 'attraction', 'address': 'Shanti Stupa Rd, Leh, Ladakh 194101', 'lat': 34.1594, 'lon': 77.5732},
        {'dest_id': 'ladakh001', 'name': 'The Tibetan Kitchen', 'category': 'restaurant', 'address': 'Fort Road, Leh, Ladakh 194101', 'lat': 34.1661, 'lon': 77.5855},
        
        {'dest_id': 'varan001', 'name': 'Ganges River', 'category': 'attraction', 'address': 'Varanasi, Uttar Pradesh', 'lat': 25.3176, 'lon': 82.9739},
        {'dest_id': 'varan001', 'name': 'Dashashwamedh Ghat', 'category': 'attraction', 'address': 'Dashashwamedh Ghat Rd, Godowlia, Varanasi, Uttar Pradesh 221001', 'lat': 25.3079, 'lon': 83.0108},
        {'dest_id': 'varan001', 'name': 'Kashi Vishwanath Temple', 'category': 'attraction', 'address': 'Lahori Tola, Varanasi, Uttar Pradesh 221001', 'lat': 25.3109, 'lon': 83.0104},
        {'dest_id': 'varan001', 'name': 'Kashi Chat Bhandar', 'category': 'restaurant', 'address': 'D-37/49, Godowlia, Varanasi, Uttar Pradesh 221001', 'lat': 25.3093, 'lon': 83.0086},
        
        {'dest_id': 'mumbai001', 'name': 'Gateway of India', 'category': 'attraction', 'address': 'Apollo Bandar, Colaba, Mumbai, Maharashtra 400001', 'lat': 18.9220, 'lon': 72.8347},
        {'dest_id': 'mumbai001', 'name': 'Marine Drive', 'category': 'attraction', 'address': 'Netaji Subhash Chandra Bose Road, Mumbai, Maharashtra 400020', 'lat': 18.9433, 'lon': 72.8246},
        {'dest_id': 'mumbai001', 'name': 'Elephanta Caves', 'category': 'attraction', 'address': 'Gharapuri, Maharashtra 400094', 'lat': 18.9634, 'lon': 72.9315},
        {'dest_id': 'mumbai001', 'name': 'Leopold Cafe', 'category': 'restaurant', 'address': 'Shahid Bhagat Singh Road, Colaba Causeway, Mumbai, Maharashtra 400001', 'lat': 18.9229, 'lon': 72.8339},
        
        {'dest_id': 'delhi001', 'name': 'India Gate', 'category': 'attraction', 'address': 'Rajpath, India Gate, New Delhi, Delhi 110001', 'lat': 28.6129, 'lon': 77.2295},
        {'dest_id': 'delhi001', 'name': 'Qutub Minar', 'category': 'attraction', 'address': 'Mehrauli, New Delhi, Delhi 110030', 'lat': 28.5245, 'lon': 77.1855},
        {'dest_id': 'delhi001', 'name': 'Humayun\'s Tomb', 'category': 'attraction', 'address': 'Mathura Road, Nizamuddin East, New Delhi, Delhi 110013', 'lat': 28.5933, 'lon': 77.2507},
        {'dest_id': 'delhi001', 'name': 'Karim\'s', 'category': 'restaurant', 'address': '16, Gali Kababian, Jama Masjid, New Delhi, Delhi 110006', 'lat': 28.6496, 'lon': 77.2341},
        
        {'dest_id': 'amrit001', 'name': 'Golden Temple', 'category': 'attraction', 'address': 'Golden Temple Rd, Atta Mandi, Katra Ahluwalia, Amritsar, Punjab 143006', 'lat': 31.6200, 'lon': 74.8765},
        {'dest_id': 'amrit001', 'name': 'Jallianwala Bagh', 'category': 'attraction', 'address': 'Golden Temple Rd, Atta Mandi, Katra Ahluwalia, Amritsar, Punjab 143006', 'lat': 31.6206, 'lon': 74.8801},
        {'dest_id': 'amrit001', 'name': 'Wagah Border', 'category': 'attraction', 'address': 'Wagah, Hardo Rattan, Amritsar, Punjab 143108', 'lat': 31.6051, 'lon': 74.5766},
        {'dest_id': 'amrit001', 'name': 'Kesar Da Dhaba', 'category': 'restaurant', 'address': 'Chowk Passian, Gali Rajpura, Amritsar, Punjab 143001', 'lat': 31.6254, 'lon': 74.8784},
        
        {'dest_id': 'agra001', 'name': 'Taj Mahal', 'category': 'attraction', 'address': 'Dharmapuri, Forest Colony, Tajganj, Agra, Uttar Pradesh 282001', 'lat': 27.1751, 'lon': 78.0421},
        {'dest_id': 'agra001', 'name': 'Agra Fort', 'category': 'attraction', 'address': 'Rakabganj, Agra, Uttar Pradesh 282003', 'lat': 27.1795, 'lon': 78.0211},
        {'dest_id': 'agra001', 'name': 'Mehtab Bagh', 'category': 'attraction', 'address': 'Nagla Devjit, Agra, Uttar Pradesh 282006', 'lat': 27.1793, 'lon': 78.0416},
        {'dest_id': 'agra001', 'name': 'Pinch of Spice', 'category': 'restaurant', 'address': '23/453, Wazirpura Road, Agra, Uttar Pradesh 282003', 'lat': 27.1959, 'lon': 78.0125},

        {'dest_id': 'jaisalmer001', 'name': 'Jaisalmer Fort', 'category': 'attraction', 'address': 'Fort Rd, Manak Chowk, Amar Sagar Pol, Jaisalmer, Rajasthan 345001', 'lat': 26.9127, 'lon': 70.9124},
        {'dest_id': 'jaisalmer001', 'name': 'Sam Sand Dunes', 'category': 'attraction', 'address': 'Sam, Rajasthan 345001', 'lat': 26.8306, 'lon': 70.5034},
        {'dest_id': 'jaisalmer001', 'name': 'Patwon Ki Haveli', 'category': 'attraction', 'address': 'No. 3129, Near Chouraha, Patwa Haveli, Jaisalmer, Rajasthan 345001', 'lat': 26.9143, 'lon': 70.9127},
        {'dest_id': 'jaisalmer001', 'name': 'Trio Restaurant', 'category': 'restaurant', 'address': 'Gandhi Chowk, Jaisalmer, Rajasthan 345001', 'lat': 26.9168, 'lon': 70.9101},

        {'dest_id': 'andaman001', 'name': 'Radhanagar Beach', 'category': 'attraction', 'address': 'Havelock Island, Andaman and Nicobar Islands', 'lat': 12.0258, 'lon': 92.9431},
        {'dest_id': 'andaman001', 'name': 'Cellular Jail', 'category': 'attraction', 'address': 'Atlanta Point, Port Blair, Andaman and Nicobar Islands 744104', 'lat': 11.6738, 'lon': 92.7558},
        {'dest_id': 'andaman001', 'name': 'Ross Island', 'category': 'attraction', 'address': 'Ross Island, Port Blair, Andaman and Nicobar Islands', 'lat': 11.6783, 'lon': 92.7663},
        {'dest_id': 'andaman001', 'name': 'Anju Coco Resto', 'category': 'restaurant', 'address': 'Beach No. 5, Havelock Island, Andaman and Nicobar Islands 744211', 'lat': 12.0300, 'lon': 92.9500},

        {'dest_id': 'coorg001', 'name': 'Abbey Falls', 'category': 'attraction', 'address': 'Abbey Falls, Madikeri, Karnataka 571201', 'lat': 12.4358, 'lon': 75.7339},
        {'dest_id': 'coorg001', 'name': 'Raja\'s Seat', 'category': 'attraction', 'address': 'Stuart Hill, Madikeri, Karnataka 571201', 'lat': 12.4173, 'lon': 75.7371},
        {'dest_id': 'coorg001', 'name': 'Namdroling Monastery', 'category': 'attraction', 'address': 'Arlikumari, Bylakuppe, Karnataka 571104', 'lat': 12.3550, 'lon': 76.0450},
        {'dest_id': 'coorg001', 'name': 'Coorg Cuisine', 'category': 'restaurant', 'address': 'Main Bus Stand Road, Madikeri, Karnataka 571201', 'lat': 12.4211, 'lon': 75.7401},

        {'dest_id': 'shillong001', 'name': 'Umiam Lake', 'category': 'attraction', 'address': 'Umiam, Meghalaya', 'lat': 25.6757, 'lon': 91.8988},
        {'dest_id': 'shillong001', 'name': 'Elephant Falls', 'category': 'attraction', 'address': 'Upper Shillong, Shillong, Meghalaya 793009', 'lat': 25.5393, 'lon': 91.8341},
        {'dest_id': 'shillong001', 'name': 'Laitlum Canyons', 'category': 'attraction', 'address': 'Laitlum, Meghalaya 793015', 'lat': 25.5300, 'lon': 91.9800},
        {'dest_id': 'shillong001', 'name': 'Cafe Shillong', 'category': 'restaurant', 'address': 'Laitumkhrah, Shillong, Meghalaya 793003', 'lat': 25.5721, 'lon': 91.8941},

        {'dest_id': 'hampi001', 'name': 'Virupaksha Temple', 'category': 'attraction', 'address': 'Hampi, Karnataka 583239', 'lat': 15.3350, 'lon': 76.4600},
        {'dest_id': 'hampi001', 'name': 'Vittala Temple', 'category': 'attraction', 'address': 'Hampi, Karnataka 583239', 'lat': 15.3400, 'lon': 76.4700},
        {'dest_id': 'hampi001', 'name': 'Matanga Hill', 'category': 'attraction', 'address': 'Hampi, Karnataka 583239', 'lat': 15.3333, 'lon': 76.4667},
        {'dest_id': 'hampi001', 'name': 'Mango Tree Restaurant', 'category': 'restaurant', 'address': 'Near Virupaksha Temple, Hampi, Karnataka 583239', 'lat': 15.3355, 'lon': 76.4605},

        {'dest_id': 'jodhpur001', 'name': 'Mehrangarh Fort', 'category': 'attraction', 'address': 'The Fort, Jodhpur, Rajasthan 342006', 'lat': 26.2976, 'lon': 73.0188},
        {'dest_id': 'jodhpur001', 'name': 'Jaswant Thada', 'category': 'attraction', 'address': 'Lawaran, Jodhpur, Rajasthan 342001', 'lat': 26.2994, 'lon': 73.0200},
        {'dest_id': 'jodhpur001', 'name': 'Umaid Bhawan Palace', 'category': 'attraction', 'address': 'Circuit House Rd, Cantt Area, Jodhpur, Rajasthan 342006', 'lat': 26.2811, 'lon': 73.0470},
        {'dest_id': 'jodhpur001', 'name': 'Indique Restaurant', 'category': 'restaurant', 'address': 'Pal Haveli, Gulab Sagar, Jodhpur, Rajasthan 342001', 'lat': 26.2941, 'lon': 73.0261},

        {'dest_id': 'spiti001', 'name': 'Key Monastery', 'category': 'attraction', 'address': 'Key, Himachal Pradesh 172114', 'lat': 32.2981, 'lon': 78.0125},
        {'dest_id': 'spiti001', 'name': 'Chandratal Lake', 'category': 'attraction', 'address': 'Chandratal, Himachal Pradesh', 'lat': 32.4792, 'lon': 77.6167},
        {'dest_id': 'spiti001', 'name': 'Hikkim Village', 'category': 'attraction', 'address': 'Hikkim, Himachal Pradesh 172114', 'lat': 32.3333, 'lon': 78.0667},
        {'dest_id': 'spiti001', 'name': 'Sol Cafe', 'category': 'restaurant', 'address': 'Kaza, Himachal Pradesh 172114', 'lat': 32.2279, 'lon': 78.0731},

        {'dest_id': 'pondy001', 'name': 'Auroville', 'category': 'attraction', 'address': 'Auroville, Tamil Nadu 605101', 'lat': 12.0067, 'lon': 79.8139},
        {'dest_id': 'pondy001', 'name': 'Promenade Beach', 'category': 'attraction', 'address': 'Pondicherry, 605001', 'lat': 11.9328, 'lon': 79.8344},
        {'dest_id': 'pondy001', 'name': 'Sri Aurobindo Ashram', 'category': 'attraction', 'address': 'No. 9, Marine Street, White Town, Puducherry, 605002', 'lat': 11.9358, 'lon': 79.8339},
        {'dest_id': 'pondy001', 'name': 'Le Dupleix', 'category': 'restaurant', 'address': '5, Caserne Street, Puducherry, 605001', 'lat': 11.9333, 'lon': 79.8333},

        {'dest_id': 'munnar001', 'name': 'Eravikulam National Park', 'category': 'attraction', 'address': 'The Wildlife Warden Munnar PO, Idukki, Kerala, 685612', 'lat': 10.1500, 'lon': 77.0500},
        {'dest_id': 'munnar001', 'name': 'Mattupetty Dam', 'category': 'attraction', 'address': 'Munnar, Kerala 685616', 'lat': 10.1167, 'lon': 77.1333},
        {'dest_id': 'munnar001', 'name': 'Top Station', 'category': 'attraction', 'address': 'Top Station, Kerala', 'lat': 10.1250, 'lon': 77.2417},
        {'dest_id': 'munnar001', 'name': 'Saravana Bhavan', 'category': 'restaurant', 'address': 'Munnar, Kerala 685612', 'lat': 10.0889, 'lon': 77.0595},

        {'dest_id': 'kolkata001', 'name': 'Victoria Memorial', 'category': 'attraction', 'address': 'Victoria Memorial Hall, 1, Queen\'s Way, Kolkata, West Bengal 700071', 'lat': 22.5448, 'lon': 88.3426},
        {'dest_id': 'kolkata001', 'name': 'Howrah Bridge', 'category': 'attraction', 'address': 'Howrah, West Bengal', 'lat': 22.5852, 'lon': 88.3470},
        {'dest_id': 'kolkata001', 'name': 'Dakshineswar Kali Temple', 'category': 'attraction', 'address': 'Dakshineswar, Kolkata, West Bengal 700076', 'lat': 22.6548, 'lon': 88.3578},
        {'dest_id': 'kolkata001', 'name': 'Peter Cat', 'category': 'restaurant', 'address': '18A, Park St, Park Street area, Kolkata, West Bengal 700071', 'lat': 22.5528, 'lon': 88.3548},

        {'dest_id': 'ahmedabad001', 'name': 'Sabarmati Ashram', 'category': 'attraction', 'address': 'Gandhi Smarak Sangrahalaya, Ashram Rd, Ahmedabad, Gujarat 380027', 'lat': 23.0611, 'lon': 72.5806},
        {'dest_id': 'ahmedabad001', 'name': 'Adalaj Stepwell', 'category': 'attraction', 'address': 'Adalaj, Gujarat 382421', 'lat': 23.1656, 'lon': 72.5861},
        {'dest_id': 'ahmedabad001', 'name': 'Kankaria Lake', 'category': 'attraction', 'address': 'Kankaria, Ahmedabad, Gujarat', 'lat': 23.0064, 'lon': 72.6019},
        {'dest_id': 'ahmedabad001', 'name': 'Agashiye - The House of MG', 'category': 'restaurant', 'address': 'The House of MG, Lal Darwaja, Ahmedabad, Gujarat 380001', 'lat': 23.0250, 'lon': 72.5833},

        {'dest_id': 'shimla001', 'name': 'The Ridge', 'category': 'attraction', 'address': 'The Ridge, Shimla, Himachal Pradesh', 'lat': 31.1058, 'lon': 77.1734},
        {'dest_id': 'shimla001', 'name': 'Jakhoo Temple', 'category': 'attraction', 'address': 'Jakhoo Temple Park, Jakhoo, Shimla, Himachal Pradesh 171001', 'lat': 31.1017, 'lon': 77.1819},
        {'dest_id': 'shimla001', 'name': 'Kufri', 'category': 'attraction', 'address': 'Kufri, Himachal Pradesh', 'lat': 31.0978, 'lon': 77.2644},
        {'dest_id': 'shimla001', 'name': 'Indian Coffee House', 'category': 'restaurant', 'address': 'The Mall, Shimla, Himachal Pradesh 171001', 'lat': 31.1048, 'lon': 77.1734},

        {'dest_id': 'mysore001', 'name': 'Mysore Palace', 'category': 'attraction', 'address': 'Sayyaji Rao Rd, Agrahara, Chamrajpura, Mysuru, Karnataka 570001', 'lat': 12.3051, 'lon': 76.6552},
        {'dest_id': 'mysore001', 'name': 'Brindavan Gardens', 'category': 'attraction', 'address': 'KRS Dam Road, Mandya, Karnataka 571607', 'lat': 12.4217, 'lon': 76.5733},
        {'dest_id': 'mysore001', 'name': 'Chamundi Hill', 'category': 'attraction', 'address': 'Mysuru, Karnataka 570010', 'lat': 12.2753, 'lon': 76.6700},
        {'dest_id': 'mysore001', 'name': 'Vinayaka Mylari', 'category': 'restaurant', 'address': '79, Nazarbad Main Rd, Doora, Mysuru, Karnataka 570010', 'lat': 12.3025, 'lon': 76.6622},

        {'dest_id': 'kutch001', 'name': 'Great Rann of Kutch', 'category': 'attraction', 'address': 'Great Rann of Kutch, Gujarat', 'lat': 23.8541, 'lon': 70.4008},
        {'dest_id': 'kutch001', 'name': 'Kalo Dungar', 'category': 'attraction', 'address': 'Khavda, Gujarat 370510', 'lat': 23.9781, 'lon': 69.8239},
        {'dest_id': 'kutch001', 'name': 'Mandvi Beach', 'category': 'attraction', 'address': 'Mandvi, Gujarat', 'lat': 22.8167, 'lon': 69.3500},
        {'dest_id': 'kutch001', 'name': 'Osho Hotel', 'category': 'restaurant', 'address': 'Station Road, Bhuj, Gujarat 370001', 'lat': 23.2500, 'lon': 69.6667},

        {'dest_id': 'gokarna001', 'name': 'Om Beach', 'category': 'attraction', 'address': 'Gokarna, Karnataka', 'lat': 14.5200, 'lon': 74.3167},
        {'dest_id': 'gokarna001', 'name': 'Mahabaleshwar Temple', 'category': 'attraction', 'address': 'Koti Teertha Rd, Kotiteertha, Gokarna, Karnataka 581326', 'lat': 14.5444, 'lon': 74.3153},
        {'dest_id': 'gokarna001', 'name': 'Kudle Beach', 'category': 'attraction', 'address': 'Gokarna, Karnataka', 'lat': 14.5333, 'lon': 74.3167},
        {'dest_id': 'gokarna001', 'name': 'Namaste Cafe', 'category': 'restaurant', 'address': 'Om Beach, Gokarna, Karnataka 581326', 'lat': 14.5200, 'lon': 74.3167},

        {'dest_id': 'kaziranga001', 'name': 'Central Range', 'category': 'attraction', 'address': 'Kaziranga National Park, Assam', 'lat': 26.6667, 'lon': 93.3333},
        {'dest_id': 'kaziranga001', 'name': 'Western Range', 'category': 'attraction', 'address': 'Kaziranga National Park, Assam', 'lat': 26.6500, 'lon': 93.1667},
        {'dest_id': 'kaziranga001', 'name': 'Kaziranga Orchid and Biodiversity Park', 'category': 'attraction', 'address': 'NH 37, Durgapur, Assam 785609', 'lat': 26.6231, 'lon': 93.4331},
        {'dest_id': 'kaziranga001', 'name': 'Hornbill Restaurant', 'category': 'restaurant', 'address': 'Kohora, Kaziranga National Park, Assam', 'lat': 26.5775, 'lon': 93.3639},

        {'dest_id': 'chennai001', 'name': 'Marina Beach', 'category': 'attraction', 'address': 'Marina Beach, Chennai, Tamil Nadu', 'lat': 13.0500, 'lon': 80.2825},
        {'dest_id': 'chennai001', 'name': 'Kapaleeshwarar Temple', 'category': 'attraction', 'address': 'Mylapore, Chennai, Tamil Nadu 600004', 'lat': 13.0339, 'lon': 80.2694},
        {'dest_id': 'chennai001', 'name': 'Fort St. George', 'category': 'attraction', 'address': 'Rajaji Salai, Near Legislature and Secretariat, Chennai, Tamil Nadu 600009', 'lat': 13.0811, 'lon': 80.2894},
        {'dest_id': 'chennai001', 'name': 'Murugan Idli Shop', 'category': 'restaurant', 'address': 'Besant Nagar, Chennai, Tamil Nadu 600090', 'lat': 13.0000, 'lon': 80.2667},

        {'dest_id': 'bengaluru001', 'name': 'Lalbagh Botanical Garden', 'category': 'attraction', 'address': 'Mavalli, Bengaluru, Karnataka 560004', 'lat': 12.9507, 'lon': 77.5848},
        {'dest_id': 'bengaluru001', 'name': 'Cubbon Park', 'category': 'attraction', 'address': 'Kasturba Road, Bengaluru, Karnataka 560001', 'lat': 12.9757, 'lon': 77.5929},
        {'dest_id': 'bengaluru001', 'name': 'Bangalore Palace', 'category': 'attraction', 'address': 'Palace Rd, Vasanth Nagar, Bengaluru, Karnataka 560052', 'lat': 12.9988, 'lon': 77.5921},
        {'dest_id': 'bengaluru001', 'name': 'Mavalli Tiffin Rooms (MTR)', 'category': 'restaurant', 'address': '14, Lalbagh Road, Mavalli, Bengaluru, Karnataka 560027', 'lat': 12.9555, 'lon': 77.5822},

        {'dest_id': 'hyderabad001', 'name': 'Charminar', 'category': 'attraction', 'address': 'Char Kaman, Ghansi Bazaar, Hyderabad, Telangana 500002', 'lat': 17.3616, 'lon': 78.4747},
        {'dest_id': 'hyderabad001', 'name': 'Golconda Fort', 'category': 'attraction', 'address': 'Ibrahim Bagh, Hyderabad, Telangana 500008', 'lat': 17.3833, 'lon': 78.4011},
        {'dest_id': 'hyderabad001', 'name': 'Ramoji Film City', 'category': 'attraction', 'address': 'Anaspur Village, Hayathnagar Mandal, Hyderabad, Telangana 501512', 'lat': 17.2544, 'lon': 78.6811},
        {'dest_id': 'hyderabad001', 'name': 'Paradise Biryani', 'category': 'restaurant', 'address': 'SD Road, Paradise Circle, Secunderabad, Telangana 500003', 'lat': 17.4425, 'lon': 78.4983},

        # --- International - Asia & Oceania ---
        {'dest_id': 'kyoto001', 'name': 'Kinkaku-ji (Golden Pavilion)', 'category': 'attraction', 'address': '1 Kinkakujicho, Kita Ward, Kyoto, 603-8361, Japan', 'lat': 35.0394, 'lon': 135.7292},
        {'dest_id': 'kyoto001', 'name': 'Fushimi Inari-taisha Shrine', 'category': 'attraction', 'address': '68 Fukakusa Yabunouchicho, Fushimi Ward, Kyoto, 612-0882, Japan', 'lat': 34.9671, 'lon': 135.7727},
        {'dest_id': 'kyoto001', 'name': 'Arashiyama Bamboo Grove', 'category': 'attraction', 'address': 'Sagatenryuji Susukinobabacho, Ukyo Ward, Kyoto, 616-8385, Japan', 'lat': 35.0175, 'lon': 135.6670},
        {'dest_id': 'kyoto001', 'name': 'Kikunoi Roan', 'category': 'restaurant', 'address': '118 Saitocho, Shimogyo Ward, Kyoto, 600-8012, Japan', 'lat': 35.0022, 'lon': 135.7719},

        {'dest_id': 'tokyo001', 'name': 'Senso-ji Temple', 'category': 'attraction', 'address': '2 Chome-3-1 Asakusa, Taito City, Tokyo 111-0032, Japan', 'lat': 35.7148, 'lon': 139.7967},
        {'dest_id': 'tokyo001', 'name': 'Shibuya Crossing', 'category': 'attraction', 'address': '2 Chome-2-1 Dogenzaka, Shibuya City, Tokyo 150-0043, Japan', 'lat': 35.6595, 'lon': 139.7005},
        {'dest_id': 'tokyo001', 'name': 'Tokyo Skytree', 'category': 'attraction', 'address': '1 Chome-1-2 Oshiage, Sumida City, Tokyo 131-0045, Japan', 'lat': 35.7101, 'lon': 139.8107},
        {'dest_id': 'tokyo001', 'name': 'Sukiyabashi Jiro', 'category': 'restaurant', 'address': '4-2-15 Ginza, Chuo City, Tokyo 104-0061, Japan', 'lat': 35.6719, 'lon': 139.7643},

        {'dest_id': 'bali001', 'name': 'Uluwatu Temple', 'category': 'attraction', 'address': 'Pecatu, South Kuta, Badung Regency, Bali, Indonesia', 'lat': -8.8291, 'lon': 115.0849},
        {'dest_id': 'bali001', 'name': 'Tanah Lot Temple', 'category': 'attraction', 'address': 'Beraban, Kediri, Tabanan Regency, Bali, Indonesia', 'lat': -8.6212, 'lon': 115.0869},
        {'dest_id': 'bali001', 'name': 'Tegallalang Rice Terraces', 'category': 'attraction', 'address': 'Jl. Raya Tegallalang, Tegallalang, Gianyar, Bali, Indonesia', 'lat': -8.4311, 'lon': 115.2779},
        {'dest_id': 'bali001', 'name': 'Mozaic Restaurant Gastronomique', 'category': 'restaurant', 'address': 'Jl. Raya Sanggingan, Kedewatan, Ubud, Gianyar, Bali 80571, Indonesia', 'lat': -8.4970, 'lon': 115.2530},

        {'dest_id': 'bkk001', 'name': 'The Grand Palace', 'category': 'attraction', 'address': 'Na Phra Lan Rd, Phra Borom Maha Ratchawang, Phra Nakhon, Bangkok 10200, Thailand', 'lat': 13.7499, 'lon': 100.4913},
        {'dest_id': 'bkk001', 'name': 'Wat Arun Ratchawararam', 'category': 'attraction', 'address': '158 Wang Doem Rd, Wat Arun, Bangkok Yai, Bangkok 10600, Thailand', 'lat': 13.7437, 'lon': 100.4889},
        {'dest_id': 'bkk001', 'name': 'Chatuchak Weekend Market', 'category': 'attraction', 'address': 'Kamphaeng Phet 2 Rd, Chatuchak, Bangkok 10900, Thailand', 'lat': 13.8011, 'lon': 100.5500},
        {'dest_id': 'bkk001', 'name': 'Gaggan Anand', 'category': 'restaurant', 'address': '68/9 Soi Langsuan, Ploenchit Road, Lumpini, Bangkok 10330, Thailand', 'lat': 13.7400, 'lon': 100.5450},

        {'dest_id': 'phuket001', 'name': 'Big Buddha Phuket', 'category': 'attraction', 'address': 'Karon, Mueang Phuket District, Phuket 83100, Thailand', 'lat': 7.8279, 'lon': 98.3126},
        {'dest_id': 'phuket001', 'name': 'Patong Beach', 'category': 'attraction', 'address': 'Patong, Kathu District, Phuket, Thailand', 'lat': 7.8931, 'lon': 98.2957},
        {'dest_id': 'phuket001', 'name': 'Phi Phi Islands', 'category': 'attraction', 'address': 'Mueang Krabi District, Krabi, Thailand', 'lat': 7.7408, 'lon': 98.7786},
        {'dest_id': 'phuket001', 'name': 'Mom Tri\'s Kitchen', 'category': 'restaurant', 'address': '12 Kata Noi Road, Karon, Mueang Phuket District, Phuket 83100, Thailand', 'lat': 7.8080, 'lon': 98.2980},

        {'dest_id': 'singapore001', 'name': 'Gardens by the Bay', 'category': 'attraction', 'address': '18 Marina Gardens Dr, Singapore 018953', 'lat': 1.2816, 'lon': 103.8636},
        {'dest_id': 'singapore001', 'name': 'Marina Bay Sands', 'category': 'attraction', 'address': '10 Bayfront Ave, Singapore 018956', 'lat': 1.2838, 'lon': 103.8600},
        {'dest_id': 'singapore001', 'name': 'Sentosa Island', 'category': 'attraction', 'address': 'Sentosa Island, Singapore', 'lat': 1.2494, 'lon': 103.8303},
        {'dest_id': 'singapore001', 'name': 'Lau Pa Sat', 'category': 'restaurant', 'address': '18 Raffles Quay, Singapore 048582', 'lat': 1.2798, 'lon': 103.8504},

        {'dest_id': 'seoul001', 'name': 'Gyeongbokgung Palace', 'category': 'attraction', 'address': '161 Sajik-ro, Jongno-gu, Seoul, South Korea', 'lat': 37.5796, 'lon': 126.9770},
        {'dest_id': 'seoul001', 'name': 'N Seoul Tower', 'category': 'attraction', 'address': '105 Namsangongwon-gil, Yongsan-gu, Seoul, South Korea', 'lat': 37.5512, 'lon': 126.9882},
        {'dest_id': 'seoul001', 'name': 'Myeongdong Market', 'category': 'attraction', 'address': 'Myeongdong-gil, Jung-gu, Seoul, South Korea', 'lat': 37.5639, 'lon': 126.9840},
        {'dest_id': 'seoul001', 'name': 'Mingles', 'category': 'restaurant', 'address': '757 Seolleung-ro, Gangnam-gu, Seoul, South Korea', 'lat': 37.5222, 'lon': 127.0396},

        {'dest_id': 'siemreap001', 'name': 'Angkor Wat', 'category': 'attraction', 'address': 'Krong Siem Reap, Cambodia', 'lat': 13.4125, 'lon': 103.8667},
        {'dest_id': 'siemreap001', 'name': 'Bayon Temple', 'category': 'attraction', 'address': 'Angkor Thom, Krong Siem Reap, Cambodia', 'lat': 13.4414, 'lon': 103.8590},
        {'dest_id': 'siemreap001', 'name': 'Ta Prohm', 'category': 'attraction', 'address': 'Angkor Archeological Park, Krong Siem Reap, Cambodia', 'lat': 13.4349, 'lon': 103.8893},
        {'dest_id': 'siemreap001', 'name': 'Malis Restaurant', 'category': 'restaurant', 'address': 'Pokambor Ave, Krong Siem Reap, Cambodia', 'lat': 13.3590, 'lon': 103.8540},

        {'dest_id': 'beijing001', 'name': 'Forbidden City', 'category': 'attraction', 'address': '4 Jingshan Front St, Dongcheng, Beijing, China', 'lat': 39.9163, 'lon': 116.3972},
        {'dest_id': 'beijing001', 'name': 'Great Wall at Mutianyu', 'category': 'attraction', 'address': 'Mutianyu Rd, Huairou District, Beijing, China', 'lat': 40.4316, 'lon': 116.5684},
        {'dest_id': 'beijing001', 'name': 'Temple of Heaven', 'category': 'attraction', 'address': '1 Tiantan E Rd, Dongcheng, Beijing, China', 'lat': 39.8822, 'lon': 116.4066},
        {'dest_id': 'beijing001', 'name': 'Da Dong Roast Duck', 'category': 'restaurant', 'address': '1-2/F, Nanxincang International Tower, 22A Dongsishitiao, Dongcheng, Beijing, China', 'lat': 39.9281, 'lon': 116.4320},

        {'dest_id': 'sydney001', 'name': 'Sydney Opera House', 'category': 'attraction', 'address': 'Bennelong Point, Sydney NSW 2000, Australia', 'lat': -33.8568, 'lon': 151.2153},
        {'dest_id': 'sydney001', 'name': 'Sydney Harbour Bridge', 'category': 'attraction', 'address': 'Sydney Harbour Bridge, Sydney NSW, Australia', 'lat': -33.8523, 'lon': 151.2108},
        {'dest_id': 'sydney001', 'name': 'Bondi Beach', 'category': 'attraction', 'address': 'Bondi Beach, NSW 2026, Australia', 'lat': -33.8914, 'lon': 151.2778},
        {'dest_id': 'sydney001', 'name': 'Quay Restaurant', 'category': 'restaurant', 'address': 'Upper Level, Overseas Passenger Terminal, The Rocks, Sydney NSW 2000, Australia', 'lat': -33.8587, 'lon': 151.2100},

        {'dest_id': 'hanoi001', 'name': 'Hoan Kiem Lake', 'category': 'attraction', 'address': 'Hoan Kiem, Hanoi, Vietnam', 'lat': 21.0287, 'lon': 105.8524},
        {'dest_id': 'hanoi001', 'name': 'Ho Chi Minh Mausoleum', 'category': 'attraction', 'address': '8 Hung Vuong, Dien Ban, Ba Dinh, Hanoi, Vietnam', 'lat': 21.0368, 'lon': 105.8349},
        {'dest_id': 'hanoi001', 'name': 'The Old Quarter', 'category': 'attraction', 'address': 'Hoan Kiem, Hanoi, Vietnam', 'lat': 21.0333, 'lon': 105.8500},
        {'dest_id': 'hanoi001', 'name': 'Bun Cha Huong Lien', 'category': 'restaurant', 'address': '24 Le Van Huu, Phan Chu Trinh, Hai Ba Trung, Hanoi, Vietnam', 'lat': 21.0163, 'lon': 105.8520},

        {'dest_id': 'kathmandu001', 'name': 'Boudhanath Stupa', 'category': 'attraction', 'address': 'Buddha Stupa, Kathmandu 44600, Nepal', 'lat': 27.7215, 'lon': 85.3621},
        {'dest_id': 'kathmandu001', 'name': 'Pashupatinath Temple', 'category': 'attraction', 'address': 'Pashupati Nath Road, Kathmandu 44600, Nepal', 'lat': 27.7107, 'lon': 85.3486},
        {'dest_id': 'kathmandu001', 'name': 'Swayambhunath Stupa', 'category': 'attraction', 'address': 'Swayambhu, Kathmandu 44600, Nepal', 'lat': 27.7149, 'lon': 85.2905},
        {'dest_id': 'kathmandu001', 'name': 'Krishnarpan Restaurant', 'category': 'restaurant', 'address': 'Dwarika\'s Hotel, Battisputali, Kathmandu 44600, Nepal', 'lat': 27.7088, 'lon': 85.3438},

        {'dest_id': 'busan001', 'name': 'Haeundae Beach', 'category': 'attraction', 'address': 'Haeundae-gu, Busan, South Korea', 'lat': 35.1587, 'lon': 129.1604},
        {'dest_id': 'busan001', 'name': 'Gamcheon Culture Village', 'category': 'attraction', 'address': '203 Gamnae 2-ro, Saha-gu, Busan, South Korea', 'lat': 35.0970, 'lon': 129.0108},
        {'dest_id': 'busan001', 'name': 'Haedong Yonggungsa Temple', 'category': 'attraction', 'address': '86 Yonggung-gil, Gijang-gun, Busan, South Korea', 'lat': 35.1889, 'lon': 129.2225},
        {'dest_id': 'busan001', 'name': 'Jagalchi Fish Market', 'category': 'restaurant', 'address': '52 Jagalchihaean-ro, Jung-gu, Busan, South Korea', 'lat': 35.0971, 'lon': 129.0301},

        {'dest_id': 'melbourne001', 'name': 'Federation Square', 'category': 'attraction', 'address': 'Swanston St & Flinders St, Melbourne VIC 3000, Australia', 'lat': -37.8179, 'lon': 144.9691},
        {'dest_id': 'melbourne001', 'name': 'Queen Victoria Market', 'category': 'attraction', 'address': 'Queen St, Melbourne VIC 3000, Australia', 'lat': -37.8076, 'lon': 144.9568},
        {'dest_id': 'melbourne001', 'name': 'Royal Botanic Gardens Victoria', 'category': 'attraction', 'address': 'Birdwood Ave, South Yarra VIC 3141, Australia', 'lat': -37.8304, 'lon': 144.9796},
        {'dest_id': 'melbourne001', 'name': 'Attica', 'category': 'restaurant', 'address': '74 Glen Eira Rd, Ripponlea VIC 3185, Australia', 'lat': -37.8812, 'lon': 144.9968},

        {'dest_id': 'halong001', 'name': 'Sung Sot Cave', 'category': 'attraction', 'address': 'Bo Hon Island, Ha Long Bay, Vietnam', 'lat': 20.8920, 'lon': 107.0870},
        {'dest_id': 'halong001', 'name': 'Ti Top Island', 'category': 'attraction', 'address': 'Ha Long Bay, Quang Ninh Province, Vietnam', 'lat': 20.8572, 'lon': 107.0811},
        {'dest_id': 'halong001', 'name': 'Cat Ba Island', 'category': 'attraction', 'address': 'Cat Hai District, Hai Phong, Vietnam', 'lat': 20.7833, 'lon': 106.9667},
        {'dest_id': 'halong001', 'name': 'Cua Vang Restaurant', 'category': 'restaurant', 'address': 'Tuan Chau, Ha Long City, Quang Ninh, Vietnam', 'lat': 20.9167, 'lon': 106.9833},

        {'dest_id': 'shanghai001', 'name': 'The Bund', 'category': 'attraction', 'address': 'Zhongshan East 1st Rd, Huangpu, Shanghai, China', 'lat': 31.2381, 'lon': 121.4912},
        {'dest_id': 'shanghai001', 'name': 'Yu Garden', 'category': 'attraction', 'address': '279 Yuyuan Old St, Huangpu, Shanghai, China', 'lat': 31.2285, 'lon': 121.4927},
        {'dest_id': 'shanghai001', 'name': 'Shanghai Tower', 'category': 'attraction', 'address': '501 Yincheng Middle Rd, Lujiazui, Pudong, Shanghai, China', 'lat': 31.2339, 'lon': 121.5059},
        {'dest_id': 'shanghai001', 'name': 'Ultraviolet by Paul Pairet', 'category': 'restaurant', 'address': 'c/o Bund18, 6/F, 18 Zhongshan Dong Yi Lu, Huangpu, Shanghai, China', 'lat': 31.2393, 'lon': 121.4880},

        {'dest_id': 'kl001', 'name': 'Petronas Twin Towers', 'category': 'attraction', 'address': 'Kuala Lumpur City Centre, 50088 Kuala Lumpur, Federal Territory of Kuala Lumpur, Malaysia', 'lat': 3.1578, 'lon': 101.7119},
        {'dest_id': 'kl001', 'name': 'Batu Caves', 'category': 'attraction', 'address': 'Gombak, 68100 Batu Caves, Selangor, Malaysia', 'lat': 3.2379, 'lon': 101.6840},
        {'dest_id': 'kl001', 'name': 'Menara Kuala Lumpur', 'category': 'attraction', 'address': '2 Jalan Punchak, Off, Jalan P. Ramlee, 50250 Kuala Lumpur, Malaysia', 'lat': 3.1528, 'lon': 101.7038},
        {'dest_id': 'kl001', 'name': 'Jalan Alor Food Street', 'category': 'restaurant', 'address': 'Jalan Alor, Bukit Bintang, 50200 Kuala Lumpur, Malaysia', 'lat': 3.1451, 'lon': 101.7088},

        {'dest_id': 'chiangmai001', 'name': 'Wat Phra That Doi Suthep', 'category': 'attraction', 'address': 'Mueang Chiang Mai District, Chiang Mai 50200, Thailand', 'lat': 18.8050, 'lon': 98.9216},
        {'dest_id': 'chiangmai001', 'name': 'Elephant Nature Park', 'category': 'attraction', 'address': '1 Ratmakka Rd, Phra Sing, Mueang Chiang Mai District, Chiang Mai 50200, Thailand', 'lat': 19.2990, 'lon': 98.8550},
        {'dest_id': 'chiangmai001', 'name': 'Chiang Mai Night Bazaar', 'category': 'attraction', 'address': 'Changklan Rd, Chang Moi, Mueang Chiang Mai District, Chiang Mai 50100, Thailand', 'lat': 18.7881, 'lon': 98.9959},
        {'dest_id': 'chiangmai001', 'name': 'Dash! Restaurant and Bar', 'category': 'restaurant', 'address': '38/2 Moon Muang Rd, Soi 1, Phra Sing, Mueang Chiang Mai District, Chiang Mai 50200, Thailand', 'lat': 18.7845, 'lon': 98.9910},

        {'dest_id': 'fiji001', 'name': 'Garden of the Sleeping Giant', 'category': 'attraction', 'address': 'Wailoko Rd, Nadi, Fiji', 'lat': -17.7167, 'lon': 177.4667},
        {'dest_id': 'fiji001', 'name': 'Sabeto Hot Springs and Mud Pool', 'category': 'attraction', 'address': 'Sabeto, Nadi, Fiji', 'lat': -17.7000, 'lon': 177.5000},
        {'dest_id': 'fiji001', 'name': 'Malamala Beach Club', 'category': 'attraction', 'address': 'Malamala Island, Mamanuca Islands, Fiji', 'lat': -17.7667, 'lon': 177.3167},
        {'dest_id': 'fiji001', 'name': 'Taste Fiji Kitchen', 'category': 'restaurant', 'address': 'Namaka, Nadi, Fiji', 'lat': -17.7500, 'lon': 177.4667},

        {'dest_id': 'uluru001', 'name': 'Uluru-Kata Tjuta National Park', 'category': 'attraction', 'address': 'Uluru, Northern Territory, Australia', 'lat': -25.3444, 'lon': 131.0369},
        {'dest_id': 'uluru001', 'name': 'Kata Tjuta (The Olgas)', 'category': 'attraction', 'address': 'Petermann, NT 0872, Australia', 'lat': -25.2975, 'lon': 130.7328},
        {'dest_id': 'uluru001', 'name': 'Field of Light Uluru', 'category': 'attraction', 'address': '173 Yulara Dr, Yulara NT 0872, Australia', 'lat': -25.2447, 'lon': 130.9839},
        {'dest_id': 'uluru001', 'name': 'Arnguli Grill & Restaurant', 'category': 'restaurant', 'address': 'Sails in the Desert Hotel, Yulara Dr, Yulara NT 0872, Australia', 'lat': -25.2400, 'lon': 130.9850},

        {'dest_id': 'osaka001', 'name': 'Osaka Castle', 'category': 'attraction', 'address': '1-1 Osakajo, Chuo Ward, Osaka, 540-0002, Japan', 'lat': 34.6873, 'lon': 135.5262},
        {'dest_id': 'osaka001', 'name': 'Dotonbori', 'category': 'attraction', 'address': 'Dotonbori, Chuo Ward, Osaka, 542-0071, Japan', 'lat': 34.6687, 'lon': 135.5013},
        {'dest_id': 'osaka001', 'name': 'Universal Studios Japan', 'category': 'attraction', 'address': '2 Chome-1-33 Sakurajima, Konohana Ward, Osaka, 554-0031, Japan', 'lat': 34.6656, 'lon': 135.4323},
        {'dest_id': 'osaka001', 'name': 'Kiji (Okonomiyaki)', 'category': 'restaurant', 'address': '1 Chome-9-20 Oyodona, Kita Ward, Osaka, 531-0076, Japan', 'lat': 34.7045, 'lon': 135.4947},

        {'dest_id': 'hochiminh001', 'name': 'War Remnants Museum', 'category': 'attraction', 'address': '28 Vo Van Tan, Ward 6, District 3, Ho Chi Minh City, Vietnam', 'lat': 10.7794, 'lon': 106.6925},
        {'dest_id': 'hochiminh001', 'name': 'Cu Chi Tunnels', 'category': 'attraction', 'address': 'Phu Hiep, Cu Chi District, Ho Chi Minh City, Vietnam', 'lat': 11.1444, 'lon': 106.4633},
        {'dest_id': 'hochiminh001', 'name': 'Ben Thanh Market', 'category': 'attraction', 'address': 'Le Loi, Ben Thanh Ward, District 1, Ho Chi Minh City, Vietnam', 'lat': 10.7725, 'lon': 106.6983},
        {'dest_id': 'hochiminh001', 'name': 'Cuc Gach Quan', 'category': 'restaurant', 'address': '10 Dang Tat, Tan Dinh, District 1, Ho Chi Minh City, Vietnam', 'lat': 10.7895, 'lon': 106.6908},

        {'dest_id': 'manila001', 'name': 'Intramuros', 'category': 'attraction', 'address': 'Intramuros, Manila, Metro Manila, Philippines', 'lat': 14.5895, 'lon': 120.9750},
        {'dest_id': 'manila001', 'name': 'San Agustin Church', 'category': 'attraction', 'address': 'General Luna St, Intramuros, Manila, 1002 Metro Manila, Philippines', 'lat': 14.5889, 'lon': 120.9756},
        {'dest_id': 'manila001', 'name': 'Rizal Park', 'category': 'attraction', 'address': 'Roxas Blvd, Ermita, Manila, 1000 Metro Manila, Philippines', 'lat': 14.5825, 'lon': 120.9786},
        {'dest_id': 'manila001', 'name': 'Aristocrat Restaurant', 'category': 'restaurant', 'address': '432, 1004 San Andres St, Malate, Manila, 1004 Metro Manila, Philippines', 'lat': 14.5684, 'lon': 120.9880},

        {'dest_id': 'boracay001', 'name': 'White Beach', 'category': 'attraction', 'address': 'White Beach, Boracay, Malay, Aklan, Philippines', 'lat': 11.9631, 'lon': 121.9255},
        {'dest_id': 'boracay001', 'name': 'D\'Mall Boracay', 'category': 'attraction', 'address': 'D\'Mall, Station 2, Boracay, Malay, Aklan, Philippines', 'lat': 11.9626, 'lon': 121.9261},
        {'dest_id': 'boracay001', 'name': 'Ariel\'s Point', 'category': 'attraction', 'address': 'Batason, Buruanga, Aklan, Philippines', 'lat': 11.9167, 'lon': 121.9000},
        {'dest_id': 'boracay001', 'name': 'The Sunny Side Cafe', 'category': 'restaurant', 'address': 'Station 3, White Beach, Boracay, Malay, Aklan, Philippines', 'lat': 11.9567, 'lon': 121.9300},

        {'dest_id': 'palawan001', 'name': 'Puerto Princesa Subterranean River', 'category': 'attraction', 'address': 'Puerto Princesa, Palawan, Philippines', 'lat': 10.1989, 'lon': 118.9263},
        {'dest_id': 'palawan001', 'name': 'El Nido', 'category': 'attraction', 'address': 'El Nido, Palawan, Philippines', 'lat': 11.2000, 'lon': 119.4167},
        {'dest_id': 'palawan001', 'name': 'Coron', 'category': 'attraction', 'address': 'Coron, Palawan, Philippines', 'lat': 12.0000, 'lon': 120.2000},
        {'dest_id': 'palawan001', 'name': 'Kalui Restaurant', 'category': 'restaurant', 'address': '369 Rizal Ave, Puerto Princesa, 5300 Palawan, Philippines', 'lat': 9.7431, 'lon': 118.7428},

        {'dest_id': 'auckland001', 'name': 'Sky Tower', 'category': 'attraction', 'address': 'Victoria St W, Auckland CBD, Auckland 1010, New Zealand', 'lat': -36.8483, 'lon': 174.7622},
        {'dest_id': 'auckland001', 'name': 'Waiheke Island', 'category': 'attraction', 'address': 'Waiheke Island, Auckland, New Zealand', 'lat': -36.7833, 'lon': 175.0833},
        {'dest_id': 'auckland001', 'name': 'Auckland War Memorial Museum', 'category': 'attraction', 'address': 'Parnell, Auckland 1010, New Zealand', 'lat': -36.8604, 'lon': 174.7779},
        {'dest_id': 'auckland001', 'name': 'The Grove', 'category': 'restaurant', 'address': 'Saint Patricks Square, Wyndham St, Auckland CBD, Auckland 1010, New Zealand', 'lat': -36.8471, 'lon': 174.7645},

        {'dest_id': 'christchurch001', 'name': 'Christchurch Botanic Gardens', 'category': 'attraction', 'address': 'Rolleston Ave, Christchurch Central City, Christchurch 8013, New Zealand', 'lat': -43.5300, 'lon': 172.6200},
        {'dest_id': 'christchurch001', 'name': 'Canterbury Museum', 'category': 'attraction', 'address': 'Rolleston Ave, Christchurch Central City, Christchurch 8013, New Zealand', 'lat': -43.5308, 'lon': 172.6283},
        {'dest_id': 'christchurch001', 'name': 'Cardboard Cathedral', 'category': 'attraction', 'address': '234 Hereford St, Christchurch Central City, Christchurch 8011, New Zealand', 'lat': -43.5333, 'lon': 172.6417},
        {'dest_id': 'christchurch001', 'name': 'The Bicycle Thief', 'category': 'restaurant', 'address': '136 Oxford Terrace, Christchurch Central City, Christchurch 8011, New Zealand', 'lat': -43.5317, 'lon': 172.6367},

        {'dest_id': 'greatbarrier001', 'name': 'Cairns Esplanade', 'category': 'attraction', 'address': 'Cairns City, QLD 4870, Australia', 'lat': -16.9186, 'lon': 145.7781},
        {'dest_id': 'greatbarrier001', 'name': 'Daintree Rainforest', 'category': 'attraction', 'address': 'Cape Tribulation, QLD 4873, Australia', 'lat': -16.0833, 'lon': 145.4167},
        {'dest_id': 'greatbarrier001', 'name': 'Kuranda Scenic Railway', 'category': 'attraction', 'address': 'Bunda St, Cairns City QLD 4870, Australia', 'lat': -16.9231, 'lon': 145.7725},
        {'dest_id': 'greatbarrier001', 'name': 'Nu Nu Restaurant', 'category': 'restaurant', 'address': '1 Veivers Rd, Palm Cove QLD 4879, Australia', 'lat': -16.7423, 'lon': 145.6690},

        {'dest_id': 'perth001', 'name': 'Kings Park and Botanic Garden', 'category': 'attraction', 'address': 'Fraser Ave, Perth WA 6005, Australia', 'lat': -31.9600, 'lon': 115.8450},
        {'dest_id': 'perth001', 'name': 'Cottesloe Beach', 'category': 'attraction', 'address': 'Cottesloe, WA 6011, Australia', 'lat': -31.9933, 'lon': 115.7533},
        {'dest_id': 'perth001', 'name': 'Rottnest Island', 'category': 'attraction', 'address': 'Rottnest Island, WA 6161, Australia', 'lat': -32.0000, 'lon': 115.5000},
        {'dest_id': 'perth001', 'name': 'Wildflower', 'category': 'restaurant', 'address': 'COMO The Treasury, 1 Cathedral Ave, Perth WA 6000, Australia', 'lat': -31.9547, 'lon': 115.8600},

        {'dest_id': 'xian001', 'name': 'Terracotta Army', 'category': 'attraction', 'address': 'Lintong District, Xi\'an, Shaanxi, China', 'lat': 34.3853, 'lon': 109.2741},
        {'dest_id': 'xian001', 'name': 'Xi\'an City Wall', 'category': 'attraction', 'address': 'Andingmen, Beilin, Xi\'an, Shaanxi, China', 'lat': 34.2570, 'lon': 108.9530},
        {'dest_id': 'xian001', 'name': 'Muslim Quarter', 'category': 'attraction', 'address': 'Beiyuanmen, Lianhu, Xi\'an, Shaanxi, China', 'lat': 34.2667, 'lon': 108.9450},
        {'dest_id': 'xian001', 'name': 'De Fa Chang Dumpling Restaurant', 'category': 'restaurant', 'address': '3 West St, Beilin, Xi\'an, Shaanxi, China', 'lat': 34.2600, 'lon': 108.9400},

        {'dest_id': 'luangprabang001', 'name': 'Kuang Si Falls', 'category': 'attraction', 'address': 'Luang Prabang, Laos', 'lat': 19.7492, 'lon': 101.9908},
        {'dest_id': 'luangprabang001', 'name': 'Mount Phousi', 'category': 'attraction', 'address': 'Luang Prabang, Laos', 'lat': 19.8917, 'lon': 102.1383},
        {'dest_id': 'luangprabang001', 'name': 'Royal Palace Museum', 'category': 'attraction', 'address': '27 Ounheun Rd, Luang Prabang, Laos', 'lat': 19.8911, 'lon': 102.1367},
        {'dest_id': 'luangprabang001', 'name': 'Manda de Laos', 'category': 'restaurant', 'address': '10 Norrassan Road, Luang Prabang, Laos', 'lat': 19.8867, 'lon': 102.1333},

        {'dest_id': 'pokhara001', 'name': 'Phewa Lake', 'category': 'attraction', 'address': 'Pokhara, Nepal', 'lat': 28.2167, 'lon': 83.9500},
        {'dest_id': 'pokhara001', 'name': 'Sarangkot', 'category': 'attraction', 'address': 'Sarangkot, Pokhara, Nepal', 'lat': 28.2500, 'lon': 83.9167},
        {'dest_id': 'pokhara001', 'name': 'World Peace Pagoda', 'category': 'attraction', 'address': 'Pumdi Bhumdi, Pokhara, Nepal', 'lat': 28.2000, 'lon': 83.9333},
        {'dest_id': 'pokhara001', 'name': 'Moondance Restaurant', 'category': 'restaurant', 'address': 'Lakeside, Pokhara, Nepal', 'lat': 28.2167, 'lon': 83.9500},

        {'dest_id': 'paronepal001', 'name': 'Paro Taktsang (Tiger\'s Nest)', 'category': 'attraction', 'address': 'Taktsang Trail, Paro, Bhutan', 'lat': 27.4917, 'lon': 89.3633},
        {'dest_id': 'paronepal001', 'name': 'Rinpung Dzong', 'category': 'attraction', 'address': 'Paro, Bhutan', 'lat': 27.4167, 'lon': 89.4167},
        {'dest_id': 'paronepal001', 'name': 'Chele La Pass', 'category': 'attraction', 'address': 'Between Paro and Haa Valley, Bhutan', 'lat': 27.3500, 'lon': 89.3000},
        {'dest_id': 'paronepal001', 'name': 'Bukhari Restaurant', 'category': 'restaurant', 'address': 'Uma by COMO, Paro, Bhutan', 'lat': 27.4333, 'lon': 89.4167},

        {'dest_id': 'colombo001', 'name': 'Galle Face Green', 'category': 'attraction', 'address': 'Colombo, Sri Lanka', 'lat': 6.9200, 'lon': 79.8450},
        {'dest_id': 'colombo001', 'name': 'Gangaramaya Temple', 'category': 'attraction', 'address': '61 Sri Jinarathana Rd, Colombo 00200, Sri Lanka', 'lat': 6.9150, 'lon': 79.8550},
        {'dest_id': 'colombo001', 'name': 'National Museum of Colombo', 'category': 'attraction', 'address': 'Sir Marcus Fernando Mawatha, Colombo 00700, Sri Lanka', 'lat': 6.9033, 'lon': 79.8617},
        {'dest_id': 'colombo001', 'name': 'Ministry of Crab', 'category': 'restaurant', 'address': 'Old Dutch Hospital Complex, 04 Hospital St, Colombo 00100, Sri Lanka', 'lat': 6.9333, 'lon': 79.8450},

        {'dest_id': 'kandy001', 'name': 'Temple of the Sacred Tooth Relic', 'category': 'attraction', 'address': 'Sri Dalada Veediya, Kandy 20000, Sri Lanka', 'lat': 7.2936, 'lon': 80.6413},
        {'dest_id': 'kandy001', 'name': 'Kandy Lake', 'category': 'attraction', 'address': 'Kandy, Sri Lanka', 'lat': 7.2917, 'lon': 80.6400},
        {'dest_id': 'kandy001', 'name': 'Royal Botanical Gardens, Peradeniya', 'category': 'attraction', 'address': 'Peradeniya, Kandy, Sri Lanka', 'lat': 7.2667, 'lon': 80.6000},
        {'dest_id': 'kandy001', 'name': 'The Empire Cafe', 'category': 'restaurant', 'address': '21 Temple St, Kandy 20000, Sri Lanka', 'lat': 7.2933, 'lon': 80.6400},

        {'dest_id': 'maldives001', 'name': 'Malé Fish Market', 'category': 'attraction', 'address': 'Male, Maldives', 'lat': 4.1750, 'lon': 73.5083},
        {'dest_id': 'maldives001', 'name': 'Hukuru Miskiy (Old Friday Mosque)', 'category': 'attraction', 'address': 'Male, Maldives', 'lat': 4.1767, 'lon': 73.5117},
        {'dest_id': 'maldives001', 'name': 'Maafushi Island', 'category': 'attraction', 'address': 'Maafushi, Kaafu Atoll, Maldives', 'lat': 3.9333, 'lon': 73.4833},
        {'dest_id': 'maldives001', 'name': 'Ithaa Undersea Restaurant', 'category': 'restaurant', 'address': 'Conrad Rangali Island, Maldives', 'lat': 3.6167, 'lon': 72.7167},

        {'dest_id': 'jeju001', 'name': 'Seongsan Ilchulbong (Sunrise Peak)', 'category': 'attraction', 'address': 'Seogwipo, Jeju-do, South Korea', 'lat': 33.4581, 'lon': 126.9426},
        {'dest_id': 'jeju001', 'name': 'Hallasan National Park', 'category': 'attraction', 'address': 'Jeju-do, South Korea', 'lat': 33.3617, 'lon': 126.5292},
        {'dest_id': 'jeju001', 'name': 'Manjanggul Cave', 'category': 'attraction', 'address': '182 Manjanggul-gil, Gujwa-eup, Jeju-si, Jeju-do, South Korea', 'lat': 33.5283, 'lon': 126.7719},
        {'dest_id': 'jeju001', 'name': 'Donsadon', 'category': 'restaurant', 'address': '19, Uopyeong-ro, Jeju-si, Jeju-do, South Korea', 'lat': 33.5070, 'lon': 126.5220},

        {'dest_id': 'jakarta001', 'name': 'National Monument (Monas)', 'category': 'attraction', 'address': 'Gambir, Central Jakarta City, Jakarta, Indonesia', 'lat': -6.1754, 'lon': 106.8272},
        {'dest_id': 'jakarta001', 'name': 'Istiqlal Mosque', 'category': 'attraction', 'address': 'Jl. Taman Wijaya Kusuma, Ps. Baru, Sawah Besar, Central Jakarta City, Jakarta, Indonesia', 'lat': -6.1700, 'lon': 106.8300},
        {'dest_id': 'jakarta001', 'name': 'Kota Tua (Old Town)', 'category': 'attraction', 'address': 'Pinangsia, Tamansari, West Jakarta City, Jakarta, Indonesia', 'lat': -6.1352, 'lon': 106.8133},
        {'dest_id': 'jakarta001', 'name': 'Bandar Djakarta', 'category': 'restaurant', 'address': 'Pintu Timur, Taman Impian Jaya Ancol, Jl. Lodan Timur No.7, Ancol, Pademangan, North Jakarta City, Jakarta 14430, Indonesia', 'lat': -6.1214, 'lon': 106.8338},

        {'dest_id': 'taipei001', 'name': 'Taipei 101', 'category': 'attraction', 'address': 'No. 7, Section 5, Xinyi Rd, Xinyi District, Taipei City, Taiwan 110', 'lat': 25.0336, 'lon': 121.5645},
        {'dest_id': 'taipei001', 'name': 'National Palace Museum', 'category': 'attraction', 'address': 'No. 221, Sec 2, Zhi Shan Rd, Shilin District, Taipei City, Taiwan 111', 'lat': 25.1023, 'lon': 121.5484},
        {'dest_id': 'taipei001', 'name': 'Shilin Night Market', 'category': 'attraction', 'address': 'No. 101, Jihe Rd, Shilin District, Taipei City, Taiwan 111', 'lat': 25.0877, 'lon': 121.5244},
        {'dest_id': 'taipei001', 'name': 'Din Tai Fung (Xinyi)', 'category': 'restaurant', 'address': 'No. 194, Section 2, Xinyi Rd, Da’an District, Taipei City, Taiwan 106', 'lat': 25.0345, 'lon': 121.5288},

        {'dest_id': 'hongkong001', 'name': 'Victoria Peak', 'category': 'attraction', 'address': 'The Peak, Hong Kong', 'lat': 22.2759, 'lon': 114.1455},
        {'dest_id': 'hongkong001', 'name': 'Tian Tan Buddha (Big Buddha)', 'category': 'attraction', 'address': 'Ngong Ping, Lantau Island, Hong Kong', 'lat': 22.2540, 'lon': 113.9050},
        {'dest_id': 'hongkong001', 'name': 'Star Ferry', 'category': 'attraction', 'address': 'Tsim Sha Tsui, Hong Kong', 'lat': 22.2936, 'lon': 114.1691},
        {'dest_id': 'hongkong001', 'name': 'Tim Ho Wan', 'category': 'restaurant', 'address': '9 Fuk Wing St, Sham Shui Po, Hong Kong', 'lat': 22.3298, 'lon': 114.1613},

        {'dest_id': 'phnompenh001', 'name': 'Royal Palace', 'category': 'attraction', 'address': 'Samdach Sothearos Blvd (3), Phnom Penh, Cambodia', 'lat': 11.5645, 'lon': 104.9310},
        {'dest_id': 'phnompenh001', 'name': 'Tuol Sleng Genocide Museum', 'category': 'attraction', 'address': 'St 113, Phnom Penh, Cambodia', 'lat': 11.5494, 'lon': 104.9175},
        {'dest_id': 'phnompenh001', 'name': 'Choeung Ek Genocidal Center', 'category': 'attraction', 'address': 'Phnom Penh, Cambodia', 'lat': 11.4844, 'lon': 104.9022},
        {'dest_id': 'phnompenh001', 'name': 'Romdeng', 'category': 'restaurant', 'address': '74 Oknha Ket St. (174), Phnom Penh, Cambodia', 'lat': 11.5658, 'lon': 104.9222},

        {'dest_id': 'guilin001', 'name': 'Li River Cruise', 'category': 'attraction', 'address': 'Guilin, Guangxi, China', 'lat': 25.2809, 'lon': 110.2872},
        {'dest_id': 'guilin001', 'name': 'Reed Flute Cave', 'category': 'attraction', 'address': 'Lingui District, Guilin, Guangxi, China', 'lat': 25.3000, 'lon': 110.2333},
        {'dest_id': 'guilin001', 'name': 'Yangshuo', 'category': 'attraction', 'address': 'Yangshuo, Guilin, Guangxi, China', 'lat': 24.7761, 'lon': 110.4912},
        {'dest_id': 'guilin001', 'name': 'McFound Restaurant', 'category': 'restaurant', 'address': '8 Zhongshan Middle Rd, Xiufeng, Guilin, Guangxi, China', 'lat': 25.2811, 'lon': 110.2889},

        {'dest_id': 'tashkent001', 'name': 'Chorsu Bazaar', 'category': 'attraction', 'address': 'Tashkent, Uzbekistan', 'lat': 41.3264, 'lon': 69.2345},
        {'dest_id': 'tashkent001', 'name': 'Amir Timur Museum', 'category': 'attraction', 'address': '1 Amir Timur Avenue, Tashkent, Uzbekistan', 'lat': 41.3128, 'lon': 69.2783},
        {'dest_id': 'tashkent001', 'name': 'Tashkent Metro', 'category': 'attraction', 'address': 'Tashkent, Uzbekistan', 'lat': 41.2995, 'lon': 69.2401},
        {'dest_id': 'tashkent001', 'name': 'Plov Center', 'category': 'restaurant', 'address': '1 Iftixor ko\'chasi, Tashkent, Uzbekistan', 'lat': 41.3411, 'lon': 69.2894},

        {'dest_id': 'wellington001', 'name': 'Te Papa Tongarewa Museum', 'category': 'attraction', 'address': '55 Cable St, Te Aro, Wellington 6011, New Zealand', 'lat': -41.2905, 'lon': 174.7818},
        {'dest_id': 'wellington001', 'name': 'Wellington Cable Car', 'category': 'attraction', 'address': '280 Lambton Quay, Wellington 6011, New Zealand', 'lat': -41.2850, 'lon': 174.7750},
        {'dest_id': 'wellington001', 'name': 'Mount Victoria Lookout', 'category': 'attraction', 'address': 'Lookout Rd, Hataitai, Wellington 6021, New Zealand', 'lat': -41.2958, 'lon': 174.7900},
        {'dest_id': 'wellington001', 'name': 'Logan Brown', 'category': 'restaurant', 'address': '192 Cuba St, Te Aro, Wellington 6011, New Zealand', 'lat': -41.2933, 'lon': 174.7744},

        {'dest_id': 'adelaide001', 'name': 'Adelaide Central Market', 'category': 'attraction', 'address': '44-60 Gouger St, Adelaide SA 5000, Australia', 'lat': -34.9300, 'lon': 138.5950},
        {'dest_id': 'adelaide001', 'name': 'Adelaide Botanic Garden', 'category': 'attraction', 'address': 'North Terrace, Adelaide SA 5000, Australia', 'lat': -34.9183, 'lon': 138.6083},
        {'dest_id': 'adelaide001', 'name': 'Barossa Valley', 'category': 'attraction', 'address': 'Barossa Valley, SA, Australia', 'lat': -34.5333, 'lon': 138.9500},
        {'dest_id': 'adelaide001', 'name': 'Africola', 'category': 'restaurant', 'address': '4 East Terrace, Adelaide SA 5000, Australia', 'lat': -34.9250, 'lon': 138.6117},

                # --- International - Europe ---
        {'dest_id': 'paris001', 'name': 'Eiffel Tower', 'category': 'attraction', 'address': 'Champ de Mars, 5 Av. Anatole France, 75007 Paris, France', 'lat': 48.8584, 'lon': 2.2945},
        {'dest_id': 'paris001', 'name': 'Louvre Museum', 'category': 'attraction', 'address': 'Rue de Rivoli, 75001 Paris, France', 'lat': 48.8606, 'lon': 2.3376},
        {'dest_id': 'paris001', 'name': 'Notre-Dame Cathedral', 'category': 'attraction', 'address': '6 Parvis Notre-Dame - Pl. Jean-Paul II, 75004 Paris, France', 'lat': 48.8530, 'lon': 2.3499},
        {'dest_id': 'paris001', 'name': 'Le Procope', 'category': 'restaurant', 'address': '13 Rue de l\'Ancienne Comédie, 75006 Paris, France', 'lat': 48.8533, 'lon': 2.3387},

        {'dest_id': 'rome001', 'name': 'Colosseum', 'category': 'attraction', 'address': 'Piazza del Colosseo, 1, 00184 Roma RM, Italy', 'lat': 41.8902, 'lon': 12.4922},
        {'dest_id': 'rome001', 'name': 'Pantheon', 'category': 'attraction', 'address': 'Piazza della Rotonda, 00186 Roma RM, Italy', 'lat': 41.8986, 'lon': 12.4769},
        {'dest_id': 'rome001', 'name': 'Trevi Fountain', 'category': 'attraction', 'address': 'Piazza di Trevi, 00187 Roma RM, Italy', 'lat': 41.9009, 'lon': 12.4833},
        {'dest_id': 'rome001', 'name': 'Roscioli Salumeria con Cucina', 'category': 'restaurant', 'address': 'Via dei Giubbonari, 21, 00186 Roma RM, Italy', 'lat': 41.8943, 'lon': 12.4725},

        {'dest_id': 'london001', 'name': 'The British Museum', 'category': 'attraction', 'address': 'Great Russell St, London WC1B 3DG, UK', 'lat': 51.5194, 'lon': -0.1270},
        {'dest_id': 'london001', 'name': 'Tower of London', 'category': 'attraction', 'address': 'London EC3N 4AB, UK', 'lat': 51.5081, 'lon': -0.0759},
        {'dest_id': 'london001', 'name': 'Buckingham Palace', 'category': 'attraction', 'address': 'London SW1A 1AA, UK', 'lat': 51.5014, 'lon': -0.1419},
        {'dest_id': 'london001', 'name': 'Dishoom Covent Garden', 'category': 'restaurant', 'address': '12 Upper St Martin\'s Ln, London WC2H 9FB, UK', 'lat': 51.5126, 'lon': -0.1264},

        {'dest_id': 'barca001', 'name': 'La Sagrada Familia', 'category': 'attraction', 'address': 'C/ de Mallorca, 401, 08013 Barcelona, Spain', 'lat': 41.4036, 'lon': 2.1744},
        {'dest_id': 'barca001', 'name': 'Park Güell', 'category': 'attraction', 'address': '08024 Barcelona, Spain', 'lat': 41.4145, 'lon': 2.1527},
        {'dest_id': 'barca001', 'name': 'Gothic Quarter (Barri Gòtic)', 'category': 'attraction', 'address': 'Ciutat Vella, 08002 Barcelona, Spain', 'lat': 41.3830, 'lon': 2.1760},
        {'dest_id': 'barca001', 'name': 'El Xampanyet', 'category': 'restaurant', 'address': 'Carrer de Montcada, 22, 08003 Barcelona, Spain', 'lat': 41.3846, 'lon': 2.1812},

        {'dest_id': 'amsterdam001', 'name': 'Rijksmuseum', 'category': 'attraction', 'address': 'Museumstraat 1, 1071 XX Amsterdam, Netherlands', 'lat': 52.3600, 'lon': 4.8852},
        {'dest_id': 'amsterdam001', 'name': 'Anne Frank House', 'category': 'attraction', 'address': 'Westermarkt 20, 1016 GV Amsterdam, Netherlands', 'lat': 52.3752, 'lon': 4.8839},
        {'dest_id': 'amsterdam001', 'name': 'Van Gogh Museum', 'category': 'attraction', 'address': 'Museumplein 6, 1071 DJ Amsterdam, Netherlands', 'lat': 52.3584, 'lon': 4.8811},
        {'dest_id': 'amsterdam001', 'name': 'The Pantry', 'category': 'restaurant', 'address': 'Leidsekruisstraat 21, 1017 RE Amsterdam, Netherlands', 'lat': 52.3630, 'lon': 4.8840},

        {'dest_id': 'prague001', 'name': 'Charles Bridge', 'category': 'attraction', 'address': 'Karlův most, 110 00 Prague 1, Czechia', 'lat': 50.0865, 'lon': 14.4114},
        {'dest_id': 'prague001', 'name': 'Prague Castle', 'category': 'attraction', 'address': 'Hradčany, 119 08 Prague 1, Czechia', 'lat': 50.0901, 'lon': 14.4020},
        {'dest_id': 'prague001', 'name': 'Old Town Square', 'category': 'attraction', 'address': 'Staroměstské nám., 110 00 Josefov, Czechia', 'lat': 50.0877, 'lon': 14.4213},
        {'dest_id': 'prague001', 'name': 'U Medvidku', 'category': 'restaurant', 'address': 'Na Perštýně 345/7, 100 01 Prague 1, Czechia', 'lat': 50.0833, 'lon': 14.4190},

        {'dest_id': 'venice001', 'name': 'St. Mark\'s Basilica', 'category': 'attraction', 'address': 'P.za San Marco, 328, 30124 Venezia VE, Italy', 'lat': 45.4346, 'lon': 12.3397},
        {'dest_id': 'venice001', 'name': 'Doge\'s Palace', 'category': 'attraction', 'address': 'P.za San Marco, 1, 30124 Venezia VE, Italy', 'lat': 45.4339, 'lon': 12.3400},
        {'dest_id': 'venice001', 'name': 'Rialto Bridge', 'category': 'attraction', 'address': 'Sestiere San Polo, 30125 Venezia VE, Italy', 'lat': 45.4380, 'lon': 12.3359},
        {'dest_id': 'venice001', 'name': 'Osteria alle Testiere', 'category': 'restaurant', 'address': 'Calle del Mondo Novo, 5801, 30122 Venezia VE, Italy', 'lat': 45.4372, 'lon': 12.3400},

        {'dest_id': 'santorini001', 'name': 'Oia Village', 'category': 'attraction', 'address': 'Oia 847 02, Greece', 'lat': 36.4623, 'lon': 25.3753},
        {'dest_id': 'santorini001', 'name': 'Akrotiri Archaeological Site', 'category': 'attraction', 'address': 'Akrotiri 847 00, Greece', 'lat': 36.3516, 'lon': 25.3995},
        {'dest_id': 'santorini001', 'name': 'Red Beach', 'category': 'attraction', 'address': 'Akrotiri 847 00, Greece', 'lat': 36.3486, 'lon': 25.3944},
        {'dest_id': 'santorini001', 'name': 'Ambrosia Restaurant', 'category': 'restaurant', 'address': 'Oia 847 02, Greece', 'lat': 36.4616, 'lon': 25.3750},

        {'dest_id': 'interlaken001', 'name': 'Jungfraujoch', 'category': 'attraction', 'address': '3801 Fieschertal, Switzerland', 'lat': 46.5475, 'lon': 7.9854},
        {'dest_id': 'interlaken001', 'name': 'Harder Kulm', 'category': 'attraction', 'address': '3800 Unterseen, Switzerland', 'lat': 46.6975, 'lon': 7.8631},
        {'dest_id': 'interlaken001', 'name': 'Lake Brienz', 'category': 'attraction', 'address': 'Lake Brienz, Switzerland', 'lat': 46.7271, 'lon': 7.9839},
        {'dest_id': 'interlaken001', 'name': 'Restaurant Laterne', 'category': 'restaurant', 'address': 'Obere Gasse 2, 3800 Interlaken, Switzerland', 'lat': 46.6853, 'lon': 7.8600},

        {'dest_id': 'zermatt001', 'name': 'The Matterhorn', 'category': 'attraction', 'address': 'Matterhorn, 3920 Zermatt, Switzerland', 'lat': 45.9766, 'lon': 7.6585},
        {'dest_id': 'zermatt001', 'name': 'Gornergrat Railway', 'category': 'attraction', 'address': 'Bahnhofplatz, 3920 Zermatt, Switzerland', 'lat': 46.0222, 'lon': 7.7486},
        {'dest_id': 'zermatt001', 'name': 'Matterhorn Glacier Paradise', 'category': 'attraction', 'address': 'Schluhmattstrasse 28, 3920 Zermatt, Switzerland', 'lat': 45.9389, 'lon': 7.7317},
        {'dest_id': 'zermatt001', 'name': 'Restaurant Whymper-Stube', 'category': 'restaurant', 'address': 'Bahnhofstrasse 80, 3920 Zermatt, Switzerland', 'lat': 46.0207, 'lon': 7.7491},

        {'dest_id': 'reykjavik001', 'name': 'Blue Lagoon', 'category': 'attraction', 'address': 'Norðurljósavegur 9, 240 Grindavík, Iceland', 'lat': 63.8804, 'lon': -22.4496},
        {'dest_id': 'reykjavik001', 'name': 'Hallgrímskirkja', 'category': 'attraction', 'address': 'Hallgrímstorg 1, 101 Reykjavík, Iceland', 'lat': 64.1417, 'lon': -21.9266},
        {'dest_id': 'reykjavik001', 'name': 'Golden Circle Route', 'category': 'attraction', 'address': 'Thingvellir National Park, Iceland', 'lat': 64.2558, 'lon': -21.1301},
        {'dest_id': 'reykjavik001', 'name': 'Bæjarins Beztu Pylsur', 'category': 'restaurant', 'address': 'Tryggvagata 1, 101 Reykjavík, Iceland', 'lat': 64.1485, 'lon': -21.9395},

        {'dest_id': 'florence001', 'name': 'Florence Cathedral (Duomo)', 'category': 'attraction', 'address': 'Piazza del Duomo, 50122 Firenze FI, Italy', 'lat': 43.7731, 'lon': 11.2558},
        {'dest_id': 'florence001', 'name': 'Uffizi Gallery', 'category': 'attraction', 'address': 'Piazzale degli Uffizi, 6, 50122 Firenze FI, Italy', 'lat': 43.7678, 'lon': 11.2552},
        {'dest_id': 'florence001', 'name': 'Ponte Vecchio', 'category': 'attraction', 'address': 'Ponte Vecchio, 50125 Firenze FI, Italy', 'lat': 43.7680, 'lon': 11.2530},
        {'dest_id': 'florence001', 'name': 'Trattoria Mario', 'category': 'restaurant', 'address': 'Via Rosina, 2/r, 50123 Firenze FI, Italy', 'lat': 43.7766, 'lon': 11.2558},

        {'dest_id': 'lisbon001', 'name': 'Belém Tower', 'category': 'attraction', 'address': 'Av. Brasília, 1400-038 Lisboa, Portugal', 'lat': 38.6916, 'lon': -9.2160},
        {'dest_id': 'lisbon001', 'name': 'Jerónimos Monastery', 'category': 'attraction', 'address': 'Praça do Império 1400-206, Lisboa, Portugal', 'lat': 38.6978, 'lon': -9.2061},
        {'dest_id': 'lisbon001', 'name': 'Alfama District', 'category': 'attraction', 'address': 'Alfama, 1100-341 Lisboa, Portugal', 'lat': 38.7120, 'lon': -9.1290},
        {'dest_id': 'lisbon001', 'name': 'Cervejaria Ramiro', 'category': 'restaurant', 'address': 'Av. Almirante Reis 1 - H, 1150-007 Lisboa, Portugal', 'lat': 38.7200, 'lon': -9.1360},

        {'dest_id': 'budapest001', 'name': 'Hungarian Parliament Building', 'category': 'attraction', 'address': 'Kossuth Lajos tér 1-3, 1055 Budapest, Hungary', 'lat': 47.5072, 'lon': 19.0483},
        {'dest_id': 'budapest001', 'name': 'Széchenyi Thermal Bath', 'category': 'attraction', 'address': 'Állatkerti krt. 9-11, 1146 Budapest, Hungary', 'lat': 47.5188, 'lon': 19.0823},
        {'dest_id': 'budapest001', 'name': 'Buda Castle', 'category': 'attraction', 'address': 'Szent György tér 2, 1014 Budapest, Hungary', 'lat': 47.4960, 'lon': 19.0395},
        {'dest_id': 'budapest001', 'name': 'New York Café', 'category': 'restaurant', 'address': 'Erzsébet krt. 9-11, 1073 Budapest, Hungary', 'lat': 47.4983, 'lon': 19.0689},

        {'dest_id': 'edinburgh001', 'name': 'Edinburgh Castle', 'category': 'attraction', 'address': 'Castlehill, Edinburgh EH1 2NG, UK', 'lat': 55.9486, 'lon': -3.1999},
        {'dest_id': 'edinburgh001', 'name': 'Arthur\'s Seat', 'category': 'attraction', 'address': 'Queen\'s Drive, Edinburgh EH8 8HG, UK', 'lat': 55.9443, 'lon': -3.1614},
        {'dest_id': 'edinburgh001', 'name': 'Royal Mile', 'category': 'attraction', 'address': 'Royal Mile, Edinburgh, UK', 'lat': 55.9503, 'lon': -3.1800},
        {'dest_id': 'edinburgh001', 'name': 'The Witchery by the Castle', 'category': 'restaurant', 'address': 'Castlehill, Edinburgh EH1 2NF, UK', 'lat': 55.9493, 'lon': -3.1950},

        {'dest_id': 'dublin001', 'name': 'Guinness Storehouse', 'category': 'attraction', 'address': 'St. James\'s Gate, Dublin 8, Ireland', 'lat': 53.3418, 'lon': -6.2867},
        {'dest_id': 'dublin001', 'name': 'Kilmainham Gaol', 'category': 'attraction', 'address': 'Inchicore Rd, Kilmainham, Dublin 8, Ireland', 'lat': 53.3416, 'lon': -6.3100},
        {'dest_id': 'dublin001', 'name': 'Trinity College Dublin', 'category': 'attraction', 'address': 'College Green, Dublin 2, Ireland', 'lat': 53.3438, 'lon': -6.2546},
        {'dest_id': 'dublin001', 'name': 'The Winding Stair', 'category': 'restaurant', 'address': '40 Lower Ormond Quay, Dublin 1, Ireland', 'lat': 53.3470, 'lon': -6.2650},

        {'dest_id': 'berlin001', 'name': 'Brandenburg Gate', 'category': 'attraction', 'address': 'Pariser Platz, 10117 Berlin, Germany', 'lat': 52.5163, 'lon': 13.3777},
        {'dest_id': 'berlin001', 'name': 'Reichstag Building', 'category': 'attraction', 'address': 'Platz der Republik 1, 11011 Berlin, Germany', 'lat': 52.5186, 'lon': 13.3762},
        {'dest_id': 'berlin001', 'name': 'East Side Gallery', 'category': 'attraction', 'address': 'Mühlenstraße 3-100, 10243 Berlin, Germany', 'lat': 52.5050, 'lon': 13.4390},
        {'dest_id': 'berlin001', 'name': 'Mustafa\'s Gemuese Kebab', 'category': 'restaurant', 'address': 'Mehringdamm 32, 10961 Berlin, Germany', 'lat': 52.4930, 'lon': 13.3880},

        {'dest_id': 'moscow001', 'name': 'Red Square', 'category': 'attraction', 'address': 'Red Square, Moscow, Russia, 109012', 'lat': 55.7539, 'lon': 37.6208},
        {'dest_id': 'moscow001', 'name': 'Saint Basil\'s Cathedral', 'category': 'attraction', 'address': 'Red Square, Moscow, Russia, 109012', 'lat': 55.7525, 'lon': 37.6231},
        {'dest_id': 'moscow001', 'name': 'The Kremlin', 'category': 'attraction', 'address': 'Moscow, Russia, 103132', 'lat': 55.7517, 'lon': 37.6176},
        {'dest_id': 'moscow001', 'name': 'Café Pushkin', 'category': 'restaurant', 'address': 'Tverskoy Blvd, 26А, Moscow, Russia, 125009', 'lat': 55.7651, 'lon': 37.6042},

        {'dest_id': 'istanbul001', 'name': 'Hagia Sophia', 'category': 'attraction', 'address': 'Sultan Ahmet, Ayasofya Meydanı No:1, 34122 Fatih/İstanbul, Turkey', 'lat': 41.0086, 'lon': 28.9800},
        {'dest_id': 'istanbul001', 'name': 'The Blue Mosque', 'category': 'attraction', 'address': 'Sultan Ahmet, Atmeydanı Cd. No:7, 34122 Fatih/İstanbul, Turkey', 'lat': 41.0053, 'lon': 28.9769},
        {'dest_id': 'istanbul001', 'name': 'Grand Bazaar', 'category': 'attraction', 'address': 'Beyazıt, Kalpakçılar Cd. No:22, 34126 Fatih/İstanbul, Turkey', 'lat': 41.0100, 'lon': 28.9680},
        {'dest_id': 'istanbul001', 'name': 'Ciğeristan', 'category': 'restaurant', 'address': 'Hocapaşa Sk. No:8, Sirkeci, 34110 Fatih/İstanbul, Turkey', 'lat': 41.0125, 'lon': 28.9780},

        {'dest_id': 'dubrovnik001', 'name': 'Walls of Dubrovnik', 'category': 'attraction', 'address': 'Stradun, 20000, Dubrovnik, Croatia', 'lat': 42.6416, 'lon': 18.1070},
        {'dest_id': 'dubrovnik001', 'name': 'Dubrovnik Old Town', 'category': 'attraction', 'address': 'Stradun, 20000, Dubrovnik, Croatia', 'lat': 42.6401, 'lon': 18.1082},
        {'dest_id': 'dubrovnik001', 'name': 'Lokrum Island', 'category': 'attraction', 'address': 'Lokrum, Dubrovnik, Croatia', 'lat': 42.6250, 'lon': 18.1250},
        {'dest_id': 'dubrovnik001', 'name': 'Restaurant 360', 'category': 'restaurant', 'address': 'Ul. od Puča 1, 20000, Dubrovnik, Croatia', 'lat': 42.6410, 'lon': 18.1100},

        {'dest_id': 'vienna001', 'name': 'Schönbrunn Palace', 'category': 'attraction', 'address': 'Schönbrunner Schloßstraße 47, 1130 Wien, Austria', 'lat': 48.1848, 'lon': 16.3117},
        {'dest_id': 'vienna001', 'name': 'Hofburg Palace', 'category': 'attraction', 'address': 'Michaelerkuppel, 1010 Wien, Austria', 'lat': 48.2078, 'lon': 16.3653},
        {'dest_id': 'vienna001', 'name': 'St. Stephen\'s Cathedral', 'category': 'attraction', 'address': 'Stephansplatz 3, 1010 Wien, Austria', 'lat': 48.2083, 'lon': 16.3731},
        {'dest_id': 'vienna001', 'name': 'Figlmüller', 'category': 'restaurant', 'address': 'Wollzeile 5, 1010 Wien, Austria', 'lat': 48.2084, 'lon': 16.3755},

        {'dest_id': 'munich001', 'name': 'Marienplatz', 'category': 'attraction', 'address': 'Marienplatz, 80331 München, Germany', 'lat': 48.1372, 'lon': 11.5755},
        {'dest_id': 'munich001', 'name': 'English Garden', 'category': 'attraction', 'address': 'Englischer Garten, 80538 München, Germany', 'lat': 48.1643, 'lon': 11.6050},
        {'dest_id': 'munich001', 'name': 'Nymphenburg Palace', 'category': 'attraction', 'address': 'Schloß Nymphenburg 1, 80638 München, Germany', 'lat': 48.1581, 'lon': 11.5033},
        {'dest_id': 'munich001', 'name': 'Hofbräuhaus München', 'category': 'restaurant', 'address': 'Platzl 9, 80331 München, Germany', 'lat': 48.1376, 'lon': 11.5798},

        {'dest_id': 'madrid001', 'name': 'Prado Museum', 'category': 'attraction', 'address': 'C. de Ruiz de Alarcón, 23, 28014 Madrid, Spain', 'lat': 40.4138, 'lon': -3.6921},
        {'dest_id': 'madrid001', 'name': 'Royal Palace of Madrid', 'category': 'attraction', 'address': 'C. de Bailén, s/n, 28071 Madrid, Spain', 'lat': 40.4179, 'lon': -3.7141},
        {'dest_id': 'madrid001', 'name': 'Retiro Park', 'category': 'attraction', 'address': 'Plaza de la Independencia, 7, 28001 Madrid, Spain', 'lat': 40.4150, 'lon': -3.6840},
        {'dest_id': 'madrid001', 'name': 'Sobrino de Botín', 'category': 'restaurant', 'address': 'C. de Cuchilleros, 17, 28005 Madrid, Spain', 'lat': 40.4124, 'lon': -3.7081},

        {'dest_id': 'copenhagen001', 'name': 'Tivoli Gardens', 'category': 'attraction', 'address': 'Vesterbrogade 3, 1630 København V, Denmark', 'lat': 55.6732, 'lon': 12.5683},
        {'dest_id': 'copenhagen001', 'name': 'Nyhavn', 'category': 'attraction', 'address': 'Nyhavn, 1051 København, Denmark', 'lat': 55.6793, 'lon': 12.5901},
        {'dest_id': 'copenhagen001', 'name': 'The Little Mermaid', 'category': 'attraction', 'address': 'Langelinie, 2100 København Ø, Denmark', 'lat': 55.6928, 'lon': 12.5993},
        {'dest_id': 'copenhagen001', 'name': 'Noma', 'category': 'restaurant', 'address': 'Refshalevej 96, 1432 København, Denmark', 'lat': 55.6880, 'lon': 12.6100},

        {'dest_id': 'krakow001', 'name': 'Main Market Square', 'category': 'attraction', 'address': 'Rynek Główny, 31-042 Kraków, Poland', 'lat': 50.0619, 'lon': 19.9368},
        {'dest_id': 'krakow001', 'name': 'Wawel Royal Castle', 'category': 'attraction', 'address': 'Wawel 5, 31-001 Kraków, Poland', 'lat': 50.0543, 'lon': 19.9355},
        {'dest_id': 'krakow001', 'name': 'Auschwitz-Birkenau Memorial and Museum', 'category': 'attraction', 'address': 'Więźniów Oświęcimia 20, 32-600 Oświęcim, Poland', 'lat': 50.0264, 'lon': 19.2094},
        {'dest_id': 'krakow001', 'name': 'Pod Aniołami', 'category': 'restaurant', 'address': 'Grodzka 35, 31-001 Kraków, Poland', 'lat': 50.0594, 'lon': 19.9383},

        {'dest_id': 'amalfi001', 'name': 'Positano', 'category': 'attraction', 'address': 'Positano SA, Italy', 'lat': 40.6280, 'lon': 14.4850},
        {'dest_id': 'amalfi001', 'name': 'Amalfi Cathedral', 'category': 'attraction', 'address': 'Piazza Duomo, 1, 84011 Amalfi SA, Italy', 'lat': 40.6346, 'lon': 14.6027},
        {'dest_id': 'amalfi001', 'name': 'Villa Cimbrone Gardens', 'category': 'attraction', 'address': 'Via Santa Chiara, 26, 84010 Ravello SA, Italy', 'lat': 40.6475, 'lon': 14.6133},
        {'dest_id': 'amalfi001', 'name': 'La Sponda', 'category': 'restaurant', 'address': 'Via S. Sebastiano, 2, 84017 Positano SA, Italy', 'lat': 40.6288, 'lon': 14.4858},

        {'dest_id': 'bergen001', 'name': 'Bryggen', 'category': 'attraction', 'address': 'Bryggen, 5003 Bergen, Norway', 'lat': 60.3971, 'lon': 5.3245},
        {'dest_id': 'bergen001', 'name': 'Fløibanen Funicular', 'category': 'attraction', 'address': 'Vetrlidsallmenningen 23A, 5014 Bergen, Norway', 'lat': 60.3948, 'lon': 5.3283},
        {'dest_id': 'bergen001', 'name': 'Nærøyfjord', 'category': 'attraction', 'address': 'Nærøyfjord, Aurland, Norway', 'lat': 60.9481, 'lon': 6.9458},
        {'dest_id': 'bergen001', 'name': 'Fisketorget (Fish Market)', 'category': 'restaurant', 'address': 'Torget 5, 5014 Bergen, Norway', 'lat': 60.3942, 'lon': 5.3256},

        {'dest_id': 'athens001', 'name': 'Acropolis of Athens', 'category': 'attraction', 'address': 'Athens 105 58, Greece', 'lat': 37.9715, 'lon': 23.7257},
        {'dest_id': 'athens001', 'name': 'Parthenon', 'category': 'attraction', 'address': 'Athens 105 58, Greece', 'lat': 37.9715, 'lon': 23.7266},
        {'dest_id': 'athens001', 'name': 'Plaka', 'category': 'attraction', 'address': 'Plaka, Athens, Greece', 'lat': 37.9729, 'lon': 23.7308},
        {'dest_id': 'athens001', 'name': 'Taverna Saita', 'category': 'restaurant', 'address': 'Kidathineon 21, Athina 105 58, Greece', 'lat': 37.9733, 'lon': 23.7311},

        {'dest_id': 'stockholm001', 'name': 'Gamla Stan (Old Town)', 'category': 'attraction', 'address': 'Gamla Stan, Stockholm, Sweden', 'lat': 59.3258, 'lon': 18.0718},
        {'dest_id': 'stockholm001', 'name': 'Vasa Museum', 'category': 'attraction', 'address': 'Galärvarvsvägen 14, 115 21 Stockholm, Sweden', 'lat': 59.3280, 'lon': 18.0910},
        {'dest_id': 'stockholm001', 'name': 'Skansen', 'category': 'attraction', 'address': 'Djurgårdsslätten 49-51, 115 21 Stockholm, Sweden', 'lat': 59.3249, 'lon': 18.1039},
        {'dest_id': 'stockholm001', 'name': 'Gastrologik', 'category': 'restaurant', 'address': 'Artillerigatan 14, 114 51 Stockholm, Sweden', 'lat': 59.3364, 'lon': 18.0800},

        {'dest_id': 'helsinki001', 'name': 'Suomenlinna', 'category': 'attraction', 'address': '00190 Helsinki, Finland', 'lat': 60.1460, 'lon': 24.9860},
        {'dest_id': 'helsinki001', 'name': 'Helsinki Cathedral', 'category': 'attraction', 'address': 'Unioninkatu 29, 00170 Helsinki, Finland', 'lat': 60.1705, 'lon': 24.9523},
        {'dest_id': 'helsinki001', 'name': 'Temppeliaukio Church (Rock Church)', 'category': 'attraction', 'address': 'Lutherinkatu 3, 00100 Helsinki, Finland', 'lat': 60.1723, 'lon': 24.9250},
        {'dest_id': 'helsinki001', 'name': 'Savoy', 'category': 'restaurant', 'address': 'Eteläesplanadi 14, 00130 Helsinki, Finland', 'lat': 60.1664, 'lon': 24.9472},

        {'dest_id': 'brussels001', 'name': 'Grand-Place', 'category': 'attraction', 'address': '1000 Brussels, Belgium', 'lat': 50.8467, 'lon': 4.3525},
        {'dest_id': 'brussels001', 'name': 'Atomium', 'category': 'attraction', 'address': 'Pl. de l\'Atomium 1, 1020 Bruxelles, Belgium', 'lat': 50.8948, 'lon': 4.3415},
        {'dest_id': 'brussels001', 'name': 'Manneken Pis', 'category': 'attraction', 'address': '1000 Brussels, Belgium', 'lat': 50.8450, 'lon': 4.3500},
        {'dest_id': 'brussels001', 'name': 'Fin de Siècle', 'category': 'restaurant', 'address': 'Rue des Chartreux 9, 1000 Bruxelles, Belgium', 'lat': 50.8492, 'lon': 4.3467},

        {'dest_id': 'geneva001', 'name': 'Jet d\'Eau', 'category': 'attraction', 'address': 'Quai Gustave-Ador, 1207 Genève, Switzerland', 'lat': 46.2075, 'lon': 6.1558},
        {'dest_id': 'geneva001', 'name': 'St. Pierre Cathedral', 'category': 'attraction', 'address': 'Cr de Saint-Pierre, 1204 Genève, Switzerland', 'lat': 46.2009, 'lon': 6.1481},
        {'dest_id': 'geneva001', 'name': 'Palace of Nations', 'category': 'attraction', 'address': '1211 Geneva, Switzerland', 'lat': 46.2267, 'lon': 6.1408},
        {'dest_id': 'geneva001', 'name': 'Les Armures', 'category': 'restaurant', 'address': 'Rue du Puits-Saint-Pierre 1, 1204 Genève, Switzerland', 'lat': 46.2011, 'lon': 6.1472},

        {'dest_id': 'nice001', 'name': 'Promenade des Anglais', 'category': 'attraction', 'address': '06000 Nice, France', 'lat': 43.6946, 'lon': 7.2570},
        {'dest_id': 'nice001', 'name': 'Castle Hill of Nice', 'category': 'attraction', 'address': '06300 Nice, France', 'lat': 43.6942, 'lon': 7.2797},
        {'dest_id': 'nice001', 'name': 'Vieille Ville (Old Town)', 'category': 'attraction', 'address': '06300 Nice, France', 'lat': 43.6975, 'lon': 7.2769},
        {'dest_id': 'nice001', 'name': 'Le Chantecler', 'category': 'restaurant', 'address': '37 Prom. des Anglais, 06000 Nice, France', 'lat': 43.6953, 'lon': 7.2597},

        {'dest_id': 'seville001', 'name': 'Plaza de España', 'category': 'attraction', 'address': 'Av de Isabel la Católica, 41004 Sevilla, Spain', 'lat': 37.3772, 'lon': -5.9869},
        {'dest_id': 'seville001', 'name': 'Alcázar of Seville', 'category': 'attraction', 'address': 'Patio de Banderas, s/n, 41004 Sevilla, Spain', 'lat': 37.3826, 'lon': -5.9903},
        {'dest_id': 'seville001', 'name': 'Seville Cathedral', 'category': 'attraction', 'address': 'Av. de la Constitución, s/n, 41004 Sevilla, Spain', 'lat': 37.3858, 'lon': -5.9930},
        {'dest_id': 'seville001', 'name': 'El Rinconcillo', 'category': 'restaurant', 'address': 'C. Gerona, 40, 41003 Sevilla, Spain', 'lat': 37.3941, 'lon': -5.9886},

        {'dest_id': 'porto001', 'name': 'Dom Luís I Bridge', 'category': 'attraction', 'address': 'Pte. Luiz I, Porto, Portugal', 'lat': 41.1399, 'lon': -8.6095},
        {'dest_id': 'porto001', 'name': 'Ribeira District', 'category': 'attraction', 'address': 'Ribeira, Porto, Portugal', 'lat': 41.1408, 'lon': -8.6133},
        {'dest_id': 'porto001', 'name': 'Livraria Lello', 'category': 'attraction', 'address': 'R. das Carmelitas 144, 4050-161 Porto, Portugal', 'lat': 41.1469, 'lon': -8.6147},
        {'dest_id': 'porto001', 'name': 'Tasca do Tio', 'category': 'restaurant', 'address': 'R. da Madeira 226, 4000-069 Porto, Portugal', 'lat': 41.1472, 'lon': -8.6078},

        {'dest_id': 'hamburg001', 'name': 'Miniatur Wunderland', 'category': 'attraction', 'address': 'Kehrwieder 2-4/Block D, 20457 Hamburg, Germany', 'lat': 53.5439, 'lon': 9.9889},
        {'dest_id': 'hamburg001', 'name': 'Elbphilharmonie Hamburg', 'category': 'attraction', 'address': 'Platz d. Deutschen Einheit 1, 20457 Hamburg, Germany', 'lat': 53.5413, 'lon': 9.9841},
        {'dest_id': 'hamburg001', 'name': 'Speicherstadt', 'category': 'attraction', 'address': '20457 Hamburg, Germany', 'lat': 53.5444, 'lon': 9.9922},
        {'dest_id': 'hamburg001', 'name': 'Fischereihafen Restaurant', 'category': 'restaurant', 'address': 'Große Elbstraße 143, 22767 Hamburg, Germany', 'lat': 53.5451, 'lon': 9.9520},

        {'dest_id': 'warsaw001', 'name': 'Warsaw Old Town Market Square', 'category': 'attraction', 'address': 'Rynek Starego Miasta, 00-272 Warszawa, Poland', 'lat': 52.2497, 'lon': 21.0122},
        {'dest_id': 'warsaw001', 'name': 'Łazienki Park', 'category': 'attraction', 'address': 'Agrykola 1, 00-460 Warszawa, Poland', 'lat': 52.2128, 'lon': 21.0333},
        {'dest_id': 'warsaw001', 'name': 'Palace of Culture and Science', 'category': 'attraction', 'address': 'plac Defilad 1, 00-901 Warszawa, Poland', 'lat': 52.2319, 'lon': 21.0067},
        {'dest_id': 'warsaw001', 'name': 'Zapiecek', 'category': 'restaurant', 'address': 'Krakowskie Przedmieście 55, 00-071 Warszawa, Poland', 'lat': 52.2422, 'lon': 21.0150},

        {'dest_id': 'oslo001', 'name': 'Vigeland Park', 'category': 'attraction', 'address': 'Nobels gate 32, 0268 Oslo, Norway', 'lat': 59.9269, 'lon': 10.7011},
        {'dest_id': 'oslo001', 'name': 'Viking Ship Museum', 'category': 'attraction', 'address': 'Huk Aveny 35, 0287 Oslo, Norway', 'lat': 59.9050, 'lon': 10.6850},
        {'dest_id': 'oslo001', 'name': 'Oslo Opera House', 'category': 'attraction', 'address': 'Kirsten Flagstads Plass 1, 0150 Oslo, Norway', 'lat': 59.9073, 'lon': 10.7533},
        {'dest_id': 'oslo001', 'name': 'Maaemo', 'category': 'restaurant', 'address': 'Dronning Eufemias gate 23, 0194 Oslo, Norway', 'lat': 59.9056, 'lon': 10.7583},

        {'dest_id': 'mykonos001', 'name': 'Little Venice', 'category': 'attraction', 'address': 'Mykonos Town 846 00, Greece', 'lat': 37.4450, 'lon': 25.3283},
        {'dest_id': 'mykonos001', 'name': 'Paradise Beach', 'category': 'attraction', 'address': 'Paradise Beach, Mykonos 846 00, Greece', 'lat': 37.4083, 'lon': 25.3583},
        {'dest_id': 'mykonos001', 'name': 'Delos Island', 'category': 'attraction', 'address': 'Delos 846 00, Greece', 'lat': 37.3992, 'lon': 25.2672},
        {'dest_id': 'mykonos001', 'name': 'Kiki\'s Tavern', 'category': 'restaurant', 'address': 'Agios Sostis Beach, Mykonos 846 00, Greece', 'lat': 37.4817, 'lon': 25.3400},

        {'dest_id': 'valencia001', 'name': 'City of Arts and Sciences', 'category': 'attraction', 'address': 'Av. del Professor López Piñero, 7, 46013 València, Spain', 'lat': 39.4547, 'lon': -0.3508},
        {'dest_id': 'valencia001', 'name': 'Mercado Central', 'category': 'attraction', 'address': 'Plaça de la Ciutat de Bruges, s/n, 46001 València, Spain', 'lat': 39.4744, 'lon': -0.3789},
        {'dest_id': 'valencia001', 'name': 'Valencia Cathedral', 'category': 'attraction', 'address': 'Plaça de l\'Almoina, s/n, 46003 València, Spain', 'lat': 39.4758, 'lon': -0.3753},
        {'dest_id': 'valencia001', 'name': 'Casa Montaña', 'category': 'restaurant', 'address': 'C/ de Josep Benlliure, 69, 46011 València, Spain', 'lat': 39.4678, 'lon': -0.3228},

        {'dest_id': 'stpetersburg001', 'name': 'The Hermitage Museum', 'category': 'attraction', 'address': 'Palace Square, 2, St Petersburg, Russia, 190000', 'lat': 59.9398, 'lon': 30.3146},
        {'dest_id': 'stpetersburg001', 'name': 'Church of the Savior on Spilled Blood', 'category': 'attraction', 'address': 'Griboyedov channel embankment, 2b, St Petersburg, Russia, 191186', 'lat': 59.9400, 'lon': 30.3289},
        {'dest_id': 'stpetersburg001', 'name': 'Peterhof Palace', 'category': 'attraction', 'address': 'Razvodnaya Ulitsa, 2, Petergof, St Petersburg, Russia, 198516', 'lat': 59.8810, 'lon': 29.9060},
        {'dest_id': 'stpetersburg001', 'name': 'Palkin', 'category': 'restaurant', 'address': 'Nevsky Ave, 47, St Petersburg, Russia, 191025', 'lat': 59.9325, 'lon': 30.3442},

        {'dest_id': 'bruges001', 'name': 'Market Square (Markt)', 'category': 'attraction', 'address': 'Markt, 8000 Brugge, Belgium', 'lat': 51.2089, 'lon': 3.2256},
        {'dest_id': 'bruges001', 'name': 'Belfry of Bruges', 'category': 'attraction', 'address': 'Markt 7, 8000 Brugge, Belgium', 'lat': 51.2083, 'lon': 3.2247},
        {'dest_id': 'bruges001', 'name': 'Canal Cruise', 'category': 'attraction', 'address': 'Rozenhoedkaai, 8000 Brugge, Belgium', 'lat': 51.2081, 'lon': 3.2269},
        {'dest_id': 'bruges001', 'name': 'De Halve Maan Brewery', 'category': 'restaurant', 'address': 'Walplein 26, 8000 Brugge, Belgium', 'lat': 51.2014, 'lon': 3.2242},

        {'dest_id': 'salzburg001', 'name': 'Hohensalzburg Fortress', 'category': 'attraction', 'address': 'Mönchsberg 34, 5020 Salzburg, Austria', 'lat': 47.7946, 'lon': 13.0468},
        {'dest_id': 'salzburg001', 'name': 'Mirabell Palace and Gardens', 'category': 'attraction', 'address': 'Mirabellplatz, 5020 Salzburg, Austria', 'lat': 47.8071, 'lon': 13.0418},
        {'dest_id': 'salzburg001', 'name': 'Mozart\'s Birthplace', 'category': 'attraction', 'address': 'Getreidegasse 9, 5020 Salzburg, Austria', 'lat': 47.8005, 'lon': 13.0435},
        {'dest_id': 'salzburg001', 'name': 'Augustiner Bräustübl', 'category': 'restaurant', 'address': 'Lindhofstraße 7, 5020 Salzburg, Austria', 'lat': 47.8069, 'lon': 13.0333},

        {'dest_id': 'lucerne001', 'name': 'Chapel Bridge (Kapellbrücke)', 'category': 'attraction', 'address': 'Kapellbrücke, 6002 Luzern, Switzerland', 'lat': 47.0510, 'lon': 8.3075},
        {'dest_id': 'lucerne001', 'name': 'Mount Pilatus', 'category': 'attraction', 'address': '6010 Alpnach, Switzerland', 'lat': 46.9790, 'lon': 8.2530},
        {'dest_id': 'lucerne001', 'name': 'Lion Monument', 'category': 'attraction', 'address': 'Denkmalstrasse 4, 6002 Luzern, Switzerland', 'lat': 47.0583, 'lon': 8.3122},
        {'dest_id': 'lucerne001', 'name': 'Wirtshaus Galliker', 'category': 'restaurant', 'address': 'Schützenstrasse 1, 6003 Luzern, Switzerland', 'lat': 47.0469, 'lon': 8.3025},

        {'dest_id': 'ibiza001', 'name': 'Dalt Vila (Ibiza Old Town)', 'category': 'attraction', 'address': '07800 Ibiza Town, Balearic Islands, Spain', 'lat': 38.9067, 'lon': 1.4361},
        {'dest_id': 'ibiza001', 'name': 'Es Vedrà', 'category': 'attraction', 'address': '07830 Sant Josep de sa Talaia, Balearic Islands, Spain', 'lat': 38.8686, 'lon': 1.2056},
        {'dest_id': 'ibiza001', 'name': 'Pacha Ibiza', 'category': 'attraction', 'address': 'Av. 8 d\'Agost, 07800 Ibiza Town, Balearic Islands, Spain', 'lat': 38.9189, 'lon': 1.4428},
        {'dest_id': 'ibiza001', 'name': 'El Chiringuito es Cavallet', 'category': 'restaurant', 'address': 'Playa Es Cavallet, 07817, Balearic Islands, Spain', 'lat': 38.8783, 'lon': 1.3917},

        {'dest_id': 'frankfurt001', 'name': 'Römerberg', 'category': 'attraction', 'address': 'Römerberg, 60311 Frankfurt am Main, Germany', 'lat': 50.1106, 'lon': 8.6819},
        {'dest_id': 'frankfurt001', 'name': 'Main Tower', 'category': 'attraction', 'address': 'Neue Mainzer Str. 52-58, 60311 Frankfurt am Main, Germany', 'lat': 50.1133, 'lon': 8.6728},
        {'dest_id': 'frankfurt001', 'name': 'Städel Museum', 'category': 'attraction', 'address': 'Schaumainkai 63, 60596 Frankfurt am Main, Germany', 'lat': 50.1031, 'lon': 8.6756},
        {'dest_id': 'frankfurt001', 'name': 'Apfelwein Wagner', 'category': 'restaurant', 'address': 'Schweizer Str. 71, 60594 Frankfurt am Main, Germany', 'lat': 50.1017, 'lon': 8.6811},

        {'dest_id': 'lyon001', 'name': 'Vieux Lyon (Old Lyon)', 'category': 'attraction', 'address': '69005 Lyon, France', 'lat': 45.7619, 'lon': 4.8272},
        {'dest_id': 'lyon001', 'name': 'Basilica of Notre-Dame de Fourvière', 'category': 'attraction', 'address': '8 Place de Fourvière, 69005 Lyon, France', 'lat': 45.7622, 'lon': 4.8225},
        {'dest_id': 'lyon001', 'name': 'Parc de la Tête d\'Or', 'category': 'attraction', 'address': '69006 Lyon, France', 'lat': 45.7797, 'lon': 4.8519},
        {'dest_id': 'lyon001', 'name': 'L\'Auberge du Pont de Collonges (Paul Bocuse)', 'category': 'restaurant', 'address': '40 Quai de la Plage, 69660 Collonges-au-Mont-d\'Or, France', 'lat': 45.8164, 'lon': 4.8519},

        {'dest_id': 'split001', 'name': 'Diocletian\'s Palace', 'category': 'attraction', 'address': 'Dioklecijanova ul. 1, 21000, Split, Croatia', 'lat': 43.5085, 'lon': 16.4402},
        {'dest_id': 'split001', 'name': 'Riva Harbour', 'category': 'attraction', 'address': 'Obala Hrvatskog narodnog preporoda, 21000, Split, Croatia', 'lat': 43.5069, 'lon': 16.4392},
        {'dest_id': 'split001', 'name': 'Marjan Hill', 'category': 'attraction', 'address': '21000, Split, Croatia', 'lat': 43.5119, 'lon': 16.4178},
        {'dest_id': 'split001', 'name': 'Konoba Fife', 'category': 'restaurant', 'address': 'Trumbićeva obala 11, 21000, Split, Croatia', 'lat': 43.5083, 'lon': 16.4333},

        {'dest_id': 'bologna001', 'name': 'Piazza Maggiore', 'category': 'attraction', 'address': 'Piazza Maggiore, 40124 Bologna BO, Italy', 'lat': 44.4938, 'lon': 11.3426},
        {'dest_id': 'bologna001', 'name': 'Two Towers (Le Due Torri)', 'category': 'attraction', 'address': 'P.za di Porta Ravegnana, 40126 Bologna BO, Italy', 'lat': 44.4946, 'lon': 11.3466},
        {'dest_id': 'bologna001', 'name': 'Archiginnasio of Bologna', 'category': 'attraction', 'address': 'Piazza Galvani, 1, 40124 Bologna BO, Italy', 'lat': 44.4925, 'lon': 11.3425},
        {'dest_id': 'bologna001', 'name': 'Osteria dell\'Orsa', 'category': 'restaurant', 'address': 'Via Mentana, 1, 40126 Bologna BO, Italy', 'lat': 44.4983, 'lon': 11.3492},

        {'dest_id': 'glasgow001', 'name': 'Kelvingrove Art Gallery and Museum', 'category': 'attraction', 'address': 'Argyle St, Glasgow G3 8AG, UK', 'lat': 55.8686, 'lon': -4.2908},
        {'dest_id': 'glasgow001', 'name': 'Glasgow Cathedral', 'category': 'attraction', 'address': 'Castle St, Glasgow G4 0QZ, UK', 'lat': 55.8631, 'lon': -4.2306},
        {'dest_id': 'glasgow001', 'name': 'Riverside Museum', 'category': 'attraction', 'address': '100 Pointhouse Rd, Govan, Glasgow G3 8RS, UK', 'lat': 55.8653, 'lon': -4.3075},
        {'dest_id': 'glasgow001', 'name': 'Ubiquitous Chip', 'category': 'restaurant', 'address': '12 Ashton Ln, Hillhead, Glasgow G12 8SJ, UK', 'lat': 55.8756, 'lon': -4.2925},

        {'dest_id': 'tallinn001', 'name': 'Tallinn Old Town', 'category': 'attraction', 'address': 'Tallinn, Estonia', 'lat': 59.4370, 'lon': 24.7454},
        {'dest_id': 'tallinn001', 'name': 'Alexander Nevsky Cathedral', 'category': 'attraction', 'address': 'Lossi plats 10, 10130 Tallinn, Estonia', 'lat': 59.4363, 'lon': 24.7408},
        {'dest_id': 'tallinn001', 'name': 'Kadriorg Palace', 'category': 'attraction', 'address': 'A. Weizenbergi 37, 10127 Tallinn, Estonia', 'lat': 59.4383, 'lon': 24.7900},
        {'dest_id': 'tallinn001', 'name': 'Rataskaevu 16', 'category': 'restaurant', 'address': 'Rataskaevu 16, 10123 Tallinn, Estonia', 'lat': 59.4372, 'lon': 24.7431},

        {'dest_id': 'riga001', 'name': 'Riga Old Town', 'category': 'attraction', 'address': 'Riga, Latvia', 'lat': 56.9496, 'lon': 24.1052},
        {'dest_id': 'riga001', 'name': 'House of the Blackheads', 'category': 'attraction', 'address': 'Rātslaukums 7, Centra rajons, Rīga, LV-1050, Latvia', 'lat': 56.9472, 'lon': 24.1067},
        {'dest_id': 'riga001', 'name': 'Riga Central Market', 'category': 'attraction', 'address': 'Nēģu iela 7, Latgales priekšpilsēta, Rīga, LV-1050, Latvia', 'lat': 56.9439, 'lon': 24.1147},
        {'dest_id': 'riga001', 'name': 'Folkklubs ALA pagrabs', 'category': 'restaurant', 'address': 'Peldu iela 19, Centra rajons, Rīga, LV-1050, Latvia', 'lat': 56.9475, 'lon': 24.1058},

        {'dest_id': 'vilnius001', 'name': 'Vilnius Old Town', 'category': 'attraction', 'address': 'Vilnius, Lithuania', 'lat': 54.6796, 'lon': 25.2870},
        {'dest_id': 'vilnius001', 'name': 'Gediminas\' Tower', 'category': 'attraction', 'address': 'Arsenalo g. 5, Vilnius 01143, Lithuania', 'lat': 54.6867, 'lon': 25.2900},
        {'dest_id': 'vilnius001', 'name': 'St. Anne\'s Church', 'category': 'attraction', 'address': 'Maironio g. 8, Vilnius 01124, Lithuania', 'lat': 54.6833, 'lon': 25.2933},
        {'dest_id': 'vilnius001', 'name': 'Ertlio Namas', 'category': 'restaurant', 'address': 'Šv. Jono g. 7, Vilnius 01123, Lithuania', 'lat': 54.6811, 'lon': 25.2883},

        {'dest_id': 'ljubljana001', 'name': 'Ljubljana Castle', 'category': 'attraction', 'address': 'Grajska planota 1, 1000 Ljubljana, Slovenia', 'lat': 46.0489, 'lon': 14.5089},
        {'dest_id': 'ljubljana001', 'name': 'Triple Bridge (Tromostovje)', 'category': 'attraction', 'address': 'Adamič-Lundrovo nabrežje 1, 1000 Ljubljana, Slovenia', 'lat': 46.0514, 'lon': 14.5061},
        {'dest_id': 'ljubljana001', 'name': 'Tivoli Park', 'category': 'attraction', 'address': '1000 Ljubljana, Slovenia', 'lat': 46.0542, 'lon': 14.4939},
        {'dest_id': 'ljubljana001', 'name': 'Gostilna na Gradu', 'category': 'restaurant', 'address': 'Grajska planota 1, 1000 Ljubljana, Slovenia', 'lat': 46.0489, 'lon': 14.5089},
        
                # --- International - Americas ---
        {'dest_id': 'nyc001', 'name': 'Statue of Liberty', 'category': 'attraction', 'address': 'New York, NY 10004, USA', 'lat': 40.6892, 'lon': -74.0445},
        {'dest_id': 'nyc001', 'name': 'Central Park', 'category': 'attraction', 'address': 'New York, NY, USA', 'lat': 40.7851, 'lon': -73.9683},
        {'dest_id': 'nyc001', 'name': 'Times Square', 'category': 'attraction', 'address': 'Manhattan, NY 10036, USA', 'lat': 40.7580, 'lon': -73.9855},
        {'dest_id': 'nyc001', 'name': 'Katz\'s Delicatessen', 'category': 'restaurant', 'address': '205 E Houston St, New York, NY 10002', 'lat': 40.7222, 'lon': -73.9873},

        {'dest_id': 'queen001', 'name': 'Skyline Queenstown', 'category': 'attraction', 'address': 'Brecon St, Queenstown 9300, New Zealand', 'lat': -45.0300, 'lon': 168.6533},
        {'dest_id': 'queen001', 'name': 'Milford Sound', 'category': 'attraction', 'address': 'Milford Sound, Southland 9679, New Zealand', 'lat': -44.6717, 'lon': 167.9250},
        {'dest_id': 'queen001', 'name': 'Shotover Jet', 'category': 'attraction', 'address': '3 Arthurs Point Rd, Arthurs Point, Queenstown 9371, New Zealand', 'lat': -44.9967, 'lon': 168.6833},
        {'dest_id': 'queen001', 'name': 'Fergburger', 'category': 'restaurant', 'address': '42 Shotover St, Queenstown 9300, New Zealand', 'lat': -45.0325, 'lon': 168.6606},

        {'dest_id': 'machupicchu001', 'name': 'Historic Sanctuary of Machu Picchu', 'category': 'attraction', 'address': 'Aguas Calientes, Peru', 'lat': -13.1631, 'lon': -72.5450},
        {'dest_id': 'machupicchu001', 'name': 'Huayna Picchu', 'category': 'attraction', 'address': 'Machu Picchu, Peru', 'lat': -13.1550, 'lon': -72.5458},
        {'dest_id': 'machupicchu001', 'name': 'Sun Gate (Inti Punku)', 'category': 'attraction', 'address': 'Machu Picchu, Peru', 'lat': -13.1700, 'lon': -72.5317},
        {'dest_id': 'machupicchu001', 'name': 'Indio Feliz Restaurant', 'category': 'restaurant', 'address': 'Lloque Yupanqui 103, Aguas Calientes, Peru', 'lat': -13.1539, 'lon': -72.5244},

        {'dest_id': 'galapagos001', 'name': 'Charles Darwin Research Station', 'category': 'attraction', 'address': 'Puerto Ayora, Santa Cruz Island, Galapagos, Ecuador', 'lat': -0.7447, 'lon': -90.3086},
        {'dest_id': 'galapagos001', 'name': 'Tortuga Bay', 'category': 'attraction', 'address': 'Santa Cruz Island, Galapagos, Ecuador', 'lat': -0.7667, 'lon': -90.3333},
        {'dest_id': 'galapagos001', 'name': 'North Seymour Island', 'category': 'attraction', 'address': 'North Seymour Island, Galapagos, Ecuador', 'lat': -0.6500, 'lon': -90.2833},
        {'dest_id': 'galapagos001', 'name': 'El Desayuno de Pele', 'category': 'restaurant', 'address': 'Puerto Ayora, Santa Cruz Island, Galapagos, Ecuador', 'lat': -0.7500, 'lon': -90.3167},

        {'dest_id': 'havana001', 'name': 'Old Havana (Habana Vieja)', 'category': 'attraction', 'address': 'Havana, Cuba', 'lat': 23.1367, 'lon': -82.3550},
        {'dest_id': 'havana001', 'name': 'El Malecón', 'category': 'attraction', 'address': 'Havana, Cuba', 'lat': 23.1433, 'lon': -82.3767},
        {'dest_id': 'havana001', 'name': 'Fusterlandia', 'category': 'attraction', 'address': 'Jaimanitas, Havana, Cuba', 'lat': 23.0917, 'lon': -82.5083},
        {'dest_id': 'havana001', 'name': 'La Guarida', 'category': 'restaurant', 'address': '418 Concordia, La Habana, Cuba', 'lat': 23.1383, 'lon': -82.3683},

        {'dest_id': 'rio001', 'name': 'Christ the Redeemer', 'category': 'attraction', 'address': 'Parque Nacional da Tijuca, Rio de Janeiro, Brazil', 'lat': -22.9519, 'lon': -43.2105},
        {'dest_id': 'rio001', 'name': 'Sugarloaf Mountain', 'category': 'attraction', 'address': 'Av. Pasteur, 520, Urca, Rio de Janeiro, Brazil', 'lat': -22.9489, 'lon': -43.1569},
        {'dest_id': 'rio001', 'name': 'Copacabana Beach', 'category': 'attraction', 'address': 'Copacabana, Rio de Janeiro, Brazil', 'lat': -22.9719, 'lon': -43.1825},
        {'dest_id': 'rio001', 'name': 'Confeitaria Colombo', 'category': 'restaurant', 'address': 'R. Gonçalves Dias, 32, Centro, Rio de Janeiro, Brazil', 'lat': -22.9067, 'lon': -43.1783},

        {'dest_id': 'vancouver001', 'name': 'Stanley Park', 'category': 'attraction', 'address': 'Vancouver, BC, Canada', 'lat': 49.3000, 'lon': -123.1417},
        {'dest_id': 'vancouver001', 'name': 'Granville Island', 'category': 'attraction', 'address': '1661 Duranleau St, Vancouver, BC V6H 3S3, Canada', 'lat': 49.2714, 'lon': -123.1339},
        {'dest_id': 'vancouver001', 'name': 'Capilano Suspension Bridge Park', 'category': 'attraction', 'address': '3735 Capilano Rd, North Vancouver, BC V7R 4J1, Canada', 'lat': 49.3417, 'lon': -123.1150},
        {'dest_id': 'vancouver001', 'name': 'Blue Water Cafe', 'category': 'restaurant', 'address': '1095 Hamilton St, Vancouver, BC V6B 5T4, Canada', 'lat': 49.2750, 'lon': -123.1217},

        {'dest_id': 'banff001', 'name': 'Lake Louise', 'category': 'attraction', 'address': 'Lake Louise, Banff National Park, Alberta, Canada', 'lat': 51.4167, 'lon': -116.2167},
        {'dest_id': 'banff001', 'name': 'Moraine Lake', 'category': 'attraction', 'address': 'Moraine Lake, Banff National Park, Alberta, Canada', 'lat': 51.3219, 'lon': -116.1856},
        {'dest_id': 'banff001', 'name': 'Banff Gondola', 'category': 'attraction', 'address': '100 Mountain Ave, Banff, AB T1L 1B2, Canada', 'lat': 51.1500, 'lon': -115.5550},
        {'dest_id': 'banff001', 'name': 'The Grizzly House', 'category': 'restaurant', 'address': '207 Banff Ave, Banff, AB T1L 1B4, Canada', 'lat': 51.1764, 'lon': -115.5694},

        {'dest_id': 'yosemite001', 'name': 'Yosemite Valley', 'category': 'attraction', 'address': 'Yosemite National Park, CA, USA', 'lat': 37.7456, 'lon': -119.5936},
        {'dest_id': 'yosemite001', 'name': 'Glacier Point', 'category': 'attraction', 'address': 'Glacier Point Rd, Yosemite National Park, CA 95389, USA', 'lat': 37.7281, 'lon': -119.5725},
        {'dest_id': 'yosemite001', 'name': 'Mariposa Grove of Giant Sequoias', 'category': 'attraction', 'address': 'Mariposa Grove Rd, Fish Camp, CA 93623, USA', 'lat': 37.5167, 'lon': -119.6000},
        {'dest_id': 'yosemite001', 'name': 'The Ahwahnee Dining Room', 'category': 'restaurant', 'address': '1 Ahwahnee Drive, Yosemite Valley, CA 95389, USA', 'lat': 37.7472, 'lon': -119.5786},

        {'dest_id': 'vegas001', 'name': 'The Strip', 'category': 'attraction', 'address': 'Las Vegas Blvd, Las Vegas, NV, USA', 'lat': 36.1147, 'lon': -115.1728},
        {'dest_id': 'vegas001', 'name': 'Fountains of Bellagio', 'category': 'attraction', 'address': '3600 S Las Vegas Blvd, Las Vegas, NV 89109, USA', 'lat': 36.1126, 'lon': -115.1767},
        {'dest_id': 'vegas001', 'name': 'Fremont Street Experience', 'category': 'attraction', 'address': 'Fremont St, Las Vegas, NV 89101, USA', 'lat': 36.1706, 'lon': -115.1450},
        {'dest_id': 'vegas001', 'name': 'Joël Robuchon', 'category': 'restaurant', 'address': 'MGM Grand, 3799 S Las Vegas Blvd, Las Vegas, NV 89109, USA', 'lat': 36.1025, 'lon': -115.1697},

        {'dest_id': 'buenosaires001', 'name': 'La Boca', 'category': 'attraction', 'address': 'La Boca, Buenos Aires, Argentina', 'lat': -34.6358, 'lon': -58.3644},
        {'dest_id': 'buenosaires001', 'name': 'Recoleta Cemetery', 'category': 'attraction', 'address': 'Junín 1760, C1113 CABA, Argentina', 'lat': -34.5875, 'lon': -58.3931},
        {'dest_id': 'buenosaires001', 'name': 'Teatro Colón', 'category': 'attraction', 'address': 'Cerrito 628, C1010 AAN, Buenos Aires, Argentina', 'lat': -34.6010, 'lon': -58.3832},
        {'dest_id': 'buenosaires001', 'name': 'Don Julio', 'category': 'restaurant', 'address': 'Guatemala 4699, C1425 CABA, Argentina', 'lat': -34.5878, 'lon': -58.4283},

        {'dest_id': 'limaperu001', 'name': 'Historic Centre of Lima', 'category': 'attraction', 'address': 'Lima, Peru', 'lat': -12.0464, 'lon': -77.0428},
        {'dest_id': 'limaperu001', 'name': 'Huaca Pucllana', 'category': 'attraction', 'address': 'Calle General Borgoño, Miraflores, Lima, Peru', 'lat': -12.1100, 'lon': -77.0333},
        {'dest_id': 'limaperu001', 'name': 'Larco Museum', 'category': 'attraction', 'address': 'Av. Simón Bolívar 1515, Pueblo Libre, Lima, Peru', 'lat': -12.0736, 'lon': -77.0697},
        {'dest_id': 'limaperu001', 'name': 'Central Restaurante', 'category': 'restaurant', 'address': 'Av. Pedro de Osma 301, Barranco, Lima, Peru', 'lat': -12.1472, 'lon': -77.0222},

        {'dest_id': 'mexicocity001', 'name': 'Zócalo (Plaza de la Constitución)', 'category': 'attraction', 'address': 'Mexico City, CDMX, Mexico', 'lat': 19.4326, 'lon': -99.1332},
        {'dest_id': 'mexicocity001', 'name': 'Teotihuacan', 'category': 'attraction', 'address': 'San Juan Teotihuacán, State of Mexico, Mexico', 'lat': 19.6925, 'lon': -98.8436},
        {'dest_id': 'mexicocity001', 'name': 'Frida Kahlo Museum', 'category': 'attraction', 'address': 'Londres 247, Del Carmen, Coyoacán, 04100 Mexico City, CDMX, Mexico', 'lat': 19.3550, 'lon': -99.1622},
        {'dest_id': 'mexicocity001', 'name': 'Pujol', 'category': 'restaurant', 'address': 'Tennyson 133, Polanco, Mexico City, CDMX, Mexico', 'lat': 19.4319, 'lon': -99.2006},

        {'dest_id': 'losangeles001', 'name': 'Hollywood Walk of Fame', 'category': 'attraction', 'address': 'Hollywood Blvd, Hollywood, CA, USA', 'lat': 34.1017, 'lon': -118.3275},
        {'dest_id': 'losangeles001', 'name': 'Santa Monica Pier', 'category': 'attraction', 'address': '200 Santa Monica Pier, Santa Monica, CA 90401, USA', 'lat': 34.0086, 'lon': -118.4989},
        {'dest_id': 'losangeles001', 'name': 'Griffith Observatory', 'category': 'attraction', 'address': '2800 E Observatory Rd, Los Angeles, CA 90027, USA', 'lat': 34.1186, 'lon': -118.3004},
        {'dest_id': 'losangeles001', 'name': 'Grand Central Market', 'category': 'restaurant', 'address': '317 S Broadway, Los Angeles, CA 90013, USA', 'lat': 34.0506, 'lon': -118.2486},

        {'dest_id': 'chicago001', 'name': 'Millennium Park', 'category': 'attraction', 'address': '201 E Randolph St, Chicago, IL 60602, USA', 'lat': 41.8827, 'lon': -87.6226},
        {'dest_id': 'chicago001', 'name': 'Willis Tower', 'category': 'attraction', 'address': '233 S Wacker Dr, Chicago, IL 60606, USA', 'lat': 41.8789, 'lon': -87.6359},
        {'dest_id': 'chicago001', 'name': 'Navy Pier', 'category': 'attraction', 'address': '600 E Grand Ave, Chicago, IL 60611, USA', 'lat': 41.8917, 'lon': -87.6092},
        {'dest_id': 'chicago001', 'name': 'Alinea', 'category': 'restaurant', 'address': '1723 N Halsted St, Chicago, IL 60614, USA', 'lat': 41.9133, 'lon': -87.6483},

        {'dest_id': 'patagonia001', 'name': 'Perito Moreno Glacier', 'category': 'attraction', 'address': 'Los Glaciares National Park, Santa Cruz Province, Argentina', 'lat': -50.4833, 'lon': -73.0500},
        {'dest_id': 'patagonia001', 'name': 'Mount Fitz Roy', 'category': 'attraction', 'address': 'El Chaltén, Santa Cruz Province, Argentina', 'lat': -49.2667, 'lon': -73.0333},
        {'dest_id': 'patagonia001', 'name': 'Ushuaia (End of the World)', 'category': 'attraction', 'address': 'Ushuaia, Tierra del Fuego, Argentina', 'lat': -54.8000, 'lon': -68.3000},
        {'dest_id': 'patagonia001', 'name': 'La Zaina', 'category': 'restaurant', 'address': 'Gobernador Moyano 124, El Calafate, Santa Cruz, Argentina', 'lat': -50.3394, 'lon': -72.2758},

        {'dest_id': 'cancun001', 'name': 'Chichen Itza', 'category': 'attraction', 'address': 'Yucatan, Mexico', 'lat': 20.6843, 'lon': -88.5678},
        {'dest_id': 'cancun001', 'name': 'Isla Mujeres', 'category': 'attraction', 'address': 'Isla Mujeres, Quintana Roo, Mexico', 'lat': 21.2325, 'lon': -86.7325},
        {'dest_id': 'cancun001', 'name': 'Xcaret Park', 'category': 'attraction', 'address': 'Carretera Chetúmal-Puerto Juárez Kilómetro 282, Solidaridad, 77710 Playa del Carmen, Q.R., Mexico', 'lat': 20.5833, 'lon': -87.1167},
        {'dest_id': 'cancun001', 'name': 'La Habichuela Sunset', 'category': 'restaurant', 'address': 'Blvd. Kukulcan, La Isla, Zona Hotelera, 77500 Cancún, Q.R., Mexico', 'lat': 21.1000, 'lon': -86.7667},

        {'dest_id': 'toronto001', 'name': 'CN Tower', 'category': 'attraction', 'address': '290 Bremner Blvd, Toronto, ON M5V 3L9, Canada', 'lat': 43.6426, 'lon': -79.3871},
        {'dest_id': 'toronto001', 'name': 'Royal Ontario Museum', 'category': 'attraction', 'address': '100 Queens Park, Toronto, ON M5S 2C6, Canada', 'lat': 43.6677, 'lon': -79.3948},
        {'dest_id': 'toronto001', 'name': 'St. Lawrence Market', 'category': 'attraction', 'address': '93 Front St E, Toronto, ON M5E 1C3, Canada', 'lat': 43.6487, 'lon': -79.3713},
        {'dest_id': 'toronto001', 'name': 'Alo Restaurant', 'category': 'restaurant', 'address': '163 Spadina Ave, Toronto, ON M5V 2L6, Canada', 'lat': 43.6483, 'lon': -79.3967},

        {'dest_id': 'miami001', 'name': 'South Beach', 'category': 'attraction', 'address': 'Miami Beach, FL, USA', 'lat': 25.7825, 'lon': -80.1311},
        {'dest_id': 'miami001', 'name': 'Art Deco Historic District', 'category': 'attraction', 'address': '1001 Ocean Dr, Miami Beach, FL 33139, USA', 'lat': 25.7789, 'lon': -80.1306},
        {'dest_id': 'miami001', 'name': 'Wynwood Walls', 'category': 'attraction', 'address': '2516 NW 2nd Ave, Miami, FL 33127, USA', 'lat': 25.8000, 'lon': -80.1989},
        {'dest_id': 'miami001', 'name': 'Joe\'s Stone Crab', 'category': 'restaurant', 'address': '11 Washington Ave, Miami Beach, FL 33139, USA', 'lat': 25.7708, 'lon': -80.1339},

        {'dest_id': 'cartagena001', 'name': 'Walled City of Cartagena', 'category': 'attraction', 'address': 'Cartagena, Bolivar, Colombia', 'lat': 10.4244, 'lon': -75.5481},
        {'dest_id': 'cartagena001', 'name': 'Castillo de San Felipe de Barajas', 'category': 'attraction', 'address': 'Cra. 17, Cartagena, Bolivar, Colombia', 'lat': 10.4239, 'lon': -75.5383},
        {'dest_id': 'cartagena001', 'name': 'Rosario Islands', 'category': 'attraction', 'address': 'Cartagena, Bolivar, Colombia', 'lat': 10.1667, 'lon': -75.7500},
        {'dest_id': 'cartagena001', 'name': 'La Cevicheria', 'category': 'restaurant', 'address': 'Cl. 39 #7-14, Cartagena, Bolivar, Colombia', 'lat': 10.4278, 'lon': -75.5489},

        {'dest_id': 'costarica001', 'name': 'Arenal Volcano', 'category': 'attraction', 'address': 'Arenal Volcano National Park, Alajuela Province, Costa Rica', 'lat': 10.4633, 'lon': -84.7033},
        {'dest_id': 'costarica001', 'name': 'Manuel Antonio National Park', 'category': 'attraction', 'address': 'Puntarenas Province, Quepos, Costa Rica', 'lat': 9.3833, 'lon': -84.1333},
        {'dest_id': 'costarica001', 'name': 'Monteverde Cloud Forest Biological Reserve', 'category': 'attraction', 'address': 'Puntarenas Province, Monteverde, Costa Rica', 'lat': 10.3000, 'lon': -84.8167},
        {'dest_id': 'costarica001', 'name': 'La Soda Tapia', 'category': 'restaurant', 'address': 'Calle 40, San José, Costa Rica', 'lat': 9.9333, 'lon': -84.1000},

        {'dest_id': 'amazon001', 'name': 'Meeting of Waters', 'category': 'attraction', 'address': 'Manaus, Amazonas, Brazil', 'lat': -3.1333, 'lon': -59.9167},
        {'dest_id': 'amazon001', 'name': 'Anavilhanas Archipelago', 'category': 'attraction', 'address': 'Rio Negro, Amazonas, Brazil', 'lat': -2.4167, 'lon': -60.9167},
        {'dest_id': 'amazon001', 'name': 'Teatro Amazonas', 'category': 'attraction', 'address': 'Largo de São Sebastião, Centro, Manaus, AM, Brazil', 'lat': -3.1303, 'lon': -60.0239},
        {'dest_id': 'amazon001', 'name': 'Banzeiro', 'category': 'restaurant', 'address': 'R. Libertador, 102, Nossa Sra. das Gracas, Manaus, AM, Brazil', 'lat': -3.1019, 'lon': -60.0200},

        {'dest_id': 'sanfrancisco001', 'name': 'Golden Gate Bridge', 'category': 'attraction', 'address': 'San Francisco, CA, USA', 'lat': 37.8199, 'lon': -122.4783},
        {'dest_id': 'sanfrancisco001', 'name': 'Alcatraz Island', 'category': 'attraction', 'address': 'San Francisco, CA 94133, USA', 'lat': 37.8270, 'lon': -122.4230},
        {'dest_id': 'sanfrancisco001', 'name': 'Fisherman\'s Wharf', 'category': 'attraction', 'address': 'San Francisco, CA, USA', 'lat': 37.8080, 'lon': -122.4177},
        {'dest_id': 'sanfrancisco001', 'name': 'The House', 'category': 'restaurant', 'address': '1230 Grant Ave, San Francisco, CA 94133, USA', 'lat': 37.7983, 'lon': -122.4067},

        {'dest_id': 'neworleans001', 'name': 'French Quarter', 'category': 'attraction', 'address': 'New Orleans, LA, USA', 'lat': 29.9575, 'lon': -90.0658},
        {'dest_id': 'neworleans001', 'name': 'Bourbon Street', 'category': 'attraction', 'address': 'New Orleans, LA, USA', 'lat': 29.9583, 'lon': -90.0667},
        {'dest_id': 'neworleans001', 'name': 'The National WWII Museum', 'category': 'attraction', 'address': '945 Magazine St, New Orleans, LA 70130, USA', 'lat': 29.9419, 'lon': -90.0683},
        {'dest_id': 'neworleans001', 'name': 'Commander\'s Palace', 'category': 'restaurant', 'address': '1403 Washington Ave, New Orleans, LA 70130, USA', 'lat': 29.9286, 'lon': -90.0833},

        {'dest_id': 'washingtondc001', 'name': 'Lincoln Memorial', 'category': 'attraction', 'address': '2 Lincoln Memorial Cir NW, Washington, DC 20037, USA', 'lat': 38.8893, 'lon': -77.0502},
        {'dest_id': 'washingtondc001', 'name': 'National Mall', 'category': 'attraction', 'address': 'Washington, DC, USA', 'lat': 38.8895, 'lon': -77.0227},
        {'dest_id': 'washingtondc001', 'name': 'Smithsonian National Museum of Natural History', 'category': 'attraction', 'address': '10th St. & Constitution Ave. NW, Washington, DC 20560, USA', 'lat': 38.8913, 'lon': -77.0261},
        {'dest_id': 'washingtondc001', 'name': 'Old Ebbitt Grill', 'category': 'restaurant', 'address': '675 15th St NW, Washington, DC 20005, USA', 'lat': 38.8986, 'lon': -77.0336},

        {'dest_id': 'boston001', 'name': 'Freedom Trail', 'category': 'attraction', 'address': 'Boston, MA, USA', 'lat': 42.3601, 'lon': -71.0589},
        {'dest_id': 'boston001', 'name': 'Faneuil Hall Marketplace', 'category': 'attraction', 'address': '4 S Market St, Boston, MA 02109, USA', 'lat': 42.3601, 'lon': -71.0558},
        {'dest_id': 'boston001', 'name': 'Fenway Park', 'category': 'attraction', 'address': '4 Jersey St, Boston, MA 02215, USA', 'lat': 42.3467, 'lon': -71.0972},
        {'dest_id': 'boston001', 'name': 'Union Oyster House', 'category': 'restaurant', 'address': '41 Union St, Boston, MA 02108, USA', 'lat': 42.3614, 'lon': -71.0572},

        {'dest_id': 'seattle001', 'name': 'Space Needle', 'category': 'attraction', 'address': '400 Broad St, Seattle, WA 98109, USA', 'lat': 47.6205, 'lon': -122.3493},
        {'dest_id': 'seattle001', 'name': 'Pike Place Market', 'category': 'attraction', 'address': '85 Pike St, Seattle, WA 98101, USA', 'lat': 47.6093, 'lon': -122.3422},
        {'dest_id': 'seattle001', 'name': 'Chihuly Garden and Glass', 'category': 'attraction', 'address': '305 Harrison St, Seattle, WA 98109, USA', 'lat': 47.6200, 'lon': -122.3500},
        {'dest_id': 'seattle001', 'name': 'The Pink Door', 'category': 'restaurant', 'address': '1919 Post Alley, Seattle, WA 98101, USA', 'lat': 47.6106, 'lon': -122.3422},

        {'dest_id': 'montreal001', 'name': 'Old Montreal', 'category': 'attraction', 'address': 'Montreal, QC, Canada', 'lat': 45.5069, 'lon': -73.5539},
        {'dest_id': 'montreal001', 'name': 'Notre-Dame Basilica of Montreal', 'category': 'attraction', 'address': '110 Notre-Dame St W, Montreal, Quebec H2Y 1T1, Canada', 'lat': 45.5045, 'lon': -73.5564},
        {'dest_id': 'montreal001', 'name': 'Mount Royal Park', 'category': 'attraction', 'address': '1260 Remembrance Rd, Montreal, Quebec H3H 1A2, Canada', 'lat': 45.5047, 'lon': -73.5881},
        {'dest_id': 'montreal001', 'name': 'Au Pied de Cochon', 'category': 'restaurant', 'address': '536 Avenue Duluth E, Montréal, QC H2L 1A9, Canada', 'lat': 45.5219, 'lon': -73.5819},

        {'dest_id': 'quebeccity001', 'name': 'Old Quebec', 'category': 'attraction', 'address': 'Quebec City, QC, Canada', 'lat': 46.8123, 'lon': -71.2085},
        {'dest_id': 'quebeccity001', 'name': 'Fairmont Le Château Frontenac', 'category': 'attraction', 'address': '1 Rue des Carrières, Québec, QC G1R 4P5, Canada', 'lat': 46.8122, 'lon': -71.2047},
        {'dest_id': 'quebeccity001', 'name': 'Plains of Abraham', 'category': 'attraction', 'address': '835 Wilfrid-Laurier Ave, Quebec City, Quebec G1R 2L3, Canada', 'lat': 46.8033, 'lon': -71.2167},
        {'dest_id': 'quebeccity001', 'name': 'Le Continental', 'category': 'restaurant', 'address': '26 Rue Saint-Louis, Québec, QC G1R 3Y9, Canada', 'lat': 46.8117, 'lon': -71.2069},

        {'dest_id': 'cusco001', 'name': 'Plaza de Armas', 'category': 'attraction', 'address': 'Cusco, Peru', 'lat': -13.5167, 'lon': -71.9783},
        {'dest_id': 'cusco001', 'name': 'Sacsayhuamán', 'category': 'attraction', 'address': 'Cusco, Peru', 'lat': -13.5083, 'lon': -71.9819},
        {'dest_id': 'cusco001', 'name': 'Qorikancha', 'category': 'attraction', 'address': 'Plazoleta de Santo Domingo, Cusco, Peru', 'lat': -13.5208, 'lon': -71.9758},
        {'dest_id': 'cusco001', 'name': 'Chicha por Gastón Acurio', 'category': 'restaurant', 'address': 'Plaza Regocijo 261, Cusco, Peru', 'lat': -13.5169, 'lon': -71.9806},

        {'dest_id': 'bogota001', 'name': 'Gold Museum (Museo del Oro)', 'category': 'attraction', 'address': 'Cra. 6 #15-88, Bogotá, Colombia', 'lat': 4.6019, 'lon': -74.0722},
        {'dest_id': 'bogota001', 'name': 'Mount Monserrate', 'category': 'attraction', 'address': 'Bogotá, Colombia', 'lat': 4.6050, 'lon': -74.0567},
        {'dest_id': 'bogota001', 'name': 'La Candelaria', 'category': 'attraction', 'address': 'Bogotá, Colombia', 'lat': 4.5967, 'lon': -74.0717},
        {'dest_id': 'bogota001', 'name': 'Andrés Carne de Res', 'category': 'restaurant', 'address': 'Calle 3 #11a-56, Chía, Cundinamarca, Colombia', 'lat': 4.8569, 'lon': -74.0519},

        {'dest_id': 'medellin001', 'name': 'Comuna 13', 'category': 'attraction', 'address': 'Medellín, Antioquia, Colombia', 'lat': 6.2519, 'lon': -75.6183},
        {'dest_id': 'medellin001', 'name': 'Plaza Botero', 'category': 'attraction', 'address': 'Carabobo, Medellín, Antioquia, Colombia', 'lat': 6.2519, 'lon': -75.5683},
        {'dest_id': 'medellin001', 'name': 'Metrocable', 'category': 'attraction', 'address': 'Medellín, Antioquia, Colombia', 'lat': 6.2867, 'lon': -75.5500},
        {'dest_id': 'medellin001', 'name': 'El Cielo', 'category': 'restaurant', 'address': 'Cra. 40 #10a-22, Medellín, Antioquia, Colombia', 'lat': 6.2089, 'lon': -75.5689},

        {'dest_id': 'santiago001', 'name': 'Cerro San Cristóbal', 'category': 'attraction', 'address': 'Santiago, Chile', 'lat': -33.4244, 'lon': -70.6214},
        {'dest_id': 'santiago001', 'name': 'Cerro Santa Lucía', 'category': 'attraction', 'address': 'Santiago, Chile', 'lat': -33.4383, 'lon': -70.6383},
        {'dest_id': 'santiago001', 'name': 'Costanera Center', 'category': 'attraction', 'address': 'Av. Andrés Bello 2425, Providencia, Santiago, Chile', 'lat': -33.4175, 'lon': -70.6067},
        {'dest_id': 'santiago001', 'name': 'Bocanáriz', 'category': 'restaurant', 'address': 'José Victorino Lastarria 276, Santiago, Chile', 'lat': -33.4367, 'lon': -70.6367},

        {'dest_id': 'lapaz001', 'name': 'Mi Teleférico', 'category': 'attraction', 'address': 'La Paz, Bolivia', 'lat': -16.5000, 'lon': -68.1500},
        {'dest_id': 'lapaz001', 'name': 'Witches\' Market', 'category': 'attraction', 'address': 'Melchor Jimenez, La Paz, Bolivia', 'lat': -16.4950, 'lon': -68.1383},
        {'dest_id': 'lapaz001', 'name': 'Valle de la Luna', 'category': 'attraction', 'address': 'Mallasa, La Paz, Bolivia', 'lat': -16.5500, 'lon': -68.1000},
        {'dest_id': 'lapaz001', 'name': 'Gustu', 'category': 'restaurant', 'address': 'Calacoto Calle 10, La Paz, Bolivia', 'lat': -16.5333, 'lon': -68.0833},

        {'dest_id': 'uyuni001', 'name': 'Salar de Uyuni', 'category': 'attraction', 'address': 'Uyuni, Bolivia', 'lat': -20.4633, 'lon': -66.8251},
        {'dest_id': 'uyuni001', 'name': 'Isla Incahuasi', 'category': 'attraction', 'address': 'Salar de Uyuni, Bolivia', 'lat': -20.2408, 'lon': -67.6250},
        {'dest_id': 'uyuni001', 'name': 'Train Cemetery', 'category': 'attraction', 'address': 'Uyuni, Bolivia', 'lat': -20.4783, 'lon': -66.8217},
        {'dest_id': 'uyuni001', 'name': 'Tika', 'category': 'restaurant', 'address': 'Av. Arce, Uyuni, Bolivia', 'lat': -20.4633, 'lon': -66.8251},

        {'dest_id': 'quito001', 'name': 'TelefériQo', 'category': 'attraction', 'address': 'Quito, Ecuador', 'lat': -0.1833, 'lon': -78.5167},
        {'dest_id': 'quito001', 'name': 'Quito Old Town', 'category': 'attraction', 'address': 'Quito, Ecuador', 'lat': -0.2167, 'lon': -78.5167},
        {'dest_id': 'quito001', 'name': 'Middle of the World (Mitad del Mundo)', 'category': 'attraction', 'address': 'San Antonio de Pichincha, Ecuador', 'lat': -0.0022, 'lon': -78.4558},
        {'dest_id': 'quito001', 'name': 'Zazu', 'category': 'restaurant', 'address': 'Mariano Aguilera 331, Quito, Ecuador', 'lat': -0.1833, 'lon': -78.4833},

        {'dest_id': 'easterisland001', 'name': 'Rano Raraku', 'category': 'attraction', 'address': 'Easter Island, Chile', 'lat': -27.1233, 'lon': -109.2883},
        {'dest_id': 'easterisland001', 'name': 'Ahu Tongariki', 'category': 'attraction', 'address': 'Easter Island, Chile', 'lat': -27.1283, 'lon': -109.2450},
        {'dest_id': 'easterisland001', 'name': 'Anakena Beach', 'category': 'attraction', 'address': 'Easter Island, Chile', 'lat': -27.0733, 'lon': -109.3233},
        {'dest_id': 'easterisland001', 'name': 'Te Moana', 'category': 'restaurant', 'address': 'Atamu Tekena, Hanga Roa, Easter Island, Chile', 'lat': -27.1433, 'lon': -109.4283},

        {'dest_id': 'iguazufalls001', 'name': 'Iguazu Falls (Brazilian side)', 'category': 'attraction', 'address': 'Foz do Iguaçu, State of Paraná, Brazil', 'lat': -25.6953, 'lon': -54.4367},
        {'dest_id': 'iguazufalls001', 'name': 'Iguazu Falls (Argentinian side)', 'category': 'attraction', 'address': 'Puerto Iguazú, Misiones Province, Argentina', 'lat': -25.6953, 'lon': -54.4367},
        {'dest_id': 'iguazufalls001', 'name': 'Garganta del Diablo (Devil\'s Throat)', 'category': 'attraction', 'address': 'Misiones Province, Argentina', 'lat': -25.6917, 'lon': -54.4417},
        {'dest_id': 'iguazufalls001', 'name': 'Restaurante Porto Canoas', 'category': 'restaurant', 'address': 'Foz do Iguaçu, State of Paraná, Brazil', 'lat': -25.6833, 'lon': -54.4500},

        {'dest_id': 'torresdelpaine001', 'name': 'Mirador Las Torres', 'category': 'attraction', 'address': 'Torres del Paine National Park, Chile', 'lat': -50.9417, 'lon': -72.8833},
        {'dest_id': 'torresdelpaine001', 'name': 'Grey Glacier', 'category': 'attraction', 'address': 'Torres del Paine National Park, Chile', 'lat': -51.0500, 'lon': -73.2500},
        {'dest_id': 'torresdelpaine001', 'name': 'Pehoé Lake', 'category': 'attraction', 'address': 'Torres del Paine National Park, Chile', 'lat': -51.0833, 'lon': -72.9667},
        {'dest_id': 'torresdelpaine001', 'name': 'Hotel Lago Grey Restaurant', 'category': 'restaurant', 'address': 'Torres del Paine National Park, Chile', 'lat': -51.1000, 'lon': -73.1333},

        {'dest_id': 'grandcanyon001', 'name': 'Mather Point', 'category': 'attraction', 'address': 'Grand Canyon Village, AZ 86023, USA', 'lat': 36.0617, 'lon': -112.1094},
        {'dest_id': 'grandcanyon001', 'name': 'Yavapai Point', 'category': 'attraction', 'address': 'Grand Canyon Village, AZ 86023, USA', 'lat': 36.0667, 'lon': -112.1167},
        {'dest_id': 'grandcanyon001', 'name': 'Bright Angel Trail', 'category': 'attraction', 'address': 'Grand Canyon Village, AZ 86023, USA', 'lat': 36.0583, 'lon': -112.1433},
        {'dest_id': 'grandcanyon001', 'name': 'El Tovar Dining Room', 'category': 'restaurant', 'address': '1 El Tovar Rd, Grand Canyon Village, AZ 86023, USA', 'lat': 36.0583, 'lon': -112.1383},

        {'dest_id': 'yellowstone001', 'name': 'Old Faithful', 'category': 'attraction', 'address': 'Yellowstone National Park, WY 82190, USA', 'lat': 44.4605, 'lon': -110.8281},
        {'dest_id': 'yellowstone001', 'name': 'Grand Prismatic Spring', 'category': 'attraction', 'address': 'Yellowstone National Park, WY 82190, USA', 'lat': 44.5250, 'lon': -110.8383},
        {'dest_id': 'yellowstone001', 'name': 'Grand Canyon of the Yellowstone', 'category': 'attraction', 'address': 'Yellowstone National Park, WY 82190, USA', 'lat': 44.7167, 'lon': -110.4833},
        {'dest_id': 'yellowstone001', 'name': 'Old Faithful Inn Dining Room', 'category': 'restaurant', 'address': '3200 Old Faithful Inn Rd, Yellowstone National Park, WY 82190, USA', 'lat': 44.4600, 'lon': -110.8300},

        {'dest_id': 'zion001', 'name': 'Zion Canyon Scenic Drive', 'category': 'attraction', 'address': 'Zion National Park, UT, USA', 'lat': 37.2982, 'lon': -113.0263},
        {'dest_id': 'zion001', 'name': 'The Narrows', 'category': 'attraction', 'address': 'Zion National Park, UT, USA', 'lat': 37.3000, 'lon': -112.9500},
        {'dest_id': 'zion001', 'name': 'Angels Landing', 'category': 'attraction', 'address': 'Zion National Park, UT, USA', 'lat': 37.2692, 'lon': -112.9508},
        {'dest_id': 'zion001', 'name': 'Spotted Dog Cafe', 'category': 'restaurant', 'address': '428 Zion Park Blvd, Springdale, UT 84767, USA', 'lat': 37.1958, 'lon': -112.9903},
        
                # --- International - Middle East & Africa ---
        {'dest_id': 'dubai001', 'name': 'Burj Khalifa', 'category': 'attraction', 'address': '1 Sheikh Mohammed bin Rashid Blvd, Downtown Dubai, Dubai, UAE', 'lat': 25.1972, 'lon': 55.2744},
        {'dest_id': 'dubai001', 'name': 'The Dubai Mall', 'category': 'attraction', 'address': 'Financial Center Street, Along Sheikh Zayed Road, Dubai, UAE', 'lat': 25.1982, 'lon': 55.2795},
        {'dest_id': 'dubai001', 'name': 'The Dubai Fountain', 'category': 'attraction', 'address': 'Sheikh Mohammed bin Rashid Blvd, Downtown Dubai, Dubai, UAE', 'lat': 25.1950, 'lon': 55.2758},
        {'dest_id': 'dubai001', 'name': 'Pierchic', 'category': 'restaurant', 'address': 'Al Qasr at Madinat Jumeirah, Dubai, UAE', 'lat': 25.1319, 'lon': 55.1836},

        {'dest_id': 'cairo001', 'name': 'Pyramids of Giza', 'category': 'attraction', 'address': 'Al Haram, Giza Governorate, Egypt', 'lat': 29.9792, 'lon': 31.1342},
        {'dest_id': 'cairo001', 'name': 'The Egyptian Museum', 'category': 'attraction', 'address': 'Tahrir Square, Meret Basha, Ismailia, Qasr an Nile, Cairo Governorate, Egypt', 'lat': 30.0478, 'lon': 31.2336},
        {'dest_id': 'cairo001', 'name': 'Khan el-Khalili', 'category': 'attraction', 'address': 'El-Gamaleya, El Gamaliya, Cairo Governorate, Egypt', 'lat': 30.0478, 'lon': 31.2623},
        {'dest_id': 'cairo001', 'name': 'Abou El Sid', 'category': 'restaurant', 'address': '157 26th of July Corridor, Zamalek, Cairo Governorate, Egypt', 'lat': 30.0600, 'lon': 31.2217},

        {'dest_id': 'petra001', 'name': 'The Treasury (Al-Khazneh)', 'category': 'attraction', 'address': 'Petra - Wadi Musa, Jordan', 'lat': 30.3225, 'lon': 35.4519},
        {'dest_id': 'petra001', 'name': 'The Monastery (Ad-Deir)', 'category': 'attraction', 'address': 'Petra - Wadi Musa, Jordan', 'lat': 30.3383, 'lon': 35.4383},
        {'dest_id': 'petra001', 'name': 'Siq', 'category': 'attraction', 'address': 'Petra - Wadi Musa, Jordan', 'lat': 30.3167, 'lon': 35.4667},
        {'dest_id': 'petra001', 'name': 'The Basin Restaurant', 'category': 'restaurant', 'address': 'Petra - Wadi Musa, Jordan', 'lat': 30.3285, 'lon': 35.4444},

        {'dest_id': 'marrakech001', 'name': 'Jemaa el-Fnaa', 'category': 'attraction', 'address': 'Marrakesh 40000, Morocco', 'lat': 31.6258, 'lon': -7.9892},
        {'dest_id': 'marrakech001', 'name': 'Jardin Majorelle', 'category': 'attraction', 'address': 'Rue Yves St Laurent, Marrakesh 40090, Morocco', 'lat': 31.6422, 'lon': -8.0000},
        {'dest_id': 'marrakech001', 'name': 'Bahia Palace', 'category': 'attraction', 'address': 'Avenue Imam El Ghazali, Marrakesh 40000, Morocco', 'lat': 31.6231, 'lon': -7.9819},
        {'dest_id': 'marrakech001', 'name': 'Nomad', 'category': 'restaurant', 'address': '1 Derb Aarjane, Marrakesh 40000, Morocco', 'lat': 31.6283, 'lon': -7.9883},

        {'dest_id': 'cappadocia001', 'name': 'Göreme Open-Air Museum', 'category': 'attraction', 'address': '50180 Göreme/Nevşehir Merkez/Nevşehir, Turkey', 'lat': 38.6389, 'lon': 34.8450},
        {'dest_id': 'cappadocia001', 'name': 'Hot Air Balloon Ride', 'category': 'attraction', 'address': 'Göreme, Cappadocia, Turkey', 'lat': 38.6431, 'lon': 34.8285},
        {'dest_id': 'cappadocia001', 'name': 'Uçhisar Castle', 'category': 'attraction', 'address': 'Tekelli, 50240 Uçhisar/Nevşehir Merkez/Nevşehir, Turkey', 'lat': 38.6319, 'lon': 34.8050},
        {'dest_id': 'cappadocia001', 'name': 'Topdeck Cave Restaurant', 'category': 'restaurant', 'address': 'Hafiz Abdullah Efendi Sk. No 15, 50180 Göreme/Nevşehir, Turkey', 'lat': 38.6417, 'lon': 34.8283},

        {'dest_id': 'serengeti001', 'name': 'Seronera Valley', 'category': 'attraction', 'address': 'Serengeti National Park, Tanzania', 'lat': -2.4333, 'lon': 34.8333},
        {'dest_id': 'serengeti001', 'name': 'Grumeti River', 'category': 'attraction', 'address': 'Serengeti National Park, Tanzania', 'lat': -2.0000, 'lon': 34.2500},
        {'dest_id': 'serengeti001', 'name': 'Naabi Hill', 'category': 'attraction', 'address': 'Serengeti National Park, Tanzania', 'lat': -2.8167, 'lon': 34.9833},
        {'dest_id': 'serengeti001', 'name': 'Serengeti Serena Safari Lodge Restaurant', 'category': 'restaurant', 'address': 'Serengeti National Park, Tanzania', 'lat': -2.4333, 'lon': 34.8333},

        {'dest_id': 'capetown001', 'name': 'Table Mountain', 'category': 'attraction', 'address': 'Table Mountain, Cape Town, South Africa', 'lat': -33.9625, 'lon': 18.4033},
        {'dest_id': 'capetown001', 'name': 'Robben Island', 'category': 'attraction', 'address': 'Robben Island, Cape Town, South Africa', 'lat': -33.8000, 'lon': 18.3667},
        {'dest_id': 'capetown001', 'name': 'Boulders Beach Penguin Colony', 'category': 'attraction', 'address': 'Kleintuin Rd, Simon\'s Town, Cape Town, 7995, South Africa', 'lat': -34.1972, 'lon': 18.4511},
        {'dest_id': 'capetown001', 'name': 'The Test Kitchen', 'category': 'restaurant', 'address': 'The Old Biscuit Mill, 375 Albert Rd, Woodstock, Cape Town, 7915, South Africa', 'lat': -33.9281, 'lon': 18.4589},

        {'dest_id': 'jerusalem001', 'name': 'Western Wall', 'category': 'attraction', 'address': 'Jerusalem', 'lat': 31.7767, 'lon': 35.2344},
        {'dest_id': 'jerusalem001', 'name': 'Church of the Holy Sepulchre', 'category': 'attraction', 'address': 'Jerusalem', 'lat': 31.7785, 'lon': 35.2298},
        {'dest_id': 'jerusalem001', 'name': 'Dome of the Rock', 'category': 'attraction', 'address': 'Jerusalem', 'lat': 31.7780, 'lon': 35.2354},
        {'dest_id': 'jerusalem001', 'name': 'Machneyuda', 'category': 'restaurant', 'address': 'Beit Ya\'akov St 10, Jerusalem, Israel', 'lat': 31.7850, 'lon': 35.2133},

        {'dest_id': 'vicfalls001', 'name': 'Victoria Falls', 'category': 'attraction', 'address': 'Mosi-o-tunya Road, Livingstone, Zambia', 'lat': -17.9244, 'lon': 25.8572},
        {'dest_id': 'vicfalls001', 'name': 'Devil\'s Pool', 'category': 'attraction', 'address': 'Livingstone Island, Zambia', 'lat': -17.9250, 'lon': 25.8583},
        {'dest_id': 'vicfalls001', 'name': 'Zambezi River Sunset Cruise', 'category': 'attraction', 'address': 'Livingstone, Zambia', 'lat': -17.8500, 'lon': 25.8333},
        {'dest_id': 'vicfalls001', 'name': 'The Lookout Cafe', 'category': 'restaurant', 'address': 'Batoka Gorges, Victoria Falls, Zimbabwe', 'lat': -17.9167, 'lon': 25.8500},

        {'dest_id': 'zanzibar001', 'name': 'Stone Town', 'category': 'attraction', 'address': 'Zanzibar City, Tanzania', 'lat': -6.1650, 'lon': 39.1950},
        {'dest_id': 'zanzibar001', 'name': 'Nungwi Beach', 'category': 'attraction', 'address': 'Nungwi, Zanzibar, Tanzania', 'lat': -5.7333, 'lon': 39.3000},
        {'dest_id': 'zanzibar001', 'name': 'Prison Island', 'category': 'attraction', 'address': 'Zanzibar, Tanzania', 'lat': -6.1167, 'lon': 39.1667},
        {'dest_id': 'zanzibar001', 'name': 'The Rock Restaurant', 'category': 'restaurant', 'address': 'Pingwe, Michamvi, Zanzibar, Tanzania', 'lat': -6.2167, 'lon': 39.4667},

        {'dest_id': 'abudhabi001', 'name': 'Sheikh Zayed Grand Mosque', 'category': 'attraction', 'address': 'Sheikh Rashid Bin Saeed Street, Abu Dhabi, UAE', 'lat': 24.4128, 'lon': 54.4744},
        {'dest_id': 'abudhabi001', 'name': 'Louvre Abu Dhabi', 'category': 'attraction', 'address': 'Saadiyat, Abu Dhabi, UAE', 'lat': 24.5350, 'lon': 54.3967},
        {'dest_id': 'abudhabi001', 'name': 'Emirates Palace', 'category': 'attraction', 'address': 'West Corniche Road, Abu Dhabi, UAE', 'lat': 24.4600, 'lon': 54.3167},
        {'dest_id': 'abudhabi001', 'name': 'Hakkasan Abu Dhabi', 'category': 'restaurant', 'address': 'Emirates Palace, West Corniche Road, Abu Dhabi, UAE', 'lat': 24.4600, 'lon': 54.3167},

        {'dest_id': 'kruger001', 'name': 'Sabie Sand Game Reserve', 'category': 'attraction', 'address': 'Sabi Sand, South Africa', 'lat': -24.7500, 'lon': 31.5000},
        {'dest_id': 'kruger001', 'name': 'Olifants River', 'category': 'attraction', 'address': 'Kruger National Park, South Africa', 'lat': -23.9833, 'lon': 31.7500},
        {'dest_id': 'kruger001', 'name': 'Lower Sabie Rest Camp', 'category': 'attraction', 'address': 'Kruger National Park, South Africa', 'lat': -25.1167, 'lon': 31.9167},
        {'dest_id': 'kruger001', 'name': 'Cattle Baron Skukuza', 'category': 'restaurant', 'address': 'Skukuza Rest Camp, Kruger National Park, South Africa', 'lat': -24.9945, 'lon': 31.5872},

        {'dest_id': 'luxor001', 'name': 'Valley of the Kings', 'category': 'attraction', 'address': 'Luxor, Luxor Governorate, Egypt', 'lat': 25.7403, 'lon': 32.6014},
        {'dest_id': 'luxor001', 'name': 'Karnak Temple', 'category': 'attraction', 'address': 'Karnak, Luxor, Luxor Governorate, Egypt', 'lat': 25.7189, 'lon': 32.6572},
        {'dest_id': 'luxor001', 'name': 'Luxor Temple', 'category': 'attraction', 'address': 'Luxor City, Luxor, Luxor Governorate, Egypt', 'lat': 25.7006, 'lon': 32.6394},
        {'dest_id': 'luxor001', 'name': 'Sofra Restaurant & Cafe', 'category': 'restaurant', 'address': '90 Mohamed Farid St, Luxor, Luxor Governorate, Egypt', 'lat': 25.7000, 'lon': 32.6333},

        {'dest_id': 'fes001', 'name': 'Fes el-Bali (Old Fes)', 'category': 'attraction', 'address': 'Fes, Morocco', 'lat': 34.0667, 'lon': -4.9833},
        {'dest_id': 'fes001', 'name': 'Al-Attarine Madrasa', 'category': 'attraction', 'address': 'Rue Talaa Kebira, Fes, Morocco', 'lat': 34.0656, 'lon': -4.9739},
        {'dest_id': 'fes001', 'name': 'Chouara Tannery', 'category': 'attraction', 'address': 'Fes, Morocco', 'lat': 34.0667, 'lon': -4.9700},
        {'dest_id': 'fes001', 'name': 'The Ruined Garden', 'category': 'restaurant', 'address': '18 Derb Idrissy, Siaj, Fes, Morocco', 'lat': 34.0633, 'lon': -4.9817},

        {'dest_id': 'doha001', 'name': 'Museum of Islamic Art', 'category': 'attraction', 'address': 'Doha, Qatar', 'lat': 25.2956, 'lon': 51.5386},
        {'dest_id': 'doha001', 'name': 'Souq Waqif', 'category': 'attraction', 'address': 'Doha, Qatar', 'lat': 25.2878, 'lon': 51.5333},
        {'dest_id': 'doha001', 'name': 'The Pearl-Qatar', 'category': 'attraction', 'address': 'Doha, Qatar', 'lat': 25.3667, 'lon': 51.5500},
        {'dest_id': 'doha001', 'name': 'Parisa Souq Waqif', 'category': 'restaurant', 'address': 'Souq Waqif, Doha, Qatar', 'lat': 25.2878, 'lon': 51.5333},

        {'dest_id': 'muscat001', 'name': 'Sultan Qaboos Grand Mosque', 'category': 'attraction', 'address': 'Sultan Qaboos St, Muscat, Oman', 'lat': 23.5850, 'lon': 58.3883},
        {'dest_id': 'muscat001', 'name': 'Muttrah Souq', 'category': 'attraction', 'address': 'Muttrah, Muscat, Oman', 'lat': 23.6217, 'lon': 58.5667},
        {'dest_id': 'muscat001', 'name': 'Royal Opera House Muscat', 'category': 'attraction', 'address': 'Sultan Qaboos St, Muscat, Oman', 'lat': 23.6133, 'lon': 58.4683},
        {'dest_id': 'muscat001', 'name': 'Bait Al Luban Omani Restaurant', 'category': 'restaurant', 'address': 'Muttrah, Muscat, Oman', 'lat': 23.6217, 'lon': 58.5667},

        {'dest_id': 'telaviv001', 'name': 'Jaffa Old City', 'category': 'attraction', 'address': 'Jaffa, Tel Aviv-Yafo, Israel', 'lat': 32.0544, 'lon': 34.7522},
        {'dest_id': 'telaviv001', 'name': 'Carmel Market (Shuk HaCarmel)', 'category': 'attraction', 'address': 'HaCarmel St 48, Tel Aviv-Yafo, Israel', 'lat': 32.0683, 'lon': 34.7683},
        {'dest_id': 'telaviv001', 'name': 'Tel Aviv Museum of Art', 'category': 'attraction', 'address': 'Sderot Sha\'ul HaMelech 27, Tel Aviv-Yafo, Israel', 'lat': 32.0792, 'lon': 34.7917},
        {'dest_id': 'telaviv001', 'name': 'Abu Hassan/Ali Karavan', 'category': 'restaurant', 'address': 'Ha-Dolfin St 1, Tel Aviv-Yafo, Israel', 'lat': 32.0533, 'lon': 34.7517},

        {'dest_id': 'nairobi001', 'name': 'Nairobi National Park', 'category': 'attraction', 'address': 'Nairobi, Kenya', 'lat': -1.3667, 'lon': 36.8500},
        {'dest_id': 'nairobi001', 'name': 'David Sheldrick Wildlife Trust', 'category': 'attraction', 'address': 'Magadi Rd, Nairobi, Kenya', 'lat': -1.3500, 'lon': 36.7833},
        {'dest_id': 'nairobi001', 'name': 'Giraffe Centre', 'category': 'attraction', 'address': 'Langata, Nairobi, Kenya', 'lat': -1.3667, 'lon': 36.7500},
        {'dest_id': 'nairobi001', 'name': 'Carnivore Restaurant', 'category': 'restaurant', 'address': 'Langata Road, Nairobi, Kenya', 'lat': -1.3333, 'lon': 36.7833},

        {'dest_id': 'maasaimara001', 'name': 'Maasai Mara National Reserve', 'category': 'attraction', 'address': 'Narok County, Kenya', 'lat': -1.5000, 'lon': 35.0000},
        {'dest_id': 'maasaimara001', 'name': 'Mara River', 'category': 'attraction', 'address': 'Maasai Mara, Kenya', 'lat': -1.5000, 'lon': 34.7500},
        {'dest_id': 'maasaimara001', 'name': 'Maasai Village Visit', 'category': 'attraction', 'address': 'Maasai Mara, Kenya', 'lat': -1.5000, 'lon': 35.0000},
        {'dest_id': 'maasaimara001', 'name': 'Sanctuary Olonana', 'category': 'restaurant', 'address': 'Maasai Mara, Kenya', 'lat': -1.4167, 'lon': 35.0833},

        {'dest_id': 'okavango001', 'name': 'Moremi Game Reserve', 'category': 'attraction', 'address': 'Okavango Delta, Botswana', 'lat': -19.2500, 'lon': 23.3333},
        {'dest_id': 'okavango001', 'name': 'Mokoro Trip', 'category': 'attraction', 'address': 'Okavango Delta, Botswana', 'lat': -19.4333, 'lon': 23.3167},
        {'dest_id': 'okavango001', 'name': 'Chief\'s Island', 'category': 'attraction', 'address': 'Okavango Delta, Botswana', 'lat': -19.5000, 'lon': 23.0000},
        {'dest_id': 'okavango001', 'name': 'The Old Bridge Backpackers', 'category': 'restaurant', 'address': 'Maun, Botswana', 'lat': -19.9833, 'lon': 23.4333},

        {'dest_id': 'addisababa001', 'name': 'National Museum of Ethiopia', 'category': 'attraction', 'address': 'Arat Kilo, Addis Ababa, Ethiopia', 'lat': 9.0333, 'lon': 38.7667},
        {'dest_id': 'addisababa001', 'name': 'Holy Trinity Cathedral', 'category': 'attraction', 'address': 'Arat Kilo, Addis Ababa, Ethiopia', 'lat': 9.0300, 'lon': 38.7667},
        {'dest_id': 'addisababa001', 'name': 'Mercato', 'category': 'attraction', 'address': 'Addis Ketema, Addis Ababa, Ethiopia', 'lat': 9.0333, 'lon': 38.7333},
        {'dest_id': 'addisababa001', 'name': 'Yod Abyssinia Traditional Restaurant', 'category': 'restaurant', 'address': 'Bole, Addis Ababa, Ethiopia', 'lat': 8.9833, 'lon': 38.7833},

        {'dest_id': 'seychelles001', 'name': 'Anse Source d\'Argent', 'category': 'attraction', 'address': 'La Digue, Seychelles', 'lat': -4.3667, 'lon': 55.8333},
        {'dest_id': 'seychelles001', 'name': 'Vallée de Mai Nature Reserve', 'category': 'attraction', 'address': 'Praslin, Seychelles', 'lat': -4.3167, 'lon': 55.7333},
        {'dest_id': 'seychelles001', 'name': 'Beau Vallon Beach', 'category': 'attraction', 'address': 'Mahé, Seychelles', 'lat': -4.6167, 'lon': 55.4333},
        {'dest_id': 'seychelles001', 'name': 'La Plage Restaurant', 'category': 'restaurant', 'address': 'Beau Vallon, Mahé, Seychelles', 'lat': -4.6167, 'lon': 55.4333},

        {'dest_id': 'mauritius001', 'name': 'Le Morne Brabant', 'category': 'attraction', 'address': 'Le Morne, Mauritius', 'lat': -20.4500, 'lon': 57.3167},
        {'dest_id': 'mauritius001', 'name': 'Black River Gorges National Park', 'category': 'attraction', 'address': 'B103, Mauritius', 'lat': -20.4167, 'lon': 57.4167},
        {'dest_id': 'mauritius001', 'name': 'Chamarel Seven Coloured Earth Geopark', 'category': 'attraction', 'address': 'Chamarel, Mauritius', 'lat': -20.4333, 'lon': 57.3667},
        {'dest_id': 'mauritius001', 'name': 'Le Château de Bel Ombre', 'category': 'restaurant', 'address': 'Bel Ombre, Mauritius', 'lat': -20.5000, 'lon': 57.4000},

        {'dest_id': 'windhoek001', 'name': 'Christuskirche', 'category': 'attraction', 'address': 'Robert Mugabe Ave, Windhoek, Namibia', 'lat': -22.5644, 'lon': 17.0867},
        {'dest_id': 'windhoek001', 'name': 'Namibia Craft Centre', 'category': 'attraction', 'address': '40 Tal St, Windhoek, Namibia', 'lat': -22.5683, 'lon': 17.0850},
        {'dest_id': 'windhoek001', 'name': 'Independence Museum', 'category': 'attraction', 'address': 'Robert Mugabe Ave, Windhoek, Namibia', 'lat': -22.5650, 'lon': 17.0867},
        {'dest_id': 'windhoek001', 'name': 'Joe\'s Beerhouse', 'category': 'restaurant', 'address': '160 Nelson Mandela Ave, Windhoek, Namibia', 'lat': -22.5533, 'lon': 17.0833},

        {'dest_id': 'sossusvlei001', 'name': 'Deadvlei', 'category': 'attraction', 'address': 'Namib-Naukluft National Park, Namibia', 'lat': -24.7583, 'lon': 15.2917},
        {'dest_id': 'sossusvlei001', 'name': 'Dune 45', 'category': 'attraction', 'address': 'Namib-Naukluft National Park, Namibia', 'lat': -24.7333, 'lon': 15.0833},
        {'dest_id': 'sossusvlei001', 'name': 'Sesriem Canyon', 'category': 'attraction', 'address': 'Namib-Naukluft National Park, Namibia', 'lat': -24.5167, 'lon': 15.8000},
        {'dest_id': 'sossusvlei001', 'name': 'Sossusvlei Lodge Restaurant', 'category': 'restaurant', 'address': 'Sesriem, Namibia', 'lat': -24.5167, 'lon': 15.8000},

        {'dest_id': 'chefchaouen001', 'name': 'Chefchaouen Medina', 'category': 'attraction', 'address': 'Chefchaouen, Morocco', 'lat': 35.1717, 'lon': -5.2667},
        {'dest_id': 'chefchaouen001', 'name': 'Ras El Maa Waterfall', 'category': 'attraction', 'address': 'Chefchaouen, Morocco', 'lat': 35.1667, 'lon': -5.2500},
        {'dest_id': 'chefchaouen001', 'name': 'Kasbah Museum', 'category': 'attraction', 'address': 'Plaza Uta el-Hammam, Chefchaouen, Morocco', 'lat': 35.1700, 'lon': -5.2667},
        {'dest_id': 'chefchaouen001', 'name': 'Restaurant Bab Ssour', 'category': 'restaurant', 'address': 'Rue Al Andalous, Chefchaouen, Morocco', 'lat': 35.1717, 'lon': -5.2667},

        {'dest_id': 'dakar001', 'name': 'African Renaissance Monument', 'category': 'attraction', 'address': 'Ouakam, Dakar, Senegal', 'lat': 14.7217, 'lon': -17.5000},
        {'dest_id': 'dakar001', 'name': 'Île de Gorée', 'category': 'attraction', 'address': 'Dakar, Senegal', 'lat': 14.6667, 'lon': -17.4000},
        {'dest_id': 'dakar001', 'name': 'Lake Retba (Lac Rose)', 'category': 'attraction', 'address': 'Dakar, Senegal', 'lat': 14.8333, 'lon': -17.2333},
        {'dest_id': 'dakar001', 'name': 'La Calebasse', 'category': 'restaurant', 'address': 'Route de la Corniche Est, Dakar, Senegal', 'lat': 14.6667, 'lon': -17.4167},

        {'dest_id': 'accra001', 'name': 'Kwame Nkrumah Memorial Park & Mausoleum', 'category': 'attraction', 'address': 'High St, Accra, Ghana', 'lat': 5.5483, 'lon': -0.2033},
        {'dest_id': 'accra001', 'name': 'Makola Market', 'category': 'attraction', 'address': 'Accra, Ghana', 'lat': 5.5500, 'lon': -0.2000},
        {'dest_id': 'accra001', 'name': 'Jamestown Lighthouse', 'category': 'attraction', 'address': 'Accra, Ghana', 'lat': 5.5333, 'lon': -0.2167},
        {'dest_id': 'accra001', 'name': 'Buka Restaurant', 'category': 'restaurant', 'address': '10th St, Osu, Accra, Ghana', 'lat': 5.5667, 'lon': -0.1833},

        {'dest_id': 'lagos001', 'name': 'Lekki Conservation Centre', 'category': 'attraction', 'address': 'Lekki Penninsula II, Lekki, Lagos, Nigeria', 'lat': 6.4500, 'lon': 3.5667},
        {'dest_id': 'lagos001', 'name': 'Nike Art Gallery', 'category': 'attraction', 'address': '2 Elegushi Rd, Lekki Phase I, Lagos, Nigeria', 'lat': 6.4333, 'lon': 3.4833},
        {'dest_id': 'lagos001', 'name': 'Freedom Park', 'category': 'attraction', 'address': 'Old Prison Ground, Broad St, Lagos Island, Lagos, Nigeria', 'lat': 6.4500, 'lon': 3.3833},
        {'dest_id': 'lagos001', 'name': 'Nok by Alara', 'category': 'restaurant', 'address': '12a Akin Olugbade St, Victoria Island, Lagos, Nigeria', 'lat': 6.4333, 'lon': 3.4333},

        {'dest_id': 'antananarivo001', 'name': 'Rova of Antananarivo', 'category': 'attraction', 'address': 'Antananarivo, Madagascar', 'lat': -18.9233, 'lon': 47.5283},
        {'dest_id': 'antananarivo001', 'name': 'Lemurs\' Park', 'category': 'attraction', 'address': 'RN 1, Antananarivo, Madagascar', 'lat': -18.9667, 'lon': 47.3667},
        {'dest_id': 'antananarivo001', 'name': 'Analakely Market', 'category': 'attraction', 'address': 'Analakely, Antananarivo, Madagascar', 'lat': -18.9167, 'lon': 47.5167},
        {'dest_id': 'antananarivo001', 'name': 'La Varangue', 'category': 'restaurant', 'address': '17 Rue Printsy Ratsimamanga, Antananarivo, Madagascar', 'lat': -18.9167, 'lon': 47.5167},

        {'dest_id': 'gorillatrek001', 'name': 'Volcanoes National Park HQ', 'category': 'attraction', 'address': 'Kinigi, Ruhengeri, Rwanda', 'lat': -1.4589, 'lon': 29.5936},
        {'dest_id': 'gorillatrek001', 'name': 'Dian Fossey Gorilla Fund', 'category': 'attraction', 'address': 'Musanze, Rwanda', 'lat': -1.4984, 'lon': 29.6200},
        {'dest_id': 'gorillatrek001', 'name': 'Iby\'iwacu Cultural Village', 'category': 'attraction', 'address': 'Kinigi, Musanze District, Rwanda', 'lat': -1.4402, 'lon': 29.5816},
        {'dest_id': 'gorillatrek001', 'name': 'La Locanda', 'category': 'restaurant', 'address': 'Musanze, Rwanda', 'lat': -1.5008, 'lon': 29.6335}
        ]

    try:
        # Insert all destinations
        cursor.executemany('''
        INSERT OR IGNORE INTO destinations (id, name, city, country, description, tags, lat, lon, cost_tier)
        VALUES (:id, :name, :city, :country, :description, :tags, :lat, :lon, :cost_tier)
        ''', curated_data)
        conn.commit()
        print(f"Successfully added/updated {len(curated_data)} destinations.")

        # Insert the new curated landmarks
        cursor.executemany('''
        INSERT INTO landmarks (destination_id, name, category, address, lat, lon)
        VALUES (:dest_id, :name, :category, :address, :lat, :lon)
        ''', curated_landmarks)
        conn.commit()
        print(f"Successfully added {len(curated_landmarks)} curated landmarks.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    create_and_populate_db()
    print("Database `travel.db` has been created and populated successfully.")