# 🌤️ The Weather App by The PFG

A modern, interactive weather application built with Streamlit that provides real-time weather information and AI-powered local event recommendations based on current weather conditions.

## ✨ Features

### 🌡️ Weather Information
- **Real-time weather data** from Open-Meteo API
- **Automatic location detection** using IP geolocation
- **Interactive map** showing your current location
- **Comprehensive weather details** including:
  - Temperature (Celsius/Fahrenheit)
  - Wind speed and direction
  - Weather conditions with detailed descriptions
  - Timestamp of weather data

### 🤖 AI-Powered Event Recommendations
- **Local event discovery** using SerpAPI
- **Weather-appropriate recommendations** powered by ChatGPT
- **Smart clothing suggestions** based on current weather conditions
- **Personalized event filtering** considering weather suitability

### 🎨 User Experience
- **Clean, modern interface** with Streamlit
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

3. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   SERPAPI_API_KEY=your_serpapi_key_here
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
   docker run -p 8501:8501 \
     -e OPENAI_API_KEY=your_openai_api_key \
     -e SERPAPI_API_KEY=your_serpapi_key \
     weather-app
   ```

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

- **Open-Meteo**: Weather data and geocoding
- **IPify**: IP address detection
- **IPAPI**: IP-based geolocation
- **SerpAPI**: Local event discovery
- **OpenAI**: AI recommendations

## 🛠️ Technical Details

### Architecture
- **Frontend**: Streamlit web interface
- **Backend**: Python with caching for performance
- **APIs**: RESTful API integrations
- **AI**: OpenAI GPT-4o-mini for recommendations

### Key Components

- **Location Detection**: IP-based geolocation with fallback
- **Weather Data**: Real-time weather from Open-Meteo
- **Event Discovery**: Local events via SerpAPI
- **AI Integration**: Weather-appropriate recommendations
- **Caching**: 5-10 minute TTL for optimal performance

### Performance Features
- **Data caching** to reduce API calls
- **Error handling** for robust user experience
- **Responsive design** for various screen sizes
- **Health checks** for Docker deployment

## 📱 Usage

1. **Launch the app** and click "🌐 Use My Location"
2. **Choose temperature unit** (°F or °C)
3. **View weather information** with interactive map
4. **Switch to "Local Events"** for AI recommendations
5. **Get personalized suggestions** based on weather conditions

## 🔧 Configuration

### Environment Variables
```env
OPENAI_API_KEY=your_openai_api_key
SERPAPI_API_KEY=your_serpapi_key
```

### Customization Options
- Temperature units (Celsius/Fahrenheit)
- Wind speed units (km/h, mph, m/s, knots)
- Caching duration (configurable TTL)
- Weather code descriptions (WMO codes)

## 🐛 Troubleshooting

### Common Issues

1. **Location not detected**
   - Check internet connection
   - Verify IP geolocation services are accessible

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
