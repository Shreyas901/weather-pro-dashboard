# Weather Pro Dashboard with MCP Server Integration

A stunning, modern weather application built with Flask backend and vanilla JavaScript frontend, featuring real-time weather data from AccuWeather API.

![Weather Pro Dashboard](https://img.shields.io/badge/Weather-Pro-blue?style=for-the-badge)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)

## ✨ Features

### 🌤️ Weather Information
- **Current Weather Conditions** - Temperature, humidity, wind speed, pressure, UV index, and more
- **5-Day Forecast** - Detailed daily weather predictions
- **Hourly Forecast** - 12-hour detailed hourly predictions
- **Weather Insights** - Sunrise/sunset times, temperature trends, wind details

### 🎨 Modern UI/UX
- **Glassmorphism Design** - Beautiful glass-like interface with backdrop blur effects
- **Responsive Layout** - Perfect on desktop, tablet, and mobile devices
- **Dark/Light Theme** - Toggle between light and dark modes
- **Smooth Animations** - Floating elements, transitions, and micro-interactions
- **Interactive Elements** - Hover effects, smooth scrolling, and dynamic content

### 🔍 Smart Search
- **City Search** - Search for any city worldwide with autocomplete
- **Real-time Suggestions** - Get instant city suggestions as you type
- **Location Detection** - Use your current location for weather data

### 🌈 Visual Effects
- **Weather Icons** - Dynamic icons based on current weather conditions
- **Color Gradients** - Weather-themed color schemes
- **Background Effects** - Animated weather effects (rain, snow) [Optional feature]

## 🚀 Installation & Setup

### Prerequisites
- Python 3.7 or higher
- Git (optional, for cloning)
- A modern web browser

### Step 1: Download/Clone the Project
```bash
# Navigate to the project directory
cd WeatherReportAPP
```

### Step 2: Install Python Dependencies
```bash
# Install required packages
pip install -r requirements.txt

# Or install manually:
pip install Flask==2.3.3 requests==2.31.0
```

### Step 3: Run the Application
```bash
# Start the Flask server
python app.py

# Or if using Python 3 specifically:
python3 app.py
```

### Step 4: Access the Application
1. Open your web browser
2. Navigate to: `http://localhost:5000`
3. Start exploring the weather dashboard!

## 🔧 Configuration

### AccuWeather API Key
The application uses the AccuWeather API with the provided key: `ce65dcc921b44783b48105519251110`

If you need to change the API key:
1. Open `app.py`
2. Find the line: `API_KEY = "ce65dcc921b44783b48105519251110"`
3. Replace with your API key

### Customization Options
- **Default City**: Change the default city in `static/js/app.js` (line 4)
- **Theme**: The app remembers your theme preference in localStorage
- **API Endpoints**: Modify API URLs in `app.py` if needed

## 📁 Project Structure

```
WeatherReportAPP/
├── app.py                 # Flask backend application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/
│   └── index.html        # Main HTML template
└── static/
    ├── css/
    │   └── style.css     # Comprehensive CSS styles
    ├── js/
    │   └── app.js        # JavaScript application logic
    └── images/           # Static images (if any)
```

## 🎯 API Endpoints

### Backend Routes
- `GET /` - Main weather dashboard page
- `GET /api/weather/<city>` - Get complete weather data for a city
- `GET /api/search/<query>` - Search for cities

### Frontend Features
- City search with autocomplete
- Real-time weather data updates
- Responsive design for all devices
- Dark/light theme toggle
- Error handling and retry mechanisms

## 🎨 Design Features

### Color Scheme
- **Primary**: Blue gradient (`#2563eb` to `#3b82f6`)
- **Secondary**: Cyan accent (`#06b6d4`)
- **Background**: Gradient overlay with glassmorphism
- **Text**: High contrast with proper hierarchy

### Typography
- **Font**: Inter (Google Fonts)
- **Weights**: 300 (Light), 400 (Regular), 500 (Medium), 600 (Semibold), 700 (Bold)

### Layout
- **Grid-based** responsive design
- **Flexbox** for component alignment
- **CSS Grid** for complex layouts
- **Mobile-first** approach

## 🔍 Weather Data

### Current Weather
- Temperature (Celsius/Fahrenheit)
- Feels like temperature
- Humidity percentage
- Wind speed and direction
- Atmospheric pressure
- UV index
- Visibility
- Precipitation

### Forecasts
- **5-Day Forecast**: Daily high/low temperatures, conditions, precipitation probability
- **Hourly Forecast**: 12-hour detailed predictions

### Additional Data
- Sunrise and sunset times
- Wind gusts
- Temperature trends throughout the day

## 🌐 Browser Support
- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## 📱 Mobile Support
- Responsive design for all screen sizes
- Touch-friendly interface
- Optimized performance on mobile devices
- Progressive Web App features ready

## 🚀 Performance Features
- **Lazy Loading**: Efficient data loading
- **Caching**: Browser caching for static assets
- **Debounced Search**: Optimized search functionality
- **Error Handling**: Graceful error recovery
- **Loading States**: Visual feedback during data fetching

## 🔧 Troubleshooting

### Common Issues

**Issue**: Application won't start
- **Solution**: Check if Python and pip are installed correctly
- **Solution**: Verify all dependencies are installed: `pip install -r requirements.txt`

**Issue**: No weather data showing
- **Solution**: Check internet connection
- **Solution**: Verify the AccuWeather API key is valid
- **Solution**: Try searching for a different city

**Issue**: Search not working
- **Solution**: Check browser console for JavaScript errors
- **Solution**: Clear browser cache and cookies

**Issue**: Styling looks broken
- **Solution**: Hard refresh the page (Ctrl+F5 or Cmd+Shift+R)
- **Solution**: Check if CSS files are loading properly

### Development Mode
For development with auto-reload:
```bash
# Set Flask environment (Windows PowerShell)
$env:FLASK_ENV="development"

# Run with debug mode
python app.py
```

## 📄 License
This project is open source and available under the MIT License.

## 🤝 Contributing
Feel free to fork this project and submit pull requests for improvements!

## 📞 Support
If you encounter any issues or have questions, please check the troubleshooting section.

---

**Enjoy your Weather Pro dashboard!** 🌟

*Built with ❤️ using Flask, JavaScript, HTML5, and CSS3*
