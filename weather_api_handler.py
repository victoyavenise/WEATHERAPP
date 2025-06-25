import requests
from datetime import datetime

# Constants
LAT = 33.7490  # Atlanta
LON = -84.3880
API_KEY = "192b72f3ba96e73d23d50c1cbded1bab"
UNITS = "imperial"  # Fahrenheit, mph
EXCLUDE = "minutely,hourly,alerts"

# URL Constructor
url = (
    f"https://api.openweathermap.org/data/2.5/onecall"
    f"?lat={LAT}&lon={LON}&exclude={EXCLUDE}"
    f"&units={UNITS}&appid={API_KEY}"
)

# Humidity Hair Logic
def get_humidity_hair_alert(humidity):
    if humidity <= 50:
        return "You’re good. Hair stays laid and holds its style with no issues."
    elif 50 < humidity <= 65:
        return "Might get a lil frizzy or start swelling up — especially if your hair drinks up moisture (aka high porosity)."
    elif 65 < humidity <= 75:
        return "Uh oh. Hair’s starting to puff, wave up, or lose its press. That’s reversion knocking."
    else:
        return "Yeah… it’s a wrap. Curls and coils are back, press is gone, and your hair is out here doing its own thing."

# Fetch raw data
def fetch_weather_data():
    response = requests.get(url)
    if response.status_code == 200:
        print("✅ Success! Weather data loaded.")
        return response.json()
    else:
        print("❌ Error:", response.status_code)
        return None

# Parse daily forecast data
def parse_daily_weather(data):
    if not data:
        return []
    
    daily_data = []
    for day in data.get("daily", []):
        date = datetime.fromtimestamp(day["dt"]).strftime("%Y-%m-%d")
        temp = day["temp"]["day"]
        humidity = day["humidity"]
        description = day["weather"][0]["description"]
        hair_tip = get_humidity_hair_alert(humidity)
        daily_data.append({
            "date": date,
            "temp": temp,
            "humidity": humidity,
            "description": description,
            "hair_tip": hair_tip
        })
    return daily_data

# Optional: Show current humidity directly
def print_current_conditions(data):
    if data and "current" in data:
        humidity = data["current"].get("humidity")
        print(f"🌡️ Current humidity in Atlanta: {humidity}%")
        print(f"💇 Hair Tip: {get_humidity_hair_alert(humidity)}")

# Test run
if __name__ == "__main__":
    weather_data = fetch_weather_data()
    print_current_conditions(weather_data)
    daily_forecast = parse_daily_weather(weather_data)
    for day in daily_forecast:
        print(day)
