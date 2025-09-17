import streamlit as st
import requests
from datetime import datetime

# page setup - these components are being called from streamlit, theyre native
st.set_page_config(page_title="Weather App (MVP)", page_icon="SWA", layout="centered")
st.title("Simple Weather App")

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

# cache to avoid constant calls on streamlit refresh - ttl set @ 10min
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

# cache to avoid constant calls on streamlit refresh - ttl set @ 5min
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

def describe_wmo(code: int) -> str:
    return WMO_CODES.get(code, f"Code {code}")

# sidebar for farenheit and celsius option, styling
with st.sidebar:
    st.header("Settings")
    unit = st.radio("Temperature unit", ["°C", "°F"], index=0, horizontal=True)
    temp_unit = "celsius" if unit == "°C" else "fahrenheit"
    wind_unit = "kmh" if unit == "°C" else "mph"

# input handling and search action
city = st.text_input("Enter a city", placeholder="e.g. Miami, New York, London")
search = st.button("Get Weather")

# validates input from user
if search and not city.strip():
    st.warning("Please enter a city name.")

# strip input and try, if else for validations, if true, return values from api call
if city.strip():
    try:
        geocoded = geocode_city(city.strip())
        if not geocoded:
            st.error("City not found. Try a different name.")
        else:
            lat, lon, resolved, country = geocoded
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
                desc = describe_wmo(code)
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
