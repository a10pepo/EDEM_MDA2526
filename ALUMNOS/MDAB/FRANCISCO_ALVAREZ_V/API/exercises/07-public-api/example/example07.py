from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import requests

app = Flask(__name__)

# JWT Configuration
app.config['JWT_SECRET_KEY'] = 'super_secret_jwt_key_change_in_production'

jwt = JWTManager(app)

# Simulated database to store users
users = {
    # 'username': {'password': 'hashed_password'}
}

# OpenWeatherMap Configuration
# Get your free API key from https://openweathermap.org/api
OPENWEATHER_API_KEY = 'YOUR_API_KEY_HERE'  # Replace with your actual API key
GEOCODING_API_URL = 'https://api.openweathermap.org/geo/1.0/direct'
WEATHER_API_URL = 'https://api.openweathermap.org/data/2.5/weather'


# ============================================================================
# AUTHENTICATION ENDPOINTS (from Exercise 06)
# ============================================================================

@app.route('/register', methods=['POST'])
def register():
    """Register a new user - Public endpoint"""
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Request body must be JSON'}), 400

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    if username in users:
        return jsonify({'error': 'User already exists'}), 409

    users[username] = {
        'password': generate_password_hash(password)
    }

    return jsonify({
        'message': 'User registered successfully',
        'username': username
    }), 201


@app.route('/login', methods=['POST'])
def login():
    """Authenticate user and return JWT token - Public endpoint"""
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Request body must be JSON'}), 400

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    if username not in users:
        return jsonify({'error': 'Invalid credentials'}), 401

    if not check_password_hash(users[username]['password'], password):
        return jsonify({'error': 'Invalid credentials'}), 401

    # Create JWT access token
    access_token = create_access_token(identity=username)

    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'token_type': 'Bearer'
    }), 200


@app.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    """Get current user's profile - Protected endpoint (requires JWT)"""
    # Get the user identity from the JWT token
    current_user = get_jwt_identity()

    return jsonify({
        'username': current_user,
        'profile': f'Profile information for {current_user}'
    }), 200


# ============================================================================
# EXTERNAL API CONSUMPTION - WEATHER ENDPOINTS
# ============================================================================

@app.route('/weather', methods=['GET'])
def weather():
    """
    Get weather information for a city - Public endpoint

    This endpoint demonstrates consuming MULTIPLE external APIs:
    1. OpenWeatherMap Geocoding API: Convert city name to coordinates
    2. OpenWeatherMap Current Weather API: Get weather by coordinates

    Query Parameters:
        city (str): City name (default: 'Madrid')
        country (str): Optional ISO 3166 country code (e.g., 'ES', 'US')

    Returns:
        JSON with weather information or error message

    Note: This endpoint is PUBLIC (no JWT required) because the focus
    is on learning to consume external APIs, not authentication.
    """
    # Get parameters from query string
    city = request.args.get('city', 'Madrid')
    country_code = request.args.get('country', '')  # Optional country code

    # Validate API key is configured
    if OPENWEATHER_API_KEY == 'YOUR_API_KEY_HERE':
        return jsonify({
            'error': 'OpenWeatherMap API key not configured',
            'message': 'Please set OPENWEATHER_API_KEY in app.py',
            'help': 'Get a free API key at https://openweathermap.org/api'
        }), 500

    # ========================================================================
    # STEP 1: Get coordinates from city name using Geocoding API
    # ========================================================================

    # Build the geocoding query
    # Format: "CityName,CountryCode" (country code is optional but recommended)
    query = f"{city},{country_code}" if country_code else city

    # Build the geocoding API URL with query and API key
    geocoding_url = f'{GEOCODING_API_URL}?q={query}&appid={OPENWEATHER_API_KEY}&limit=1'

    # Make request to Geocoding API
    try:
        # Make GET request to geocoding API
        geo_response = requests.get(geocoding_url)

        # Check if the request was successful
        if geo_response.status_code != 200:
            return jsonify({
                'error': 'Geocoding API request failed',
                'status_code': geo_response.status_code,
                'message': 'Could not connect to OpenWeatherMap Geocoding API'
            }), 502

        # Parse JSON response from geocoding API
        geo_data = geo_response.json()

        # Check if city was found
        if not geo_data or len(geo_data) == 0:
            return jsonify({
                'error': 'City not found',
                'message': f'Could not find coordinates for city: {city}',
                'suggestion': 'Try adding a country code, e.g., ?city=Paris&country=FR'
            }), 404

        # Extract coordinates from first result
        latitude = geo_data[0]['lat']
        longitude = geo_data[0]['lon']

        # Get additional location info
        location_name = geo_data[0].get('name', city)
        country = geo_data[0].get('country', 'Unknown')
        state = geo_data[0].get('state', '')  # Some locations have state info

    except requests.exceptions.RequestException as e:
        return jsonify({
            'error': 'Network error',
            'message': f'Could not connect to Geocoding API: {str(e)}'
        }), 502
    except (KeyError, IndexError, ValueError) as e:
        return jsonify({
            'error': 'Invalid response from Geocoding API',
            'message': str(e)
        }), 502

    # ========================================================================
    # STEP 2: Get weather data using coordinates
    # ========================================================================

    # Build the weather API URL with coordinates and API key
    weather_url = f'{WEATHER_API_URL}?lat={latitude}&lon={longitude}&appid={OPENWEATHER_API_KEY}&units=metric&lang=en'

    try:
        # Make GET request to weather API
        weather_response = requests.get(weather_url)

        if weather_response.status_code != 200:
            return jsonify({
                'error': 'Weather API request failed',
                'status_code': weather_response.status_code,
                'message': 'Could not retrieve weather information'
            }), 502

        # Parse JSON response from weather API
        weather_data = weather_response.json()

        # Extract relevant weather information
        weather_info = {
            'location': {
                'city': location_name,
                'country': country,
                'state': state,
                'coordinates': {
                    'latitude': latitude,
                    'longitude': longitude
                }
            },
            'weather': {
                'temperature': weather_data['main']['temp'],
                'feels_like': weather_data['main']['feels_like'],
                'humidity': weather_data['main']['humidity'],
                'pressure': weather_data['main']['pressure'],
                'description': weather_data['weather'][0]['description'],
                'main': weather_data['weather'][0]['main'],
                'icon': weather_data['weather'][0]['icon']
            },
            'wind': {
                'speed': weather_data['wind']['speed'],
                'direction': weather_data['wind'].get('deg', 'N/A')
            },
            'timestamp': weather_data['dt']
        }

        return jsonify(weather_info), 200

    except requests.exceptions.RequestException as e:
        return jsonify({
            'error': 'Network error',
            'message': f'Could not connect to Weather API: {str(e)}'
        }), 502
    except (KeyError, ValueError) as e:
        return jsonify({
            'error': 'Invalid response from Weather API',
            'message': str(e)
        }), 502


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Method not allowed'}), 405


if __name__ == '__main__':
    print("\n" + "="*70)
    print("Exercise 7: Public API Consumption - Weather API")
    print("="*70)
    print("\n⚠️  IMPORTANT: Configure your OpenWeatherMap API key first!")
    print("   1. Get free API key: https://openweathermap.org/api")
    print("   2. Replace OPENWEATHER_API_KEY in example07.py")
    print("\nAuthentication endpoints:")
    print("  POST /register  - Register a new user")
    print("  POST /login     - Login and get JWT token")
    print("  GET  /profile   - Get user profile (requires JWT)")
    print("\nWeather endpoint (public - no auth required):")
    print("  GET  /weather?city=CityName&country=CountryCode")
    print("\nExamples:")
    print("  curl http://127.0.0.1:5000/weather?city=Madrid")
    print("  curl http://127.0.0.1:5000/weather?city=Paris&country=FR")
    print("  curl http://127.0.0.1:5000/weather?city=London&country=GB")
    print("\nServer running at: http://127.0.0.1:5000")
    print("="*70 + "\n")

    app.run(debug=True)
