# 🌤️ The Weather App by The PFG

A modern, interactive weather application built with Streamlit that provides real-time weather information and AI-powered local event recommendations based on current weather conditions.

## ✨ Features

### 🌡️ Weather Information
- **Real-time weather data** from Open-Meteo API
- **Automatic location detection** using Streamlit's geolocation module
- **Interactive map** showing your current location
- **Comprehensive weather details** including:
  - Temperature (Celsius/Fahrenheit)
  - Wind speed
  - Weather conditions with detailed descriptions
  - Current date and local time
- **5-Day Weather Forecast** powered by machine learning:
  - Regression analysis using historical weather data
  - Temperature predictions for the next 5 days
  - Weather condition forecasts with WMO codes
  - Seasonal pattern analysis for accurate predictions

### 🤖 AI-Powered Event Recommendations
- **Local event discovery** using SerpAPI
- **Weather-appropriate recommendations** powered by ChatGPT
- **Smart clothing suggestions** based on current weather conditions
- **Personalized event filtering** considering weather suitability

### 🎨 User Experience
- **Clean, modern interface** with Streamlit
- **Consistent styling** across current weather and forecast sections
- **Intuitive layout** with weather icons and clear information hierarchy
- **Responsive design** with sidebar navigation
- **Real-time updates** with caching for optimal performance
- **Error handling** with user-friendly messages

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- API keys for:
  - OpenAI (for AI recommendations)
  - SerpAPI (for local events)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
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
   Note: For Docker deployment, you'll need to set up secrets through your deployment platform.

3. **Access the app**
   Open `http://localhost:8501` in your browser

## ☁️ Streamlit Community Cloud Deployment

### Deploy to Streamlit Community Cloud

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Update for Streamlit Community Cloud deployment"
   git push origin main
   ```

2. **Deploy on Streamlit Community Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account
   - Click "New app" and select your repository
   - Choose the main branch and `app.py` as the main file

3. **Configure secrets in Streamlit Community Cloud**
   - In your app's settings, go to "Secrets"
   - Add the following secrets:
     ```toml
     SERPAPI_API_KEY = "your_serpapi_key_here"
     OPENAI_API_KEY = "your_openai_key_here"
     ```
   - Save the secrets

4. **Deploy and enjoy!**
   - Your app will be available at `https://your-app-name.streamlit.app`
   - Secrets are automatically loaded from the Streamlit secrets management system

### Important Notes for Streamlit Community Cloud
- ✅ **No `.env` file needed** - use Streamlit's built-in secrets management
- ✅ **Secrets are encrypted** and stored securely by Streamlit
- ✅ **Easy to update** secrets through the web interface
- ✅ **No environment variables** required in your code

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

## 🛠️ Technical Details

### Architecture
- **Frontend**: Streamlit web interface
- **Backend**: Python with caching for performance
- **APIs**: RESTful API integrations
- **AI**: OpenAI GPT-4o-mini for recommendations

### Key Components

- **Location Detection**: Streamlit's geolocation module with user provided fallback
- **Weather Data**: Real-time weather from Open-Meteo
- **Historical Data**: Past weather data for machine learning predictions
- **Machine Learning**: Linear regression models for weather forecasting
- **Event Discovery**: Local events via SerpAPI
- **AI Integration**: Weather-appropriate recommendations
- **Caching**: 5-10 minute TTL for optimal performance

### Performance Features
- **Data caching** to reduce API calls
- **Error handling** for robust user experience
- **Responsive design** for various screen sizes
- **Health checks** for Docker deployment

## 📱 Usage

1. **Launch the app** and click "🌐 Get Weather"
2. **Choose temperature unit** (°F or °C)
3. **View current weather** with date, time, and weather details
4. **See 5-day forecast** with machine learning predictions
5. **Switch to "Local Events"** for AI recommendations
6. **Get personalized suggestions** based on weather conditions

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
- Wind speed units (km/h, mph, m/s, knots)
- Caching duration (configurable TTL)
- Weather code descriptions (WMO codes)

## 🐛 Troubleshooting

### Common Issues

1. **Location not detected**
   - Check internet connection
   - Verify geolocation services are accessible

2. **API errors**
   - Verify API keys are correctly set
   - Check API quota and billing status

3. **No events found**
   - Ensure SerpAPI key is valid
   - Check if location has available events

### Error Messages
- Clear, user-friendly error messages
- Detailed logging for debugging
- Graceful fallbacks for API failures

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For support, please open an issue in the GitHub repository or contact the development team.

---

**Built with ❤️ using Streamlit, OpenAI, and modern web APIs**
