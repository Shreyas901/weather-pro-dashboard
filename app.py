"""
Weather Pro - Flask application with MCP client integration
"""

from flask import Flask, render_template, jsonify, request
import asyncio
import json
from datetime import datetime
import os
import logging
from mcp_weather_client import mcp_client

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_async(coro):
    """Helper function to run async functions in Flask routes"""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    return loop.run_until_complete(coro)

# Initialize MCP client when the app starts
@app.before_request
def initialize_mcp():
    """Initialize MCP client connections on first request"""
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
    """API endpoint to get complete weather data for a city via MCP"""
    try:
        logger.info(f"Getting weather data for city: {city}")
        
        # Use MCP client to get weather data
        weather_data = run_async(mcp_client.get_weather_data(city))
        
        if not weather_data:
            return jsonify({'error': 'Weather data not available'}), 500
        
        weather_data['timestamp'] = datetime.now().isoformat()
        logger.info(f"Successfully retrieved weather data for {city}")
        
        return jsonify(weather_data)
    
    except Exception as e:
        logger.error(f"Error in get_weather for {city}: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/search/<query>')
def search_cities(query):
    """API endpoint to search for cities via MCP"""
    try:
        logger.info(f"Searching for cities with query: {query}")
        
        # Use MCP client to search cities
        cities = run_async(mcp_client.search_cities(query))
        
        logger.info(f"Found {len(cities)} cities for query: {query}")
        return jsonify({'cities': cities})
    
    except Exception as e:
        logger.error(f"Error in search_cities for {query}: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/status')
def mcp_status():
    """API endpoint to check MCP client status"""
    try:
        status = {
            'mcp_services': len(mcp_client.active_servers),
            'config_loaded': bool(mcp_client.config),
            'fallback_cities': len(mcp_client.fallback_data),
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
    logger.info("Starting Weather Pro application with MCP integration...")
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                    Weather Pro - MCP Edition                 ║
    ║                                                              ║
    ║  🌤️  Advanced Weather Dashboard with MCP Integration        ║
    ║                                                              ║
    ║  Features:                                                   ║
    ║  • Multi-source weather data via MCP servers                ║
    ║  • Real-time city-specific forecasts                        ║
    ║  • Fallback demo data for reliability                       ║
    ║  • Responsive modern UI                                      ║
    ║                                                              ║
    ║  🌐 Open http://127.0.0.1:5000 to view the dashboard       ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    app.run(debug=True, host='127.0.0.1', port=5000)