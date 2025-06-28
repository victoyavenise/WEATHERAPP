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
def get_user_location():
    try:
        response = requests.get("https://ipinfo.io/json")
        data = response.json()
        loc = data["loc"]
        lat, lon = map(float, loc.split(","))
        city = data["city"]
        region = data["region"]
        print(f"[DEBUG] Location detected: {city}, {region} | Lat: {lat}, Lon: {lon}")
        return lat, lon, city
    except Exception as e:
        print(f"[ERROR] Failed to get location: {e}")
        return 33.749, -84.388, "Atlanta"  # Fallback to Atlanta


# ------------------------------
# Fetch Weather from API
# ------------------------------
def fetch_weather_data():
    _, _, city = get_user_location()
    url = f"{BASE_URL}?key={API_KEY}&q={city}&days=5&aqi=no&alerts=no"
    print(f"[DEBUG] Requesting weather from: {url}")
    try:
        response = requests.get(url)
        data = response.json()
        if "current" in data:
            return data
        else:
            print(f"[ERROR] API response issue: {data}")
            return None
    except Exception as e:
        print(f"[ERROR] Failed to fetch weather data: {e}")
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

    # Hair tip logic
    if humidity <= 50:
        hair_tip = "You're good. Hair stays laid and holds its style with no issues."
    elif 50 < humidity <= 65:
        hair_tip = "Might get a lil frizzy or swell — especially if your hair drinks up moisture."
    elif 65 < humidity <= 75:
        hair_tip = "Uh oh. Hair’s starting to puff, wave, or lose its press. That’s reversion knocking."
    else:
        hair_tip = "Yeah… it’s a wrap. Curls and coils are back, press is gone."

    return {
        "date": dt,
        "temp": round(temp),
        "humidity": humidity,
        "description": description,
        "hair_tip": hair_tip
    }

# ------------------------------
# Export functions for import
# ------------------------------
__all__ = ["fetch_weather_data", "get_user_location", "parse_daily_weather"]

