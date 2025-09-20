import streamlit as st
import requests
from datetime import datetime
from openai import OpenAI
from streamlit_geolocation import streamlit_geolocation

@st.cache_data(ttl=600)
def reverse_geocode(lat: float, lon: float):
    """Return (resolved_name, country) using Nominatim reverse geocoding."""
    try:
        url = "https://nominatim.openstreetmap.org/reverse"
        params = {
            "lat": lat,
            "lon": lon,
            "format": "json",
            "addressdetails": 1
        }
        headers = {
            "User-Agent": "WeatherApp/1.0"
        }
        r = requests.get(url, params=params, headers=headers, timeout=10)
        r.raise_for_status()
        data = r.json()
        
        if data.get("address"):
            city = data["address"].get("city") or data["address"].get("town") or data["address"].get("village") or "Unknown Location"
            country = data["address"].get("country", "")
            return city, country
        return "Unknown Location", ""
    except Exception:
        return "Unknown Location", ""

@st.cache_data(ttl=600)
def geocode_location(location_text: str):
    """Convert location text to (lat, lon, city, country) using Nominatim geocoding."""
    try:
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": location_text,
            "format": "json",
            "addressdetails": 1,
            "limit": 1
        }
        headers = {
            "User-Agent": "WeatherApp/1.0"
        }
        r = requests.get(url, params=params, headers=headers, timeout=10)
        r.raise_for_status()
        data = r.json()
        
        if data and len(data) > 0:
            result = data[0]
            lat = float(result.get("lat", 0))
            lon = float(result.get("lon", 0))
            
            # Extract city and country from address details
            address = result.get("address", {})
            city = address.get("city") or address.get("town") or address.get("village") or location_text
            country = address.get("country", "")
            
            return lat, lon, city, country
        return None, None, "Unknown Location", ""
    except Exception:
        return None, None, "Unknown Location", ""

@st.cache_data(ttl=300)
def get_current_weather(lat: float, lon: float, temp_unit: str, wind_unit: str): # passing geocode_city returned values as keys
    """Return current weather dict from Open-Meteo."""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": "true",       # simplest current weather switch
        "temperature_unit": temp_unit,   # "celsius" or "fahrenheit"
        "windspeed_unit": wind_unit,     # "kmh", "ms", "mph", "kn"
        "timezone": "auto",
    }
    r = requests.get(url, params=params, timeout=10) # send request
    r.raise_for_status()
    return r.json().get("current_weather")

@st.cache_data(ttl=300)
def get_local_events(city_name):
    api_key = st.secrets.get("SERPAPI_API_KEY")
    if not api_key:
        st.error("SERPAPI_API_KEY not found in Streamlit secrets")
        return None
    
    params = {
        "api_key": api_key,
        "engine": "google_events",
        "q": f"Events in {city_name}",
        "hl": "en",
        "gl": "us",
        "htichips": "date:today"
    }

    try:
        response = requests.get("https://serpapi.com/search", params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error fetching events: {e}")
        return None

@st.cache_data(ttl=300)
def get_ai_events(weather_data, event_data):
    client = OpenAI(api_key=st.secrets.get("OPENAI_API_KEY"))

    # System prompt for weather-appropriate event recommendations
    system_prompt = """You are a helpful weather assistant that analyzes local events and current weather conditions to provide personalized recommendations.

    Your task is to:
    1. Review the available local events
    2. Consider the current weather conditions
    3. Recommend which events are most suitable for today's weather
    4. Provide specific clothing recommendations for each recommended event

    For clothing recommendations, consider:
    - If it's raining: suggest umbrellas, waterproof jackets, rain boots
    - If it's sunny and warm: suggest light clothing, sun hats, sunscreen
    - If it's cold: suggest warm jackets, layers, gloves, hats
    - If it's windy: suggest wind-resistant clothing, secure accessories
    - If it's snowing: suggest winter gear, boots, warm layers

    Provide 3-5 specific event recommendations with weather-appropriate clothing suggestions for each."""

    # Format event data for the AI
    events_text = "No events available"
    if event_data and 'events_results' in event_data:
        events_list = event_data['events_results'][:10]  # Limit to first 10 events
        events_text = "\n".join([
            f"- {event.get('title', 'Unknown Event')} at {event.get('address', 'Unknown Location')} on {event.get('date', 'Unknown Date')}"
            for event in events_list
        ])

    # Create user message with weather and event data
    user_message = f"""Based on the current weather and available local events, please provide recommendations on which events to attend and what to wear.

    Current Weather:
    - Temperature: {weather_data.get('temperature', 'N/A')}°F
    - Wind Speed: {weather_data.get('windspeed', 'N/A')} mph
    - Wind Direction: {weather_data.get('winddirection', 'N/A')}°
    - Weather Code: {weather_data.get('weathercode', 'N/A')}
    - Time: {weather_data.get('time', 'N/A')}

    Available Local Events:
    {events_text}

    Please recommend which events are best suited for today's weather and provide specific clothing recommendations for each recommended event. Include the location address for these events."""

    # Create a chat completion
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
    )

    return response.choices[0].message.content

def main():
    # dictionary that provides hard coded weather codes - can be used to modiify verbage
    WMO_CODES = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        56: "Freezing drizzle (light)",
        57: "Freezing drizzle (dense)",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        66: "Freezing rain (light)",
        67: "Freezing rain (heavy)",
        71: "Slight snowfall",
        73: "Moderate snowfall",
        75: "Heavy snowfall",
        77: "Snow grains",
        80: "Rain showers (slight)",
        81: "Rain showers (moderate)",
        82: "Rain showers (violent)",
        85: "Snow showers (slight)",
        86: "Snow showers (heavy)",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail",
    }

    # page setup - these components are being called from streamlit, theyre native
    st.set_page_config(page_title="The Weather App by The PFG", page_icon="🌤️", layout="wide")
    st.title("🌤️ The Weather App by The PFG")

    col1,col2 = st.columns([.05,1])
    with col1:
        # Call streamlit_geolocation once
        location = streamlit_geolocation()
    with col2:
        st.html("<b><i>**Click the icon to the left and allow location permissions**</b></i>")

    location_search_txt = st.text_input("Location Search", key="city_text_search")

    # Sidebar for view selection
    with st.sidebar:
        st.header("View Options")
        view_mode = st.radio(
            "Choose what to display:",
            ["Weather Info", "Local Events"],
            index=0,
            help="Toggle between weather information and AI-powered recommendations"
        )
        st.divider()

    # Initialize session state for location data
    if 'location_data' not in st.session_state:
        st.session_state.location_data = None

    # Location detection section
    col1, col2 = st.columns([1, 1])
    with col1:
        get_weather_btn = st.button("🌐 Get Weather", help="Detect your location and get current weather", type="primary")

    with col2:
        # Always show clear button
        if st.button("🗑️ Clear Location", help="Clear detected location"):
            st.session_state.location_data = None
            st.rerun()

    # Temperature unit settings
    st.write("")  # Add some spacing
    unit = st.radio("Temperature unit", ["°F", "°C"], index=0, horizontal=True)
    temp_unit = "celsius" if unit == "°C" else "fahrenheit"
    wind_unit = "kmh" if unit == "°C" else "mph"

    # Show location status
    if st.session_state.location_data and st.session_state.location_data.get('latitude') and st.session_state.location_data.get('latitude') is not None:
        st.success("✅ Location detected!")
    
    # Get weather when button is clicked
    if get_weather_btn:
        # Clear cache to ensure fresh API calls
        get_local_events.clear()
        
        # Check if user provided a location search text
        if location_search_txt and location_search_txt.strip():
            # Use the location search text
            lat, lon, city_name, country = geocode_location(location_search_txt.strip())
            
            if lat is not None and lon is not None:
                # Store location data with city name
                st.session_state.location_data = {
                    'latitude': lat,
                    'longitude': lon,
                    'city': city_name,
                    'country': country
                }
                st.success(f"✅ Location found: {city_name}{', ' + country if country else ''}")
            else:
                st.error(f"❌ Could not find location '{location_search_txt}'. Please try a different search term.")
        else:
            # Fall back to geolocation if no search text provided
            if location:            
                if location['latitude'] and location['longitude']:
                    lat = location['latitude']
                    lon = location['longitude']
                    
                    # Use reverse geocoding to get city and country
                    reverse_geocoded = reverse_geocode(lat, lon)
                    if reverse_geocoded:
                        city_name, country = reverse_geocoded
                    else:
                        city_name = "Current Location"
                        country = ""
                    
                    # Store location data with city name
                    st.session_state.location_data = {
                        'latitude': lat,
                        'longitude': lon,
                        'city': city_name,
                        'country': country
                    }
                    st.success(f"✅ Location detected: {city_name}{', ' + country if country else ''}")
                else:
                    st.error("❌ Location coordinates are null. Please try again.")
            else:
                st.error("❌ Could not access your location. Please ensure location permissions are enabled.")

    # Display weather data if location exists (even when temperature unit changes)
    if st.session_state.location_data and st.session_state.location_data.get('latitude') and st.session_state.location_data.get('latitude') is not None:
        try:
            # Use automatic location detection
            lat = st.session_state.location_data['latitude']
            lon = st.session_state.location_data['longitude']
            
            # Use location data directly
            resolved = st.session_state.location_data.get('city', 'Current Location')
            country = st.session_state.location_data.get('country', '')
            
            # Get weather data
            weather = get_current_weather(lat, lon, temp_unit, wind_unit)

            if not weather:
                st.error("Could not fetch current weather. Please try again.")
            else: # display returned data from api using string interpolation
                if view_mode == "Weather Info":
                    st.subheader(f"Current Weather — {resolved}{', ' + country if country else ''}")
                    
                    # Create two columns: map on left, weather info on right
                    map_col, weather_col = st.columns([1, 1])
                    
                    with map_col:
                        st.write("**Location Map**")
                        st.map(data=[{"lat": lat, "lon": lon}], zoom=8)
                    
                    with weather_col:
                        # weather api call - define variables first
                        code = int(weather.get("weathercode", -1))
                        desc = WMO_CODES.get(code, f"Code {code}")
                        ts = weather.get("time")
                        when = (
                            datetime.fromisoformat(ts).strftime("%b %d, %Y %I:%M %p")
                            if ts else "—"
                        )
                        st.write("**Weather Details**")
                        st.caption(f"{when} (local time)")
                        cols = st.columns(3)
                        cols[0].metric("Temperature", f"{weather['temperature']} {unit}")
                        cols[1].metric("Wind Speed", f"{weather['windspeed']} {('km/h' if unit=='°C' else 'mph')}")
                        cols[2].metric("Direction", f"{weather['winddirection']}°")

                        st.write(f"**Condition:** {desc}")
                
                elif view_mode == "Local Events":
                    st.subheader("Local Events (Powered by ChatGPT)")
                    
                    # Get local events for the current city
                    events = get_local_events(resolved)
                    if events and 'events_results' in events:
                        # Get AI recommendations based on weather and events
                        try:
                            ai_recommendations = get_ai_events(weather, events)
                            if ai_recommendations:
                                st.write(ai_recommendations)
                        except Exception as e:
                            st.error(f"Could not generate AI recommendations: {e}")
                    else:
                        st.write("No local events found for this location.")

        # handle http responses
        except requests.HTTPError as e:
            st.error(f"HTTP error: {e}")
        except requests.RequestException as e:
            st.error(f"Network error: {e}")
        except Exception as e:
            st.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()