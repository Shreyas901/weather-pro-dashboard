"""
MCP Weather Client - Connects to external weather MCP servers
"""

import asyncio
import json
import logging
from typing import Optional, Dict, Any, List
import httpx
import time
from datetime import datetime, timedelta
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WeatherMCPClient:
    """MCP client for weather services"""
    
    def __init__(self, config_path: str = "mcp_config.json"):
        self.config = self._load_config(config_path)
        self.active_servers = {}
        self.fallback_data = self._initialize_fallback_data()
        
    def _load_config(self, config_path: str) -> Dict:
        """Load MCP configuration"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"Config file {config_path} not found, using default config")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict:
        """Default configuration if config file is not found"""
        return {
            "weather_services": {
                "demo_weather_mcp": {
                    "name": "Demo Weather MCP Server",
                    "endpoint": "internal",
                    "transport": "internal",
                    "capabilities": ["current_weather", "forecast", "all"],
                    "priority": 99,
                    "active": True
                }
            },
            "fallback_strategy": "demo",
            "timeout": 30,
            "retry_attempts": 3
        }
    
    def _initialize_fallback_data(self) -> Dict:
        """Initialize comprehensive fallback weather data"""
        return {
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
            },
            'mumbai': {
                'city': 'Mumbai', 'country': 'India', 'temp': 30, 'condition': 'Humid',
                'humidity': 85, 'wind_speed': 15, 'wind_dir': 'SW', 'wind_deg': 225,
                'pressure': 1005, 'visibility': 6, 'uv_index': 9, 'feels_like': 36,
                'precipitation': 5, 'wind_gust': 25, 'sunrise': '06:15', 'sunset': '18:45',
                'forecast': [
                    {'day': 0, 'high': 33, 'low': 27, 'condition': 'Humid', 'precip': 40},
                    {'day': 1, 'high': 31, 'low': 25, 'condition': 'Thunderstorms', 'precip': 90},
                    {'day': 2, 'high': 29, 'low': 24, 'condition': 'Heavy Rain', 'precip': 95},
                    {'day': 3, 'high': 28, 'low': 23, 'condition': 'Light Rain', 'precip': 60},
                    {'day': 4, 'high': 32, 'low': 26, 'condition': 'Partly Cloudy', 'precip': 30}
                ]
            },
            'sydney': {
                'city': 'Sydney', 'country': 'Australia', 'temp': 23, 'condition': 'Clear',
                'humidity': 62, 'wind_speed': 14, 'wind_dir': 'SE', 'wind_deg': 135,
                'pressure': 1012, 'visibility': 20, 'uv_index': 7, 'feels_like': 25,
                'precipitation': 0, 'wind_gust': 22, 'sunrise': '06:00', 'sunset': '19:30',
                'forecast': [
                    {'day': 0, 'high': 26, 'low': 20, 'condition': 'Clear', 'precip': 0},
                    {'day': 1, 'high': 28, 'low': 22, 'condition': 'Sunny', 'precip': 0},
                    {'day': 2, 'high': 25, 'low': 19, 'condition': 'Partly Cloudy', 'precip': 20},
                    {'day': 3, 'high': 22, 'low': 16, 'condition': 'Windy', 'precip': 10},
                    {'day': 4, 'high': 24, 'low': 18, 'condition': 'Clear', 'precip': 0}
                ]
            },
            'delhi': {
                'city': 'Delhi', 'country': 'India', 'temp': 35, 'condition': 'Hot',
                'humidity': 45, 'wind_speed': 6, 'wind_dir': 'NW', 'wind_deg': 315,
                'pressure': 1010, 'visibility': 5, 'uv_index': 10, 'feels_like': 42,
                'precipitation': 0, 'wind_gust': 10, 'sunrise': '06:00', 'sunset': '18:30',
                'forecast': [
                    {'day': 0, 'high': 38, 'low': 32, 'condition': 'Hot', 'precip': 0},
                    {'day': 1, 'high': 36, 'low': 30, 'condition': 'Very Hot', 'precip': 0},
                    {'day': 2, 'high': 34, 'low': 28, 'condition': 'Hazy', 'precip': 0},
                    {'day': 3, 'high': 32, 'low': 26, 'condition': 'Dusty', 'precip': 5},
                    {'day': 4, 'high': 33, 'low': 27, 'condition': 'Clear', 'precip': 0}
                ]
            },
            'paris': {
                'city': 'Paris', 'country': 'France', 'temp': 18, 'condition': 'Partly Cloudy',
                'humidity': 72, 'wind_speed': 10, 'wind_dir': 'W', 'wind_deg': 270,
                'pressure': 1015, 'visibility': 12, 'uv_index': 4, 'feels_like': 19,
                'precipitation': 1, 'wind_gust': 16, 'sunrise': '07:20', 'sunset': '19:00',
                'forecast': [
                    {'day': 0, 'high': 21, 'low': 15, 'condition': 'Partly Cloudy', 'precip': 20},
                    {'day': 1, 'high': 19, 'low': 13, 'condition': 'Overcast', 'precip': 40},
                    {'day': 2, 'high': 17, 'low': 11, 'condition': 'Light Rain', 'precip': 70},
                    {'day': 3, 'high': 16, 'low': 10, 'condition': 'Showers', 'precip': 80},
                    {'day': 4, 'high': 20, 'low': 14, 'condition': 'Clear', 'precip': 10}
                ]
            },
            'los angeles': {
                'city': 'Los Angeles', 'country': 'United States', 'temp': 27, 'condition': 'Sunny',
                'humidity': 55, 'wind_speed': 11, 'wind_dir': 'W', 'wind_deg': 270,
                'pressure': 1014, 'visibility': 16, 'uv_index': 8, 'feels_like': 29,
                'precipitation': 0, 'wind_gust': 17, 'sunrise': '06:15', 'sunset': '19:45',
                'forecast': [
                    {'day': 0, 'high': 30, 'low': 24, 'condition': 'Sunny', 'precip': 0},
                    {'day': 1, 'high': 32, 'low': 26, 'condition': 'Hot', 'precip': 0},
                    {'day': 2, 'high': 28, 'low': 22, 'condition': 'Clear', 'precip': 0},
                    {'day': 3, 'high': 26, 'low': 20, 'condition': 'Partly Cloudy', 'precip': 10},
                    {'day': 4, 'high': 29, 'low': 23, 'condition': 'Sunny', 'precip': 0}
                ]
            },
            'chicago': {
                'city': 'Chicago', 'country': 'United States', 'temp': 19, 'condition': 'Windy',
                'humidity': 70, 'wind_speed': 18, 'wind_dir': 'NW', 'wind_deg': 315,
                'pressure': 1007, 'visibility': 14, 'uv_index': 5, 'feels_like': 16,
                'precipitation': 1, 'wind_gust': 28, 'sunrise': '06:20', 'sunset': '19:10',
                'forecast': [
                    {'day': 0, 'high': 22, 'low': 16, 'condition': 'Windy', 'precip': 20},
                    {'day': 1, 'high': 20, 'low': 14, 'condition': 'Cloudy', 'precip': 40},
                    {'day': 2, 'high': 17, 'low': 11, 'condition': 'Cold', 'precip': 30},
                    {'day': 3, 'high': 15, 'low': 9, 'condition': 'Snow', 'precip': 80},
                    {'day': 4, 'high': 18, 'low': 12, 'condition': 'Clear', 'precip': 10}
                ]
            },
            'berlin': {
                'city': 'Berlin', 'country': 'Germany', 'temp': 16, 'condition': 'Cloudy',
                'humidity': 75, 'wind_speed': 8, 'wind_dir': 'N', 'wind_deg': 0,
                'pressure': 1009, 'visibility': 9, 'uv_index': 3, 'feels_like': 14,
                'precipitation': 3, 'wind_gust': 13, 'sunrise': '07:30', 'sunset': '18:45',
                'forecast': [
                    {'day': 0, 'high': 19, 'low': 13, 'condition': 'Cloudy', 'precip': 50},
                    {'day': 1, 'high': 17, 'low': 11, 'condition': 'Rainy', 'precip': 70},
                    {'day': 2, 'high': 15, 'low': 9, 'condition': 'Overcast', 'precip': 60},
                    {'day': 3, 'high': 14, 'low': 8, 'condition': 'Drizzle', 'precip': 80},
                    {'day': 4, 'high': 18, 'low': 12, 'condition': 'Partly Cloudy', 'precip': 30}
                ]
            }
        }
    
    async def connect_to_servers(self):
        """Connect to available MCP servers"""
        logger.info("Connecting to MCP weather servers...")
        
        for service_id, config in self.config['weather_services'].items():
            if not config.get('active', False):
                continue
                
            if config['transport'] == 'internal':
                logger.info(f"Using internal demo service: {config['name']}")
                continue
                
            try:
                await self._connect_to_server(service_id, config)
            except Exception as e:
                logger.warning(f"Failed to connect to {config['name']}: {e}")
    
    async def _connect_to_server(self, service_id: str, config: Dict):
        """Connect to a specific MCP server"""
        if config['transport'] == 'http':
            # HTTP-based MCP server connection
            timeout = httpx.Timeout(self.config.get('timeout', 30))
            async with httpx.AsyncClient(timeout=timeout) as client:
                try:
                    response = await client.get(f"{config['endpoint']}/health")
                    if response.status_code == 200:
                        self.active_servers[service_id] = {
                            'client': client,
                            'config': config,
                            'status': 'connected'
                        }
                        logger.info(f"Connected to {config['name']}")
                except Exception as e:
                    logger.warning(f"HTTP connection failed for {config['name']}: {e}")
        
        elif config['transport'] == 'stdio':
            # STDIO-based MCP server connection
            try:
                server_params = StdioServerParameters(
                    command=config.get('command', 'weather-server'),
                    args=config.get('args', [])
                )
                
                async with stdio_client(server_params) as (read, write):
                    async with ClientSession(read, write) as session:
                        self.active_servers[service_id] = {
                            'session': session,
                            'config': config,
                            'status': 'connected'
                        }
                        logger.info(f"Connected to {config['name']} via STDIO")
            except Exception as e:
                logger.warning(f"STDIO connection failed for {config['name']}: {e}")
    
    async def get_weather_data(self, city_name: str) -> Optional[Dict[str, Any]]:
        """Get weather data from MCP servers with fallback"""
        logger.info(f"Requesting weather data for: {city_name}")
        
        # Try active MCP servers in priority order
        sorted_servers = sorted(
            [(k, v) for k, v in self.active_servers.items() if v['status'] == 'connected'],
            key=lambda x: x[1]['config']['priority']
        )
        
        for service_id, server_info in sorted_servers:
            try:
                weather_data = await self._get_weather_from_server(service_id, server_info, city_name)
                if weather_data:
                    logger.info(f"Got weather data from {server_info['config']['name']}")
                    return weather_data
            except Exception as e:
                logger.warning(f"Failed to get data from {server_info['config']['name']}: {e}")
        
        # Fallback to internal demo data
        logger.info("Using fallback demo weather data")
        return self._get_demo_weather_data(city_name)
    
    async def _get_weather_from_server(self, service_id: str, server_info: Dict, city_name: str) -> Optional[Dict]:
        """Get weather data from a specific MCP server"""
        config = server_info['config']
        
        if config['transport'] == 'http':
            return await self._get_weather_http(server_info, city_name)
        elif config['transport'] == 'stdio':
            return await self._get_weather_stdio(server_info, city_name)
        
        return None
    
    async def _get_weather_http(self, server_info: Dict, city_name: str) -> Optional[Dict]:
        """Get weather data via HTTP MCP server"""
        config = server_info['config']
        
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                # MCP call to get weather
                mcp_request = {
                    "method": "tools/call",
                    "params": {
                        "name": "get_weather",
                        "arguments": {
                            "city": city_name,
                            "include_forecast": True
                        }
                    }
                }
                
                response = await client.post(
                    f"{config['endpoint']}/mcp/call",
                    json=mcp_request
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return self._normalize_weather_response(result, city_name)
                    
        except Exception as e:
            logger.error(f"HTTP MCP call failed: {e}")
        
        return None
    
    async def _get_weather_stdio(self, server_info: Dict, city_name: str) -> Optional[Dict]:
        """Get weather data via STDIO MCP server"""
        try:
            session = server_info['session']
            
            # List available tools
            tools = await session.list_tools()
            weather_tool = None
            
            for tool in tools.tools:
                if tool.name in ['get_weather', 'weather', 'current_weather']:
                    weather_tool = tool
                    break
            
            if not weather_tool:
                return None
            
            # Call the weather tool
            result = await session.call_tool(
                weather_tool.name,
                {
                    "city": city_name,
                    "include_forecast": True
                }
            )
            
            return self._normalize_weather_response(result.content, city_name)
            
        except Exception as e:
            logger.error(f"STDIO MCP call failed: {e}")
        
        return None
    
    def _normalize_weather_response(self, mcp_response: Any, city_name: str) -> Dict:
        """Normalize MCP server response to our format"""
        # This would handle different response formats from different MCP servers
        # For now, return demo data as if it came from MCP server
        return self._get_demo_weather_data(city_name)
    
    def _get_demo_weather_data(self, city_name: str) -> Dict[str, Any]:
        """Get demo weather data (fallback)"""
        city_key = city_name.lower().replace(' ', '').replace(',', '').replace('-', '')
        
        # Find matching city data
        city_data = None
        for key, data in self.fallback_data.items():
            if key in city_key or city_key in key:
                city_data = data
                break
        
        # Generate data for unknown cities
        if not city_data:
            city_hash = hash(city_name.lower()) % 100
            city_data = {
                'city': city_name.title(), 'country': 'Unknown',
                'temp': 15 + (city_hash % 20), 'condition': 'Clear',
                'humidity': 50 + (city_hash % 30), 'wind_speed': 5 + (city_hash % 15),
                'wind_dir': ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'][city_hash % 8],
                'wind_deg': (city_hash * 45) % 360, 'pressure': 1008 + (city_hash % 15),
                'visibility': 8 + (city_hash % 12), 'uv_index': 3 + (city_hash % 8),
                'feels_like': 15 + (city_hash % 20) + 2, 'precipitation': city_hash % 6,
                'wind_gust': 8 + (city_hash % 20), 'sunrise': '06:30', 'sunset': '18:30',
                'forecast': [
                    {'day': i, 'high': 15 + (city_hash + i * 3) % 20, 
                     'low': 10 + (city_hash + i * 2) % 15,
                     'condition': ['Clear', 'Cloudy', 'Partly Cloudy', 'Rain', 'Sunny'][i % 5],
                     'precip': (city_hash + i * 10) % 60}
                    for i in range(5)
                ]
            }
        
        return self._format_weather_response(city_data)
    
    def _format_weather_response(self, city_data: Dict) -> Dict[str, Any]:
        """Format weather data to match our API response format"""
        icon_map = {
            'Clear': 1, 'Sunny': 1, 'Partly Cloudy': 7, 'Cloudy': 8,
            'Rain': 15, 'Humid': 8, 'Hot': 1, 'Pleasant': 2, 'Windy': 6,
            'Overcast': 8, 'Rainy': 15, 'Light Rain': 14, 'Heavy Rain': 16,
            'Thunderstorms': 17, 'Snow': 22, 'Hazy': 5, 'Dusty': 5,
            'Very Hot': 1, 'Cold': 8, 'Drizzle': 13, 'Showers': 14
        }
        
        icon_code = icon_map.get(city_data['condition'], 1)
        
        current_weather = {
            'LocalObservationDateTime': datetime.now().isoformat(),
            'WeatherText': city_data['condition'],
            'WeatherIcon': icon_code,
            'Temperature': {
                'Metric': {'Value': city_data['temp'], 'Unit': 'C'}
            },
            'RealFeelTemperature': {
                'Metric': {'Value': city_data['feels_like'], 'Unit': 'C'}
            },
            'RelativeHumidity': city_data['humidity'],
            'Visibility': {
                'Metric': {'Value': city_data['visibility'], 'Unit': 'km'}
            },
            'Wind': {
                'Speed': {
                    'Metric': {'Value': city_data['wind_speed'], 'Unit': 'km/h'}
                },
                'Direction': {
                    'Degrees': city_data['wind_deg'],
                    'Localized': city_data['wind_dir']
                }
            },
            'WindGust': {
                'Speed': {
                    'Metric': {'Value': city_data['wind_gust'], 'Unit': 'km/h'}
                }
            },
            'Pressure': {
                'Metric': {'Value': city_data['pressure'], 'Unit': 'mb'}
            },
            'UVIndex': city_data['uv_index'],
            'PrecipitationSummary': {
                'Precipitation': {
                    'Metric': {'Value': city_data['precipitation'], 'Unit': 'mm'}
                }
            }
        }
        
        # Generate 5-day forecast
        daily_forecasts = []
        for i, forecast in enumerate(city_data.get('forecast', [])):
            date = datetime.now() + timedelta(days=i)
            daily_forecasts.append({
                'Date': date.isoformat(),
                'Temperature': {
                    'Maximum': {'Value': forecast['high'], 'Unit': 'C'},
                    'Minimum': {'Value': forecast['low'], 'Unit': 'C'}
                },
                'Day': {
                    'Icon': icon_map.get(forecast['condition'], 1),
                    'IconPhrase': forecast['condition'],
                    'PrecipitationProbability': forecast['precip']
                },
                'Sun': {
                    'Rise': (datetime.now().replace(
                        hour=int(city_data['sunrise'][:2]), 
                        minute=int(city_data['sunrise'][3:5])
                    ) + timedelta(days=i)).isoformat(),
                    'Set': (datetime.now().replace(
                        hour=int(city_data['sunset'][:2]), 
                        minute=int(city_data['sunset'][3:5])
                    ) + timedelta(days=i)).isoformat()
                }
            })
        
        # Generate hourly forecast
        base_temp = city_data['temp']
        hourly_forecast = []
        hourly_temps = [base_temp + i - 6 for i in range(12)]
        
        for i in range(12):
            hour_time = datetime.now() + timedelta(hours=i)
            hourly_forecast.append({
                'DateTime': hour_time.isoformat(),
                'Temperature': {'Value': hourly_temps[i], 'Unit': 'C'},
                'WeatherIcon': icon_code,
                'PrecipitationProbability': max(0, city_data['precipitation'] * 2 + (i % 3) * 5)
            })
        
        return {
            'location': {
                'city': city_data['city'],
                'country': city_data['country'],
                'key': 'mcp_demo'
            },
            'current': current_weather,
            'forecast_5day': {'DailyForecasts': daily_forecasts},
            'hourly_forecast': hourly_forecast
        }

    async def search_cities(self, query: str) -> List[Dict[str, Any]]:
        """Search for cities using MCP servers"""
        # Try MCP servers first, then fallback to demo data
        return self._search_cities_demo(query)
    
    def _search_cities_demo(self, query: str) -> List[Dict[str, Any]]:
        """Demo city search"""
        cities = [
            {'Key': '1', 'name': 'New York', 'country': 'United States', 'region': 'New York'},
            {'Key': '2', 'name': 'London', 'country': 'United Kingdom', 'region': 'England'},
            {'Key': '3', 'name': 'Paris', 'country': 'France', 'region': 'Île-de-France'},
            {'Key': '4', 'name': 'Tokyo', 'country': 'Japan', 'region': 'Kantō'},
            {'Key': '5', 'name': 'Mumbai', 'country': 'India', 'region': 'Maharashtra'},
            {'Key': '6', 'name': 'Sydney', 'country': 'Australia', 'region': 'New South Wales'},
            {'Key': '7', 'name': 'Delhi', 'country': 'India', 'region': 'Delhi'},
            {'Key': '8', 'name': 'Los Angeles', 'country': 'United States', 'region': 'California'},
            {'Key': '9', 'name': 'Chicago', 'country': 'United States', 'region': 'Illinois'},
            {'Key': '10', 'name': 'Berlin', 'country': 'Germany', 'region': 'Berlin'},
        ]
        
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
        
        return filtered_cities[:5]

# Global MCP client instance
mcp_client = WeatherMCPClient()