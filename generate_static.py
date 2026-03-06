#!/usr/bin/env python3
"""
Static Site Generator for WeatherReportAPP
Generates static HTML files for GitHub Pages deployment
"""

import os
import json
import shutil
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

def generate_static_site():
    """Generate static HTML files for GitHub Pages"""
    
    # Create output directory
    output_dir = Path('_site')
    output_dir.mkdir(exist_ok=True)
    
    # Copy static assets
    if Path('static').exists():
        if (output_dir / 'static').exists():
            shutil.rmtree(output_dir / 'static')
        shutil.copytree('static', output_dir / 'static')
    
    # Set up Jinja2 environment with Flask-like functions
    env = Environment(loader=FileSystemLoader('templates'))
    
    # Define url_for function for static assets
    def url_for(endpoint, **values):
        if endpoint == 'static':
            return f"static/{values['filename']}"
        return f"/{endpoint}"
    
    # Add Flask-like functions to the environment
    env.globals['url_for'] = url_for
    
    # Generate main index.html
    template = env.get_template('index.html')
    
    # Render the template with static asset paths
    html_content = template.render()
    
    # Write index.html to output directory
    with open(output_dir / 'index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # Create a simple API mock for demo purposes
    api_dir = output_dir / 'api'
    api_dir.mkdir(exist_ok=True)
    
    # Generate sample weather data for demo
    sample_cities = {
        'new-york': {
            'city': 'New York',
            'country': 'United States',
            'temp': 22,
            'condition': 'Clear',
            'humidity': 65,
            'wind_speed': 12,
            'wind_dir': 'NW',
            'pressure': 1013,
            'visibility': 10,
            'uv_index': 6,
            'feels_like': 24,
            'precipitation': 0,
            'sunrise': '06:30',
            'sunset': '19:15',
            'timestamp': '2024-01-01T12:00:00',
            'forecast': [
                {'day': 0, 'high': 27, 'low': 19, 'condition': 'Clear', 'precip': 0},
                {'day': 1, 'high': 24, 'low': 17, 'condition': 'Partly Cloudy', 'precip': 10},
                {'day': 2, 'high': 23, 'low': 16, 'condition': 'Cloudy', 'precip': 20},
                {'day': 3, 'high': 21, 'low': 14, 'condition': 'Light Rain', 'precip': 60},
                {'day': 4, 'high': 25, 'low': 18, 'condition': 'Sunny', 'precip': 0}
            ]
        },
        'london': {
            'city': 'London',
            'country': 'United Kingdom',
            'temp': 15,
            'condition': 'Cloudy',
            'humidity': 78,
            'wind_speed': 8,
            'wind_dir': 'SW',
            'pressure': 1008,
            'visibility': 8,
            'uv_index': 3,
            'feels_like': 13,
            'precipitation': 2,
            'sunrise': '07:45',
            'sunset': '18:30',
            'timestamp': '2024-01-01T12:00:00',
            'forecast': [
                {'day': 0, 'high': 18, 'low': 12, 'condition': 'Cloudy', 'precip': 30},
                {'day': 1, 'high': 16, 'low': 10, 'condition': 'Rainy', 'precip': 80},
                {'day': 2, 'high': 14, 'low': 8, 'condition': 'Overcast', 'precip': 40},
                {'day': 3, 'high': 17, 'low': 11, 'condition': 'Partly Cloudy', 'precip': 20},
                {'day': 4, 'high': 19, 'low': 13, 'condition': 'Clear', 'precip': 5}
            ]
        },
        'tokyo': {
            'city': 'Tokyo',
            'country': 'Japan',
            'temp': 26,
            'condition': 'Sunny',
            'humidity': 58,
            'wind_speed': 7,
            'wind_dir': 'E',
            'pressure': 1018,
            'visibility': 15,
            'uv_index': 8,
            'feels_like': 28,
            'precipitation': 0,
            'sunrise': '05:45',
            'sunset': '18:20',
            'timestamp': '2024-01-01T12:00:00',
            'forecast': [
                {'day': 0, 'high': 29, 'low': 23, 'condition': 'Sunny', 'precip': 0},
                {'day': 1, 'high': 27, 'low': 21, 'condition': 'Clear', 'precip': 0},
                {'day': 2, 'high': 25, 'low': 19, 'condition': 'Partly Cloudy', 'precip': 10},
                {'day': 3, 'high': 24, 'low': 18, 'condition': 'Cloudy', 'precip': 30},
                {'day': 4, 'high': 26, 'low': 20, 'condition': 'Clear', 'precip': 5}
            ]
        }
    }
    
    # Create API endpoints as JSON files
    weather_dir = api_dir / 'weather'
    weather_dir.mkdir(exist_ok=True)
    
    for city_key, data in sample_cities.items():
        with open(weather_dir / f'{city_key}.json', 'w') as f:
            json.dump(data, f, indent=2)
    
    # Create search API mock
    search_dir = api_dir / 'search'
    search_dir.mkdir(exist_ok=True)
    
    search_data = {
        'cities': [
            {'name': 'New York', 'country': 'United States', 'key': 'new-york'},
            {'name': 'London', 'country': 'United Kingdom', 'key': 'london'},
            {'name': 'Tokyo', 'country': 'Japan', 'key': 'tokyo'},
            {'name': 'Paris', 'country': 'France', 'key': 'paris'},
            {'name': 'Sydney', 'country': 'Australia', 'key': 'sydney'},
            {'name': 'Mumbai', 'country': 'India', 'key': 'mumbai'},
            {'name': 'Berlin', 'country': 'Germany', 'key': 'berlin'},
            {'name': 'Los Angeles', 'country': 'United States', 'key': 'los-angeles'},
        ]
    }
    
    with open(search_dir / 'cities.json', 'w') as f:
        json.dump(search_data, f, indent=2)
    
    # Create a static JavaScript file that works with static JSON
    static_js_content = '''
// Modified app.js for static deployment
const API_BASE = window.location.origin;

// Override the original functions to work with static JSON files
window.originalFetch = window.fetch;

// Custom fetch for static files
async function staticFetch(url) {
    try {
        if (url.includes('/api/weather/')) {
            const city = url.split('/api/weather/')[1].toLowerCase().replace(/\\s+/g, '-');
            const response = await window.originalFetch(`${API_BASE}/api/weather/${city}.json`);
            return response;
        } else if (url.includes('/api/search/')) {
            const response = await window.originalFetch(`${API_BASE}/api/search/cities.json`);
            return response;
        }
        return window.originalFetch(url);
    } catch (error) {
        console.error('Static fetch error:', error);
        throw error;
    }
}

// Replace global fetch for our app
window.fetch = staticFetch;

console.log('WeatherReportAPP - Static mode enabled');
console.log('Demo data available for: New York, London, Tokyo, Paris, Sydney, Mumbai, Berlin, Los Angeles');
    '''.strip()
    
    # Write the modified JavaScript
    with open(output_dir / 'static' / 'js' / 'static-adapter.js', 'w') as f:
        f.write(static_js_content)
    
    # Create a modified index.html that includes the static adapter
    with open(output_dir / 'index.html', 'r') as f:
        html_content = f.read()
    
    # Add the static adapter script before the closing </body> tag
    static_script = '<script src="static/js/static-adapter.js"></script>'
    html_content = html_content.replace('</body>', f'{static_script}\n</body>')
    
    # Add note about demo mode
    demo_banner = '''
    <div style="position: fixed; top: 0; left: 0; right: 0; background: #2563eb; color: white; text-align: center; padding: 8px; z-index: 10000; font-size: 14px;">
        📡 Demo Mode - Showing sample weather data for demonstration
    </div>
    <style>body { padding-top: 40px !important; }</style>
    '''
    html_content = html_content.replace('<body>', f'<body>{demo_banner}')
    
    with open(output_dir / 'index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ Static site generated successfully!")
    print(f"📁 Output directory: {output_dir.absolute()}")
    print("🌐 Ready for GitHub Pages deployment")

if __name__ == '__main__':
    generate_static_site()