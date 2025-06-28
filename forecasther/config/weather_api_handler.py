# -*- coding: utf-8 -*-
import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path

# Load .env
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)
API_KEY = os.getenv("WEATHERAPI_KEY")
print(f"[DEBUG] Loaded WeatherAPI Key: {API_KEY}")

BASE_URL = "https://api.weatherapi.com/v1/forecast.json"

def get_user_location():
    try:
        response = requests.get("https://ipinfo.io/json")
        data = response.json()
        loc = data['loc']
        lat, lon = map(float, loc.split(','))
        city = data['city']
        region = data['region']
        print(f"[DEBUG] Location detected: {city}, {region} | Lat: {lat}, Lon: {lon}")
        return city
    except Exception as e:
        print(f"[ERROR] Failed to get location: {e}")
        return "Atlanta"

def fetch_weather_data_by_location():
    city = get_user_location()
    url = f"{BASE_URL}?key={API_KEY}&q={city}&days=1&aqi=no&alerts=no"
    print(f"[DEBUG] Requesting weather from: {url}")
    try:
        response = requests.get(url)
        data = response.json()
        if "current" in data:
            return data, city
        else:
            print(f"❌ API response error: {data}")
            return None, city
    except Exception as e:
        print(f"[ERROR] Failed to fetch weather: {e}")
        return None, city

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

def print_current_conditions(data):
    if not data:
        print("No weather data to display.")
        return

    humidity = data["current"]["humidity"]
    condition = data["current"]["condition"]["text"]
    temp = data["current"]["temp_f"]
    print(f"🌡️ Current Temp: {temp}°F")
    print(f"💧 Humidity: {humidity}%")
    print(f"🌥️ Condition: {condition}")
