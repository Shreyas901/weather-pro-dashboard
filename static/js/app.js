// Weather Dashboard JavaScript
class WeatherApp {
    constructor() {
        this.currentCity = 'New York';
        this.isLoading = false;
        this.searchTimeout = null;
        
        this.initializeEventListeners();
        this.loadInitialWeather();
        this.initializeTheme();
    }

    initializeEventListeners() {
        // Search functionality
        const searchInput = document.getElementById('citySearch');
        const searchResults = document.getElementById('searchResults');
        
        searchInput.addEventListener('input', (e) => {
            clearTimeout(this.searchTimeout);
            const query = e.target.value.trim();
            
            if (query.length > 2) {
                this.searchTimeout = setTimeout(() => {
                    this.searchCities(query);
                }, 300);
            } else {
                searchResults.style.display = 'none';
            }
        });

        // Hide search results when clicking outside
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.search-container')) {
                searchResults.style.display = 'none';
            }
        });

        // Location button
        const locationBtn = document.getElementById('locationBtn');
        locationBtn.addEventListener('click', () => {
            this.getCurrentLocation();
        });

        // Theme toggle
        const themeToggle = document.getElementById('themeToggle');
        themeToggle.addEventListener('click', () => {
            this.toggleTheme();
        });

        // Retry button
        const retryBtn = document.getElementById('retryBtn');
        retryBtn.addEventListener('click', () => {
            this.hideError();
            this.loadWeatherData(this.currentCity);
        });

        // Handle Enter key in search
        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                const query = e.target.value.trim();
                if (query) {
                    this.loadWeatherData(query);
                    searchResults.style.display = 'none';
                }
            }
        });
    }

    async searchCities(query) {
        try {
            const response = await fetch(`/api/search/${encodeURIComponent(query)}`);
            const data = await response.json();
            
            if (data.cities && data.cities.length > 0) {
                this.displaySearchResults(data.cities);
            } else {
                document.getElementById('searchResults').style.display = 'none';
            }
        } catch (error) {
            console.error('Search error:', error);
            document.getElementById('searchResults').style.display = 'none';
        }
    }

    displaySearchResults(cities) {
        const searchResults = document.getElementById('searchResults');
        searchResults.innerHTML = '';
        
        cities.forEach(city => {
            const item = document.createElement('div');
            item.className = 'search-result-item';
            item.innerHTML = `
                <i class="fas fa-map-marker-alt"></i>
                <div>
                    <div class="result-name">${city.name}</div>
                    <div class="result-details">${city.region ? city.region + ', ' : ''}${city.country}</div>
                </div>
            `;
            
            item.addEventListener('click', () => {
                this.selectCity(city.name, city.country);
                searchResults.style.display = 'none';
            });
            
            searchResults.appendChild(item);
        });
        
        searchResults.style.display = 'block';
    }

    selectCity(cityName, countryName) {
        document.getElementById('citySearch').value = `${cityName}, ${countryName}`;
        this.loadWeatherData(cityName);
    }

    async getCurrentLocation() {
        if (!navigator.geolocation) {
            this.showError('Geolocation is not supported by this browser.');
            return;
        }

        const locationBtn = document.getElementById('locationBtn');
        const originalIcon = locationBtn.innerHTML;
        locationBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';

        navigator.geolocation.getCurrentPosition(
            async (position) => {
                try {
                    const { latitude, longitude } = position.coords;
                    // For demo purposes, we'll use a default city as AccuWeather API requires specific location key handling
                    locationBtn.innerHTML = originalIcon;
                    this.loadWeatherData('Current Location');
                } catch (error) {
                    locationBtn.innerHTML = originalIcon;
                    this.showError('Unable to get weather for your location.');
                }
            },
            (error) => {
                locationBtn.innerHTML = originalIcon;
                this.showError('Unable to access your location. Please search for a city.');
            }
        );
    }

    async loadInitialWeather() {
        // Load weather for default city
        await this.loadWeatherData(this.currentCity);
    }

    async loadWeatherData(city) {
        if (this.isLoading) return;
        
        this.isLoading = true;
        this.showLoading();
        this.hideError();
        
        try {
            const response = await fetch(`/api/weather/${encodeURIComponent(city)}`);
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || 'Weather data not available');
            }
            
            this.currentCity = city;
            this.displayWeatherData(data);
            this.hideLoading();
            
        } catch (error) {
            console.error('Weather data error:', error);
            this.hideLoading();
            this.showError(error.message || 'Unable to load weather data. Please try again.');
        } finally {
            this.isLoading = false;
        }
    }

    displayWeatherData(data) {
        // Update location information
        document.getElementById('cityName').textContent = data.location.city;
        document.getElementById('countryName').textContent = data.location.country;
        document.getElementById('lastUpdated').textContent = 
            `Last updated: ${new Date(data.current.LocalObservationDateTime).toLocaleTimeString()}`;

        // Update current weather
        const current = data.current;
        document.getElementById('currentTemp').textContent = Math.round(current.Temperature.Metric.Value);
        document.getElementById('feelsLike').textContent = `${Math.round(current.RealFeelTemperature.Metric.Value)}°C`;
        
        // Update weather details
        document.getElementById('visibility').textContent = `${current.Visibility.Metric.Value} ${current.Visibility.Metric.Unit}`;
        document.getElementById('humidity').textContent = `${current.RelativeHumidity}%`;
        document.getElementById('windSpeed').textContent = `${Math.round(current.Wind.Speed.Metric.Value)} ${current.Wind.Speed.Metric.Unit}`;
        document.getElementById('pressure').textContent = `${Math.round(current.Pressure.Metric.Value)} ${current.Pressure.Metric.Unit}`;
        document.getElementById('uvIndex').textContent = current.UVIndex || 'N/A';
        document.getElementById('precipitation').textContent = `${current.PrecipitationSummary.Precipitation.Metric.Value} ${current.PrecipitationSummary.Precipitation.Metric.Unit}`;

        // Update weather icon and background
        this.updateWeatherIcon(current.WeatherIcon, current.WeatherText);
        
        // Update wind direction
        if (current.Wind.Direction.Degrees) {
            const windDirection = document.getElementById('windDirection');
            windDirection.style.transform = `rotate(${current.Wind.Direction.Degrees}deg)`;
            document.getElementById('windDir').textContent = current.Wind.Direction.Localized || 'N/A';
        }
        
        document.getElementById('windGusts').textContent = current.WindGust ? 
            `${Math.round(current.WindGust.Speed.Metric.Value)} ${current.WindGust.Speed.Metric.Unit}` : 'N/A';

        // Update hourly forecast
        if (data.hourly_forecast) {
            this.displayHourlyForecast(data.hourly_forecast);
        }

        // Update 5-day forecast
        if (data.forecast_5day && data.forecast_5day.DailyForecasts) {
            this.displayDailyForecast(data.forecast_5day.DailyForecasts);
        }

        // Update sunrise/sunset if available
        if (data.forecast_5day && data.forecast_5day.DailyForecasts[0]) {
            const today = data.forecast_5day.DailyForecasts[0];
            if (today.Sun) {
                document.getElementById('sunrise').textContent = new Date(today.Sun.Rise).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
                document.getElementById('sunset').textContent = new Date(today.Sun.Set).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
            }
        }

        // Add fade-in animation
        document.getElementById('mainContent').classList.add('fade-in');
    }

    updateWeatherIcon(iconCode, weatherText) {
        const weatherIcon = document.getElementById('weatherIcon');
        let iconClass = 'fas fa-sun';
        let gradient = 'var(--gradient-sunny)';

        // Map weather icons based on AccuWeather icon codes
        if (iconCode >= 1 && iconCode <= 5) {
            // Sunny/Mostly Sunny
            iconClass = 'fas fa-sun';
            gradient = 'var(--gradient-sunny)';
        } else if (iconCode >= 6 && iconCode <= 11) {
            // Partly Cloudy/Cloudy
            iconClass = 'fas fa-cloud-sun';
            gradient = 'var(--gradient-cloudy)';
        } else if (iconCode >= 12 && iconCode <= 18) {
            // Rain
            iconClass = 'fas fa-cloud-rain';
            gradient = 'var(--gradient-rainy)';
        } else if (iconCode >= 19 && iconCode <= 29) {
            // Snow/Ice
            iconClass = 'fas fa-snowflake';
            gradient = 'var(--gradient-cloudy)';
        } else if (iconCode >= 30 && iconCode <= 32) {
            // Hot
            iconClass = 'fas fa-temperature-high';
            gradient = 'var(--gradient-sunny)';
        } else if (iconCode >= 33 && iconCode <= 44) {
            // Night conditions
            iconClass = 'fas fa-moon';
            gradient = 'var(--gradient-primary)';
        }

        weatherIcon.innerHTML = `<i class="${iconClass}"></i>`;
        weatherIcon.style.background = gradient;
    }

    displayHourlyForecast(hourlyData) {
        const container = document.getElementById('hourlyForecast');
        container.innerHTML = '';

        hourlyData.slice(0, 12).forEach(hour => {
            const hourElement = document.createElement('div');
            hourElement.className = 'hourly-item';
            
            const time = new Date(hour.DateTime).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
            const temp = Math.round(hour.Temperature.Value);
            const iconClass = this.getWeatherIconClass(hour.WeatherIcon);
            const precipitation = hour.PrecipitationProbability || 0;

            hourElement.innerHTML = `
                <div class="hourly-time">${time}</div>
                <div class="hourly-icon"><i class="${iconClass}"></i></div>
                <div class="hourly-temp">${temp}°C</div>
                <div class="hourly-precipitation">${precipitation}%</div>
            `;

            container.appendChild(hourElement);
        });
    }

    displayDailyForecast(dailyData) {
        const container = document.getElementById('dailyForecast');
        container.innerHTML = '';

        dailyData.forEach((day, index) => {
            const dayElement = document.createElement('div');
            dayElement.className = 'daily-item';
            
            const date = index === 0 ? 'Today' : new Date(day.Date).toLocaleDateString([], {weekday: 'short', month: 'short', day: 'numeric'});
            const iconClass = this.getWeatherIconClass(day.Day.Icon);
            const highTemp = Math.round(day.Temperature.Maximum.Value);
            const lowTemp = Math.round(day.Temperature.Minimum.Value);
            const precipitation = day.Day.PrecipitationProbability || 0;

            dayElement.innerHTML = `
                <div class="daily-date">${date}</div>
                <div class="daily-icon"><i class="${iconClass}"></i></div>
                <div class="daily-desc">${day.Day.IconPhrase}</div>
                <div class="daily-temps">
                    <span class="temp-high">${highTemp}°</span>
                    <span class="temp-low">${lowTemp}°</span>
                </div>
                <div class="daily-precip">${precipitation}%</div>
            `;

            container.appendChild(dayElement);
        });
    }

    getWeatherIconClass(iconCode) {
        if (iconCode >= 1 && iconCode <= 5) return 'fas fa-sun';
        if (iconCode >= 6 && iconCode <= 11) return 'fas fa-cloud-sun';
        if (iconCode >= 12 && iconCode <= 18) return 'fas fa-cloud-rain';
        if (iconCode >= 19 && iconCode <= 29) return 'fas fa-snowflake';
        if (iconCode >= 30 && iconCode <= 32) return 'fas fa-temperature-high';
        if (iconCode >= 33 && iconCode <= 44) return 'fas fa-moon';
        return 'fas fa-cloud';
    }

    showLoading() {
        document.getElementById('loadingScreen').classList.remove('hidden');
        document.getElementById('mainContent').style.opacity = '0.5';
    }

    hideLoading() {
        document.getElementById('loadingScreen').classList.add('hidden');
        document.getElementById('mainContent').style.opacity = '1';
    }

    showError(message) {
        document.getElementById('errorText').textContent = message;
        document.getElementById('errorMessage').classList.add('show');
    }

    hideError() {
        document.getElementById('errorMessage').classList.remove('show');
    }

    initializeTheme() {
        const savedTheme = localStorage.getItem('weather-app-theme') || 'light';
        this.setTheme(savedTheme);
    }

    toggleTheme() {
        const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        this.setTheme(newTheme);
    }

    setTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('weather-app-theme', theme);
        
        const themeToggle = document.getElementById('themeToggle');
        const icon = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
        themeToggle.innerHTML = `<i class="${icon}"></i>`;
    }
}

// Weather background effects
class WeatherEffects {
    constructor() {
        this.canvas = null;
        this.ctx = null;
        this.particles = [];
        this.initCanvas();
    }

    initCanvas() {
        this.canvas = document.createElement('canvas');
        this.canvas.id = 'weather-canvas';
        this.canvas.style.position = 'fixed';
        this.canvas.style.top = '0';
        this.canvas.style.left = '0';
        this.canvas.style.width = '100%';
        this.canvas.style.height = '100%';
        this.canvas.style.pointerEvents = 'none';
        this.canvas.style.zIndex = '1';
        this.canvas.style.opacity = '0.6';
        
        document.body.appendChild(this.canvas);
        this.ctx = this.canvas.getContext('2d');
        this.resizeCanvas();
        
        window.addEventListener('resize', () => this.resizeCanvas());
    }

    resizeCanvas() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }

    createRainEffect() {
        this.particles = [];
        for (let i = 0; i < 150; i++) {
            this.particles.push({
                x: Math.random() * this.canvas.width,
                y: Math.random() * this.canvas.height,
                length: Math.random() * 20 + 10,
                speed: Math.random() * 5 + 5,
                opacity: Math.random() * 0.5 + 0.2
            });
        }
        this.animateRain();
    }

    animateRain() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.ctx.strokeStyle = 'rgba(174, 194, 224, 0.6)';
        this.ctx.lineWidth = 2;
        this.ctx.lineCap = 'round';

        this.particles.forEach(particle => {
            this.ctx.globalAlpha = particle.opacity;
            this.ctx.beginPath();
            this.ctx.moveTo(particle.x, particle.y);
            this.ctx.lineTo(particle.x, particle.y + particle.length);
            this.ctx.stroke();

            particle.y += particle.speed;
            if (particle.y > this.canvas.height) {
                particle.y = -particle.length;
            }
        });

        requestAnimationFrame(() => this.animateRain());
    }

    createSnowEffect() {
        this.particles = [];
        for (let i = 0; i < 100; i++) {
            this.particles.push({
                x: Math.random() * this.canvas.width,
                y: Math.random() * this.canvas.height,
                radius: Math.random() * 4 + 1,
                speed: Math.random() * 2 + 1,
                opacity: Math.random() * 0.8 + 0.2,
                drift: Math.random() * 0.5 - 0.25
            });
        }
        this.animateSnow();
    }

    animateSnow() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';

        this.particles.forEach(particle => {
            this.ctx.globalAlpha = particle.opacity;
            this.ctx.beginPath();
            this.ctx.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
            this.ctx.fill();

            particle.y += particle.speed;
            particle.x += particle.drift;
            
            if (particle.y > this.canvas.height) {
                particle.y = -particle.radius;
            }
            if (particle.x > this.canvas.width) {
                particle.x = -particle.radius;
            } else if (particle.x < -particle.radius) {
                particle.x = this.canvas.width;
            }
        });

        requestAnimationFrame(() => this.animateSnow());
    }

    clear() {
        if (this.ctx) {
            this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        }
    }
}

// Initialize the weather app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.weatherApp = new WeatherApp();
    window.weatherEffects = new WeatherEffects();
    
    // Add some interactive elements
    const cards = document.querySelectorAll('.current-weather-card, .insight-card, .hourly-forecast-container, .daily-forecast-container');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
});

// Add some utility functions
const utils = {
    formatTime: (timestamp) => {
        return new Date(timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
    },
    
    formatDate: (timestamp) => {
        return new Date(timestamp).toLocaleDateString([], {weekday: 'short', month: 'short', day: 'numeric'});
    },
    
    getWindDirection: (degrees) => {
        const directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW'];
        return directions[Math.round(degrees / 22.5) % 16];
    },
    
    debounce: (func, wait) => {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
};