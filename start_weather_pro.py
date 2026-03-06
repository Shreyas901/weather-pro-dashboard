#!/usr/bin/env python3
"""
Weather Pro Startup Script with MCP Integration

This script demonstrates the MCP-integrated weather application.
It shows how different cities return different, consistent weather data
via the MCP client system.
"""

import os
import sys
import time
import subprocess
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def print_banner():
    """Print application banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════════╗
    ║                                                                  ║
    ║        🌤️  Weather Pro - MCP Integration Edition 🌤️             ║
    ║                                                                  ║
    ║  Advanced Weather Dashboard with Model Context Protocol (MCP)    ║
    ║                                                                  ║
    ║  Features:                                                       ║
    ║  ✓ Multi-source weather data via MCP servers                    ║
    ║  ✓ City-specific, consistent weather reports                    ║
    ║  ✓ Real-time forecasts and hourly predictions                   ║
    ║  ✓ Fallback demo data for maximum reliability                   ║
    ║  ✓ Modern responsive web interface                              ║
    ║  ✓ Dark/Light theme support                                     ║
    ║                                                                  ║
    ║  🏙️  Try different cities:                                       ║
    ║     • New York (Clear, 22°C)                                    ║
    ║     • London (Cloudy, 15°C)                                     ║
    ║     • Tokyo (Sunny, 26°C)                                       ║
    ║     • Mumbai (Humid, 30°C)                                      ║
    ║     • Sydney (Clear, 23°C)                                      ║
    ║     • Delhi (Hot, 35°C)                                         ║
    ║     • Paris (Partly Cloudy, 18°C)                               ║
    ║     • Los Angeles (Sunny, 27°C)                                 ║
    ║     • Chicago (Windy, 19°C)                                     ║
    ║     • Berlin (Cloudy, 16°C)                                     ║
    ║                                                                  ║
    ║  Each city shows unique, realistic weather patterns!            ║
    ║                                                                  ║
    ╚══════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = [
        'flask', 'requests', 'mcp', 'httpx', 'pydantic', 
        'anyio', 'aiohttp', 'aiofiles'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing required packages: {', '.join(missing_packages)}")
        print("📦 Installing missing packages...")
        
        for package in missing_packages:
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                print(f"✅ Installed {package}")
            except subprocess.CalledProcessError:
                print(f"❌ Failed to install {package}")
                return False
    
    print("✅ All dependencies are installed!")
    return True

def verify_files():
    """Verify that all required files exist"""
    required_files = [
        'app.py',
        'mcp_weather_client.py', 
        'mcp_config.json',
        'requirements.txt',
        'templates/index.html',
        'static/css/style.css',
        'static/js/app.js'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        return False
    
    print("✅ All required files are present!")
    return True

def show_mcp_config():
    """Display MCP configuration information"""
    print("\n🔧 MCP Configuration:")
    print("=" * 60)
    
    try:
        import json
        with open('mcp_config.json', 'r') as f:
            config = json.load(f)
        
        services = config.get('weather_services', {})
        print(f"📋 Configured MCP Services: {len(services)}")
        
        for service_id, service_config in services.items():
            status = "🟢 Active" if service_config.get('active') else "🔴 Inactive"
            print(f"  • {service_config.get('name', service_id)}: {status}")
            print(f"    Priority: {service_config.get('priority', 'N/A')}")
            print(f"    Endpoint: {service_config.get('endpoint', 'N/A')}")
            print(f"    Transport: {service_config.get('transport', 'N/A')}")
            print()
        
        print(f"⏰ Timeout: {config.get('timeout', 30)}s")
        print(f"🔄 Retry Attempts: {config.get('retry_attempts', 3)}")
        print(f"🛡️  Fallback Strategy: {config.get('fallback_strategy', 'demo')}")
        
    except Exception as e:
        print(f"❌ Error reading MCP config: {e}")

def test_mcp_client():
    """Test the MCP client functionality"""
    print("\n🧪 Testing MCP Client...")
    print("=" * 40)
    
    try:
        # Import and test the MCP client
        from mcp_weather_client import mcp_client
        
        # Test basic functionality
        test_cities = ['New York', 'London', 'Tokyo']
        
        import asyncio
        
        async def test_cities():
            print("🔌 Connecting to MCP servers...")
            await mcp_client.connect_to_servers()
            
            for city in test_cities:
                try:
                    print(f"🌤️  Testing weather data for {city}...")
                    weather_data = await mcp_client.get_weather_data(city)
                    
                    if weather_data:
                        current = weather_data.get('current', {})
                        temp = current.get('Temperature', {}).get('Metric', {}).get('Value', 'N/A')
                        condition = current.get('WeatherText', 'N/A')
                        print(f"    ✅ {city}: {temp}°C, {condition}")
                    else:
                        print(f"    ❌ No data for {city}")
                        
                except Exception as e:
                    print(f"    ❌ Error testing {city}: {e}")
            
            print("✅ MCP client test completed!")
        
        # Run the async test
        asyncio.run(test_cities())
        return True
        
    except Exception as e:
        print(f"❌ MCP client test failed: {e}")
        return False

def main():
    """Main startup function"""
    print_banner()
    
    # Change to the app directory
    app_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(app_dir)
    
    print(f"📁 Working directory: {app_dir}")
    print(f"🕐 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check dependencies
    print("🔍 Checking dependencies...")
    if not check_dependencies():
        print("❌ Dependency check failed. Please install missing packages.")
        return 1
    
    # Verify files
    print("\n🔍 Verifying project files...")
    if not verify_files():
        print("❌ File verification failed. Please ensure all files are present.")
        return 1
    
    # Show MCP configuration
    show_mcp_config()
    
    # Test MCP client
    if not test_mcp_client():
        print("⚠️  MCP client test failed, but continuing with fallback data...")
    
    print("\n🚀 Starting Weather Pro application...")
    print("=" * 60)
    print("🌐 Server will be available at: http://127.0.0.1:5000")
    print("📱 Mobile-friendly responsive design")
    print("🎨 Features modern glassmorphism UI")
    print("🔄 Real-time weather updates")
    print()
    print("💡 Tips:")
    print("   • Try searching for different cities")
    print("   • Toggle between light/dark themes")
    print("   • Each city shows unique weather patterns")
    print("   • Use the location button for current location")
    print()
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 60)
    
    try:
        # Start the Flask application
        import app
        print("✅ Weather Pro started successfully!")
        
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
        return 0
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())