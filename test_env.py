import os
from dotenv import load_dotenv

env_path = "/Users/beeexpressdesigns/FORECASTHER_MAIN.PY/forecasther/.env"
print(f"[DEBUG] Loading .env from: {env_path}")

load_dotenv(dotenv_path=env_path)

api_key = os.getenv("WEATHER_API_KEY")
print(f"[DEBUG] Loaded WEATHER_API_KEY: {api_key}")

