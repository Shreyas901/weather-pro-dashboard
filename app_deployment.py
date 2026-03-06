"""
Weather Pro - Flask application with MCP client integration
Production/Deployment version
"""

from flask import Flask, render_template, jsonify, request
import asyncio
import json
import os
import logging
from datetime import datetime

# Import MCP client with fallback
try:
    from mcp_weather_client import mcp_client
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    print("Warning: MCP client not available, using fallback data only")

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Production configuration
if os.environ.get('FLASK_ENV') == 'production':
    app.config['DEBUG'] = False
else:
    app.config['DEBUG'] = True

def run_async(coro):
    """Helper function to run async functions in Flask routes"""
    if not MCP_AVAILABLE:
        return None
        
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    return loop.run_until_complete(coro)

# Fallback weather data
FALLBACK_WEATHER_DATA = {
    'new york': {
        'city': 'New York', 'country': 'United States', 'temp': 22, 'condition': 'Clear',
        'humidity': 65, 'wind_speed': 12, 'wind_dir': 'NW', 'wind_deg': 315,
        'pressure': 1013, 'visibility': 10, 'uv_index': 6, 'feels_like': 24,
        'precipitation': 0, 'wind_gust': 18, 'sunrise': '06:30', 'sunset': '19:15',
        'forecast': [
            {'day': 0, 'high': 27, 'low': 19, 'condition': 'Clear', 'precip': 0},
            {'day': 1, 'high': 24, 'low': 17, 'condition': 'Partly Cloudy', 'precip': 10},
            {'day': 2, 'high': 23, 'low': 16, 'condition': 'Cloudy', 'precip': 20},
            {'day': 3, 'high': 21, 'low': 14, 'condition': 'Light Rain', 'precip': 60},
            {'day': 4, 'high': 25, 'low': 18, 'condition': 'Sunny', 'precip': 0}
        ]
    },
    'london': {
        'city': 'London', 'country': 'United Kingdom', 'temp': 15, 'condition': 'Cloudy',
        'humidity': 78, 'wind_speed': 8, 'wind_dir': 'SW', 'wind_deg': 225,
        'pressure': 1008, 'visibility': 8, 'uv_index': 3, 'feels_like': 13,
        'precipitation': 2, 'wind_gust': 15, 'sunrise': '07:45', 'sunset': '18:30',
        'forecast': [
            {'day': 0, 'high': 18, 'low': 12, 'condition': 'Cloudy', 'precip': 30},
            {'day': 1, 'high': 16, 'low': 10, 'condition': 'Rainy', 'precip': 80},
            {'day': 2, 'high': 14, 'low': 8, 'condition': 'Overcast', 'precip': 40},
            {'day': 3, 'high': 17, 'low': 11, 'condition': 'Partly Cloudy', 'precip': 20},
            {'day': 4, 'high': 19, 'low': 13, 'condition': 'Clear', 'precip': 5}
        ]
    },
    'tokyo': {
        'city': 'Tokyo', 'country': 'Japan', 'temp': 26, 'condition': 'Sunny',
        'humidity': 58, 'wind_speed': 7, 'wind_dir': 'E', 'wind_deg': 90,
        'pressure': 1018, 'visibility': 15, 'uv_index': 8, 'feels_like': 28,
        'precipitation': 0, 'wind_gust': 12, 'sunrise': '05:45', 'sunset': '18:20',
        'forecast': [
            {'day': 0, 'high': 29, 'low': 23, 'condition': 'Sunny', 'precip': 0},
            {'day': 1, 'high': 27, 'low': 21, 'condition': 'Clear', 'precip': 0},
            {'day': 2, 'high': 25, 'low': 19, 'condition': 'Partly Cloudy', 'precip': 10},
            {'day': 3, 'high': 24, 'low': 18, 'condition': 'Cloudy', 'precip': 30},
            {'day': 4, 'high': 26, 'low': 20, 'condition': 'Clear', 'precip': 5}
        ]
    }
}

# Initialize MCP client when the app starts (if available)
@app.before_request
def initialize_mcp():
    """Initialize MCP client connections on first request"""
    if not MCP_AVAILABLE:
        return
        
    if not hasattr(initialize_mcp, 'called'):
        try:
            logger.info("Initializing MCP weather client...")
            run_async(mcp_client.connect_to_servers())
            logger.info("MCP weather client initialized successfully")
            initialize_mcp.called = True
        except Exception as e:
            logger.error(f"Failed to initialize MCP client: {e}")
            initialize_mcp.called = True  # Prevent repeated attempts

@app.route('/')
def index():
    """Main weather dashboard page"""
    return render_template('index.html')

@app.route('/api/weather/<city>')
def get_weather(city):
    """API endpoint to get complete weather data for a city"""
    try:
        logger.info(f"Getting weather data for city: {city}")
        
        # Try MCP client first if available
        if MCP_AVAILABLE:
            try:
                weather_data = run_async(mcp_client.get_weather_data(city))
                if weather_data:
                    weather_data['timestamp'] = datetime.now().isoformat()
                    logger.info(f"Successfully retrieved weather data for {city} via MCP")
                    return jsonify(weather_data)
            except Exception as e:
                logger.warning(f"MCP client failed for {city}: {e}")
        
        # Fallback to static data
        city_key = city.lower().strip()
        if city_key in FALLBACK_WEATHER_DATA:
            weather_data = FALLBACK_WEATHER_DATA[city_key].copy()
            weather_data['timestamp'] = datetime.now().isoformat()
            logger.info(f"Using fallback data for {city}")
            return jsonify(weather_data)
        
        # No data available
        return jsonify({'error': 'Weather data not available for this city'}), 404
    
    except Exception as e:
        logger.error(f"Error in get_weather for {city}: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/search/<query>')
def search_cities(query):
    """API endpoint to search for cities"""
    try:
        logger.info(f"Searching for cities with query: {query}")
        
        # Try MCP client first if available
        if MCP_AVAILABLE:
            try:
                cities = run_async(mcp_client.search_cities(query))
                if cities:
                    logger.info(f"Found {len(cities)} cities for query: {query} via MCP")
                    return jsonify({'cities': cities})
            except Exception as e:
                logger.warning(f"MCP search failed for {query}: {e}")
        
        # Fallback search
        available_cities = [
            {'name': 'New York', 'country': 'United States', 'key': 'new york'},
            {'name': 'London', 'country': 'United Kingdom', 'key': 'london'},
            {'name': 'Tokyo', 'country': 'Japan', 'key': 'tokyo'},
            {'name': 'Paris', 'country': 'France', 'key': 'paris'},
            {'name': 'Sydney', 'country': 'Australia', 'key': 'sydney'},
            {'name': 'Mumbai', 'country': 'India', 'key': 'mumbai'},
            {'name': 'Berlin', 'country': 'Germany', 'key': 'berlin'},
            {'name': 'Los Angeles', 'country': 'United States', 'key': 'los angeles'},
        ]
        
        query_lower = query.lower()
        matching_cities = [
            city for city in available_cities 
            if query_lower in city['name'].lower() or query_lower in city['country'].lower()
        ]
        
        logger.info(f"Found {len(matching_cities)} cities for query: {query} (fallback)")
        return jsonify({'cities': matching_cities})
    
    except Exception as e:
        logger.error(f"Error in search_cities for {query}: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/status')
def mcp_status():
    """API endpoint to check MCP client status"""
    try:
        if MCP_AVAILABLE:
            status = {
                'mcp_services': len(getattr(mcp_client, 'active_servers', {})),
                'config_loaded': bool(getattr(mcp_client, 'config', None)),
                'fallback_cities': len(FALLBACK_WEATHER_DATA),
                'mcp_available': True,
                'timestamp': datetime.now().isoformat()
            }
        else:
            status = {
                'mcp_services': 0,
                'config_loaded': False,
                'fallback_cities': len(FALLBACK_WEATHER_DATA),
                'mcp_available': False,
                'timestamp': datetime.now().isoformat()
            }
        return jsonify(status)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    logger.info("Starting Weather Pro application...")
    if not MCP_AVAILABLE:
        logger.warning("Running in fallback mode - MCP client unavailable")
    
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                    Weather Pro - Deployment Ready           ║
    ║                                                              ║
    ║  🌤️  Advanced Weather Dashboard                            ║
    ║                                                              ║
    ║  Features:                                                   ║
    ║  • Production-ready configuration                           ║
    ║  • Fallback weather data for demo                           ║
    ║  • MCP integration (when available)                         ║
    ║  • Responsive modern UI                                      ║
    ║                                                              ║
    ║  🌐 Ready for deployment on multiple platforms             ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    app.run(host='0.0.0.0', port=port, debug=debug)