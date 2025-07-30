# -*- coding: utf-8 -*-
import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path

# Load the .env file from the main project directory
env_path = Path(__file__).resolve().parent.parent / ".env"
print(f"[DEBUG] Loading .env from: {env_path}")
load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("WEATHER_API_KEY")
print(f"[DEBUG] Loaded WEATHER_API_KEY: {API_KEY}")

BASE_URL = "https://api.weatherapi.com/v1/forecast.json"

# ------------------------------
# Location Detection via IP
# ------------------------------
from geopy.geocoders import Nominatim

def get_user_location():
    try:
        # Step 1: Get IP-based lat/lon
        response = requests.get("https://ipinfo.io/json")
        data = response.json()
        lat, lon = map(float, data["loc"].split(","))
        
        # Step 2: Use geopy to reverse-geocode into a city name
        geolocator = Nominatim(user_agent="forecasther-app")
        location = geolocator.reverse((lat, lon), language='en')

        if location and "address" in location.raw:
            city = location.raw["address"].get("city") or \
                   location.raw["address"].get("town") or \
                   location.raw["address"].get("state")
        else:
            city = data.get("city")  # fallback to IP city

        print(f"[DEBUG] GeoPy City Detected: {city} | Lat: {lat}, Lon: {lon}")
        return lat, lon, city or "Atlanta"
    except Exception as e:
        print(f"[ERROR] Failed to get location via geopy: {e}")
        return 33.749, -84.388, "Atlanta"



# ------------------------------
# Fetch Weather from API
# ------------------------------
def fetch_weather_data(city_name):
    import requests
    import os
    from dotenv import load_dotenv

    load_dotenv()
    API_KEY = os.getenv("WEATHER_API_KEY")

    url = f"https://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city_name}&days=5&aqi=no&alerts=no"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None



# ------------------------------
# Parse & Format Daily Weather
# ------------------------------
def parse_daily_weather(data):
    current = data["current"]
    forecast = data["forecast"]["forecastday"][0]["day"]
    dt = data["location"]["localtime"].split(" ")[0]
    temp = current["temp_f"]
    humidity = current["humidity"]
    description = current["condition"]["text"]
    
    hair_tip = get_hair_tip(humidity)
 
    return {
        "date": dt,
        "temp": round(temp),
        "humidity": humidity,
        "description": description,
        "hair_tip": get_hair_tip
    }

# ------------------------------
# Hair Tip Function
# ------------------------------
def get_hair_tip(humidity):
    if humidity <= 50:
        return "You're good. Hair stays laid and holds its style with no issues."
    elif 51 <= humidity <= 65:
        return "Might get a lil frizzy or swell — especially if your hair drinks up moisture."
    elif 66 <= humidity <= 75:
        return "Uh oh. Hair’s starting to puff, wave, or lose its press."
    else:
        return "Yeah… it’s a wrap. Curls and coils are back, press is gone."


# ------------------------------
# Export functions for import
# ------------------------------
__all__ = ["fetch_weather_data", "get_user_location", "parse_daily_weather"]

