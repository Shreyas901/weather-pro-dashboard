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

# Initialize MCP client on startup
@app.before_first_request
def initialize_mcp():
    """Initialize MCP client connections"""
    try:
        asyncio.run(mcp_client.connect_to_servers())
        logger.info("MCP weather client initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize MCP client: {e}")

def run_async(coro):
    """Helper function to run async functions in Flask routes"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()

def get_demo_weather_data(city_name):
    """Generate demo weather data since we don't have a valid API key"""
    import random
    from datetime import datetime, timedelta
    
    # Demo cities data
    cities_data = {
        'new york': {'city': 'New York', 'country': 'United States', 'temp': 22, 'condition': 'Clear'},
        'london': {'city': 'London', 'country': 'United Kingdom', 'temp': 18, 'condition': 'Cloudy'},
        'paris': {'city': 'Paris', 'country': 'France', 'temp': 20, 'condition': 'Partly Cloudy'},
        'tokyo': {'city': 'Tokyo', 'country': 'Japan', 'temp': 25, 'condition': 'Sunny'},
        'mumbai': {'city': 'Mumbai', 'country': 'India', 'temp': 28, 'condition': 'Humid'},
        'sydney': {'city': 'Sydney', 'country': 'Australia', 'temp': 23, 'condition': 'Clear'},
        'delhi': {'city': 'Delhi', 'country': 'India', 'temp': 32, 'condition': 'Hot'},
        'bangalore': {'city': 'Bangalore', 'country': 'India', 'temp': 26, 'condition': 'Pleasant'},
    }
    
    # Find city data or use default
    city_key = city_name.lower().replace(' ', '').replace(',', '')
    for key in cities_data.keys():
        if key in city_key or city_key in key:
            city_data = cities_data[key]
            break
    else:
        city_data = {'city': city_name.title(), 'country': 'Unknown', 'temp': 20, 'condition': 'Clear'}
    
    base_temp = city_data['temp']
    condition = city_data['condition']
    
    # Generate weather icon code based on condition
    icon_map = {
        'Clear': 1, 'Sunny': 1, 'Partly Cloudy': 7, 'Cloudy': 8,
        'Rain': 15, 'Humid': 8, 'Hot': 1, 'Pleasant': 2
    }
    icon_code = icon_map.get(condition, 1)
    
    current_weather = {
        'LocalObservationDateTime': datetime.now().isoformat(),
        'WeatherText': condition,
        'WeatherIcon': icon_code,
        'Temperature': {
            'Metric': {'Value': base_temp, 'Unit': 'C'}
        },
        'RealFeelTemperature': {
            'Metric': {'Value': base_temp + random.randint(-2, 3), 'Unit': 'C'}
        },
        'RelativeHumidity': random.randint(40, 80),
        'Visibility': {
            'Metric': {'Value': random.randint(8, 15), 'Unit': 'km'}
        },
        'Wind': {
            'Speed': {
                'Metric': {'Value': random.randint(5, 20), 'Unit': 'km/h'}
            },
            'Direction': {
                'Degrees': random.randint(0, 360),
                'Localized': random.choice(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'])
            }
        },
        'WindGust': {
            'Speed': {
                'Metric': {'Value': random.randint(10, 30), 'Unit': 'km/h'}
            }
        },
        'Pressure': {
            'Metric': {'Value': random.randint(1000, 1020), 'Unit': 'mb'}
        },
        'UVIndex': random.randint(1, 10),
        'PrecipitationSummary': {
            'Precipitation': {
                'Metric': {'Value': random.randint(0, 5), 'Unit': 'mm'}
            }
        }
    }
    
    # Generate 5-day forecast
    daily_forecasts = []
    for i in range(5):
        date = datetime.now() + timedelta(days=i)
        high_temp = base_temp + random.randint(-3, 8)
        low_temp = high_temp - random.randint(5, 12)
        
        daily_forecasts.append({
            'Date': date.isoformat(),
            'Temperature': {
                'Maximum': {'Value': high_temp, 'Unit': 'C'},
                'Minimum': {'Value': low_temp, 'Unit': 'C'}
            },
            'Day': {
                'Icon': random.randint(1, 8),
                'IconPhrase': random.choice(['Sunny', 'Partly Cloudy', 'Cloudy', 'Light Rain']),
                'PrecipitationProbability': random.randint(0, 60)
            },
            'Sun': {
                'Rise': (datetime.now().replace(hour=6, minute=30) + timedelta(days=i)).isoformat(),
                'Set': (datetime.now().replace(hour=18, minute=45) + timedelta(days=i)).isoformat()
            }
        })
    
    forecast_5day = {'DailyForecasts': daily_forecasts}
    
    # Generate hourly forecast
    hourly_forecast = []
    for i in range(12):
        hour_time = datetime.now() + timedelta(hours=i)
        temp_variation = random.randint(-5, 5)
        hourly_forecast.append({
            'DateTime': hour_time.isoformat(),
            'Temperature': {'Value': base_temp + temp_variation, 'Unit': 'C'},
            'WeatherIcon': random.randint(1, 8),
            'PrecipitationProbability': random.randint(0, 40)
        })
    
    return {
        'location': {
            'city': city_data['city'],
            'country': city_data['country'],
            'key': 'demo'
        },
        'current': current_weather,
        'forecast_5day': forecast_5day,
        'hourly_forecast': hourly_forecast
    }

def search_cities_demo(query):
    """Generate demo city search results"""
    cities = [
        {'Key': '1', 'name': 'New York', 'country': 'United States', 'region': 'New York'},
        {'Key': '2', 'name': 'London', 'country': 'United Kingdom', 'region': 'England'},
        {'Key': '3', 'name': 'Paris', 'country': 'France', 'region': 'Île-de-France'},
        {'Key': '4', 'name': 'Tokyo', 'country': 'Japan', 'region': 'Kantō'},
        {'Key': '5', 'name': 'Mumbai', 'country': 'India', 'region': 'Maharashtra'},
        {'Key': '6', 'name': 'Sydney', 'country': 'Australia', 'region': 'New South Wales'},
        {'Key': '7', 'name': 'Delhi', 'country': 'India', 'region': 'Delhi'},
        {'Key': '8', 'name': 'Bangalore', 'country': 'India', 'region': 'Karnataka'},
        {'Key': '9', 'name': 'Los Angeles', 'country': 'United States', 'region': 'California'},
        {'Key': '10', 'name': 'Berlin', 'country': 'Germany', 'region': 'Berlin'},
    ]
    
    # Filter cities based on query
    query_lower = query.lower()
    filtered_cities = []
    for city in cities:
        if query_lower in city['name'].lower():
            filtered_cities.append({
                'key': city['Key'],
                'name': city['name'],
                'country': city['country'],
                'region': city['region'],
                'full_name': f"{city['name']}, {city['region']}, {city['country']}"
            })
    
    return filtered_cities[:5]  # Return top 5 matches

@app.route('/')
def index():
    """Main weather dashboard page"""
    return render_template('index.html')

@app.route('/api/weather/<city>')
def get_weather(city):
    """API endpoint to get complete weather data for a city"""
    try:
        # Get demo weather data
        weather_data = get_demo_weather_data(city)
        weather_data['timestamp'] = datetime.now().isoformat()
        
        return jsonify(weather_data)
    
    except Exception as e:
        print(f"Error in get_weather: {e}")  # Debug print
        return jsonify({'error': str(e)}), 500

@app.route('/api/search/<query>')
def search_cities(query):
    """API endpoint to search for cities"""
    try:
        cities = search_cities_demo(query)
        return jsonify({'cities': cities})
    
    except Exception as e:
        print(f"Error in search_cities: {e}")  # Debug print
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)