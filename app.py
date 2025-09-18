import streamlit as st
import requests
from datetime import datetime

@st.cache_data(ttl=600)
def geocode_city(name: str): # passing name as city query - we need this first to then call current weather with this informtion as key
    """Return (lat, lon, resolved_name, country) using Open-Meteo geocoding."""
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": name, "count": 1, "language": "en", "format": "json"}
    r = requests.get(url, params=params, timeout=10) # send request
    r.raise_for_status() # raise exceptio for error
    data = r.json()
    if not data.get("results"):
        return None
    top = data["results"][0]
    return ( # tuple that streamlit stores in cache
        top["latitude"],
        top["longitude"],
        top.get("name", name),
        top.get("country", ""),
    )

@st.cache_data(ttl=600)
def reverse_geocode(lat: float, lon: float):
    """Return (resolved_name, country) using Open-Meteo reverse geocoding."""
    url = "https://geocoding-api.open-meteo.com/v1/reverse"
    params = {"latitude": lat, "longitude": lon, "count": 1, "language": "en", "format": "json"}
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    data = r.json()
    if not data.get("results"):
        return None
    top = data["results"][0]
    return (
        top.get("name", "Unknown Location"),
        top.get("country", ""),
    )

@st.cache_data(ttl=600)
def get_ip_location():
    """Return (lat, lon, city, country) using IP-based geolocation as fallback."""
    try:
        # Get IP address
        ip_response = requests.get('https://api64.ipify.org?format=json', timeout=5)
        ip_data = ip_response.json()
        ip_address = ip_data['ip']
        
        # Get location from IP
        geo_response = requests.get(f'https://ipapi.co/{ip_address}/json/', timeout=5)
        geo_data = geo_response.json()
        
        if 'latitude' in geo_data and 'longitude' in geo_data:
            return (
                geo_data['latitude'],
                geo_data['longitude'],
                geo_data.get('city', 'Unknown'),
                geo_data.get('country_name', ''),
            )
    except Exception as e:
        st.write(f"IP geolocation failed: {e}")
    return None

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
    r.raise_for_status() # raise exceptio for error
    return r.json().get("current_weather")

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
    st.set_page_config(page_title="The Weather App", page_icon="SWA", layout="wide")
    st.title("The Weather App")

    # Initialize session state for location data
    if 'location_data' not in st.session_state:
        st.session_state.location_data = None

    # Location detection section
    col1, col2 = st.columns([1, 1])

    with col1:
        get_weather_btn = st.button("🌐 Get My Weather", help="Detect your location and get current weather", type="primary")

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
        # Get IP-based location
        ip_location = get_ip_location()
        if ip_location:
            lat, lon, city_name, country = ip_location
            st.session_state.location_data = {
                'latitude': lat,
                'longitude': lon,
                'city': city_name,
                'country': country
            }
            st.success(f"✅ Location detected: {city_name}, {country}")
        else:
            st.error("❌ Could not determine location from IP address")

    # Display weather data if location exists (even when temperature unit changes)
    if st.session_state.location_data and st.session_state.location_data.get('latitude') and st.session_state.location_data.get('latitude') is not None:
        try:
            # Use automatic location detection
            lat = st.session_state.location_data['latitude']
            lon = st.session_state.location_data['longitude']
            
            # Check if we have city/country from IP location
            if 'city' in st.session_state.location_data and 'country' in st.session_state.location_data:
                resolved = st.session_state.location_data['city']
                country = st.session_state.location_data['country']
            else:
                # Use reverse geocoding for GPS location
                reverse_geocoded = reverse_geocode(lat, lon)
                if reverse_geocoded:
                    resolved, country = reverse_geocoded
                else:
                    resolved = "Current Location"
                    country = ""
            
            # Get weather data
            weather = get_current_weather(lat, lon, temp_unit, wind_unit)

            if not weather:
                st.error("Could not fetch current weather. Please try again.")
            else: # display returned data from api using string interpolation
                st.subheader(f"Current Weather — {resolved}{', ' + country if country else ''}")
                cols = st.columns(3)
                cols[0].metric("Temperature", f"{weather['temperature']} {unit}")
                cols[1].metric("Wind Speed", f"{weather['windspeed']} {('km/h' if unit=='°C' else 'mph')}")
                cols[2].metric("Direction", f"{weather['winddirection']}°")

                # weather api call
                code = int(weather.get("weathercode", -1))
                desc = WMO_CODES.get(code, f"Code {code}")
                ts = weather.get("time")
                when = (
                    datetime.fromisoformat(ts).strftime("%b %d, %Y %I:%M %p")
                    if ts else "—"
                )

                st.write(f"**Condition:** {desc}")
                st.caption(f"Observed: {when} (local time)")
                st.map(data=[{"lat": lat, "lon": lon}], zoom=8)

        # handle http responses
        except requests.HTTPError as e:
            st.error(f"HTTP error: {e}")
        except requests.RequestException as e:
            st.error(f"Network error: {e}")
        except Exception as e:
            st.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()