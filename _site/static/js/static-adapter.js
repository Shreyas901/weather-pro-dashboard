// Modified app.js for static deployment
const API_BASE = window.location.origin;

// Override the original functions to work with static JSON files
window.originalFetch = window.fetch;

// Custom fetch for static files
async function staticFetch(url) {
    try {
        if (url.includes('/api/weather/')) {
            const city = url.split('/api/weather/')[1].toLowerCase().replace(/\s+/g, '-');
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