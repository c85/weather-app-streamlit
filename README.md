# 🌤️ The Weather App by The PFG

A modern, interactive weather application built with Streamlit that provides real-time weather information, advanced machine learning-powered forecasting, and AI-powered local event recommendations based on current weather conditions.

## ✨ Features

### 🌡️ Weather Information
- **Real-time weather data** from Open-Meteo API
- **Dual location detection**:
  - Automatic geolocation using Streamlit's geolocation module
  - Manual location search with text input and geocoding
- **Interactive map** showing your current location
- **Comprehensive weather details** including:
  - Temperature (Celsius/Fahrenheit) with unit conversion
  - Weather conditions with detailed WMO code descriptions
  - Current date and local time display
  - Wind speed with appropriate units (km/h or mph)
- **Advanced 5-Day Weather Forecast** powered by machine learning:
  - **WeatherHistoricalAnalyzer class** for sophisticated data processing
  - Historical weather data analysis (up to 1 year of data)
  - Linear regression models with feature engineering
  - Lagged features and rolling averages for improved accuracy
  - Temperature predictions for the next 5 days
  - Weather condition forecasts with meteorological logic
  - Seasonal pattern analysis and day-of-year matching
  - Realistic weather variation and randomness

### 🤖 AI-Powered Event Recommendations
- **Local event discovery** using SerpAPI
- **Weather-appropriate recommendations** powered by ChatGPT (GPT-4o-mini)
- **Smart clothing suggestions** based on current weather conditions
- **Personalized event filtering** considering weather suitability
- **Contextual recommendations** with specific location addresses

### 🎨 User Experience
- **Clean, modern interface** with Streamlit
- **Dual view modes**: Weather Info and Local Events
- **Consistent styling** across current weather and forecast sections
- **Intuitive layout** with weather icons and clear information hierarchy
- **Responsive design** with sidebar navigation
- **Real-time updates** with intelligent caching for optimal performance
- **Comprehensive error handling** with user-friendly messages
- **Session state management** for persistent user experience

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- API keys for:
  - OpenAI (for AI recommendations)
  - SerpAPI (for local events)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/c85/weather-app-streamlit/
   cd weather-app-streamlit
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up secrets for local development**
   Copy the example secrets file and add your API keys:
   ```bash
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   ```
   Then edit `.streamlit/secrets.toml` with your actual API keys:
   ```toml
   SERPAPI_API_KEY = "your_serpapi_key_here"
   OPENAI_API_KEY = "your_openai_key_here"
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:8501`

## 🐳 Docker Deployment

### Build and run with Docker

1. **Build the Docker image**
   ```bash
   docker build -t weather-app .
   ```

2. **Run the container**
   ```bash
   docker run -p 8501:8501 weather-app
   ```
   Note: For Docker deployment, you'll need to set up secrets through your deployment platform. The Dockerfile includes both `app.py` and `historical.py` files.

3. **Access the app**
   Open `http://localhost:8501` in your browser

## 📋 API Requirements

### Required API Keys

1. **OpenAI API Key**
   - Sign up at [OpenAI](https://platform.openai.com/)
   - Create an API key in your dashboard
   - Used for AI-powered event recommendations

2. **SerpAPI Key**
   - Sign up at [SerpAPI](https://serpapi.com/)
   - Get your API key from the dashboard
   - Used for fetching local events

### External APIs Used

- **Open-Meteo**: Weather data, geocoding, and historical weather data
- **SerpAPI**: Local event discovery
- **OpenAI**: AI recommendations
- **Nominatim**: Geocoding and reverse geocoding services

### Dependencies

#### Core Dependencies
- **streamlit**: Web application framework
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **scikit-learn**: Machine learning algorithms
- **requests**: HTTP library for API calls
- **openai**: OpenAI API client

#### Location Services
- **streamlit-geolocation**: Browser geolocation integration

#### Data Processing
- **python-dateutil**: Date/time utilities
- **pytz**: Timezone handling

## 📁 Project Structure

```
weather-app-streamlit/
├── app.py                 # Main Streamlit application
├── historical.py          # WeatherHistoricalAnalyzer class for ML forecasting
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
└── README.md             # Project documentation
```

### Key Files
- **`app.py`**: Main application with UI, location services, and weather display
- **`historical.py`**: Machine learning engine for weather forecasting
- **`requirements.txt`**: All necessary Python packages
- **`Dockerfile`**: Container configuration for deployment

## 🛠️ Technical Details

### Architecture
- **Frontend**: Streamlit web interface with responsive design
- **Backend**: Python with intelligent caching and session management
- **APIs**: RESTful API integrations with error handling
- **AI**: OpenAI GPT-4o-mini for intelligent recommendations
- **ML Engine**: Custom WeatherHistoricalAnalyzer class for forecasting

### Key Components

#### Location Services
- **Automatic Detection**: Streamlit's geolocation module
- **Manual Search**: Text-based location search with geocoding
- **Reverse Geocoding**: Nominatim API for location resolution
- **Fallback Handling**: Graceful degradation when location services fail

#### Weather Data Pipeline
- **Real-time Data**: Open-Meteo API for current weather
- **Historical Data**: Open-Meteo Archive API for ML training
- **Data Processing**: Pandas and NumPy for data manipulation
- **Feature Engineering**: Advanced meteorological feature creation

#### Machine Learning System (WeatherHistoricalAnalyzer)
- **Data Collection**: Fetches up to 1 year of historical weather data
- **Feature Engineering**: 
  - Time-based features (hour, day_of_year, month, day_of_week)
  - Lagged features (1h, 2h, 3h, 6h, 12h, 24h delays)
  - Rolling averages (6h, 12h, 24h windows)
  - Meteorological parameters (temperature, humidity, pressure, etc.)
- **Data Preprocessing**: MinMaxScaler for feature normalization
- **Model Training**: Linear regression with scikit-learn
- **Prediction Pipeline**: Multi-step forecasting with feature updates
- **Weather Logic**: Meteorological rules for weather condition determination

#### AI Integration
- **Event Discovery**: SerpAPI for local event data
- **Contextual Analysis**: Weather-aware event filtering
- **Recommendation Engine**: GPT-4o-mini for personalized suggestions
- **Clothing Advice**: Weather-appropriate attire recommendations

#### Caching Strategy
- **Historical Data**: 1-hour TTL for expensive API calls
- **Current Weather**: 5-minute TTL for real-time updates
- **Geocoding**: 10-minute TTL for location services
- **AI Responses**: 5-minute TTL for event recommendations
- **Streamlit Caching**: Optimized with proper parameter handling

### Performance Features
- **Intelligent Caching**: Multi-tier caching strategy for optimal performance
- **Error Handling**: Comprehensive error management with user feedback
- **Session Management**: Persistent state across user interactions
- **Responsive Design**: Adaptive layout for various screen sizes
- **Health Checks**: Docker health monitoring for deployment
- **Memory Management**: Efficient data handling for large datasets

## 📱 Usage

### Getting Started
1. **Launch the app** and choose your preferred temperature unit (°F or °C)
2. **Select location method**:
   - **Automatic**: Click "🌐 Get Weather" to use your device's location
   - **Manual**: Enter a city name or address in the "Location Search" field
3. **Allow location permissions** when prompted (for automatic detection)

### Weather Information
4. **View current weather** with comprehensive details:
   - Current temperature and weather conditions
   - Date and local time
   - Interactive map showing your location
5. **Explore 5-day forecast** powered by machine learning:
   - Temperature predictions for the next 5 days
   - Weather condition forecasts with meteorological accuracy
   - Seasonal pattern analysis for improved predictions

### AI-Powered Features
6. **Switch to "Local Events"** using the sidebar radio button
7. **Get AI recommendations** based on current weather:
   - Weather-appropriate event suggestions
   - Smart clothing recommendations
   - Personalized filtering based on conditions

### Advanced Features
8. **Clear location data** using the "🗑️ Clear Location" button
9. **Switch between view modes** using the sidebar
10. **Change temperature units** at any time (updates all displays)

## 🔧 Configuration

### Secrets Configuration

#### For Local Development
Create `.streamlit/secrets.toml`:
```toml
SERPAPI_API_KEY = "your_serpapi_key_here"
OPENAI_API_KEY = "your_openai_key_here"
```

#### For Streamlit Community Cloud
Add secrets through the web interface in your app settings.

### Customization Options
- Temperature units (Celsius/Fahrenheit)
- Caching duration (configurable TTL)
- Weather code descriptions (WMO codes)

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For support, please open an issue in the GitHub repository or contact the development team.

---

**Built with ❤️ using Streamlit, OpenAI, and modern web APIs**
