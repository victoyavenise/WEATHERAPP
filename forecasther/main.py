# main.py

import tkinter as tk
from config.weather_api_handler import (
    fetch_weather_data_by_location,
    parse_daily_weather,
    print_current_conditions
)


def main():
    # Fetch weather
    weather_data, city = fetch_weather_data_by_location()
    print(f"📍 City: {city}")

    if weather_data:
        print_current_conditions(weather_data)
        daily_forecast = parse_daily_weather(weather_data)
        # Uncomment the next line if you implemented CSV saving
        # save_to_csv(daily_forecast)
    else:
        print("⚠️ Weather fetch failed. Exiting app.")
        return

    # Launch simple GUI
    root = tk.Tk()
    root.title("ForecastHER")
    root.geometry("400x200")

    label = tk.Label(root, text="Welcome to ForecastHER!", font=("Helvetica", 16))
    label.pack(pady=10)

    city_label = tk.Label(root, text=f"📍 {city}", font=("Helvetica", 12))
    city_label.pack(pady=5)

    temp_label = tk.Label(
        root,
        text=f"🌡️ Temp: {daily_forecast['temp']}°F\n"
             f"💧 Humidity: {daily_forecast['humidity']}%\n"
             f"🌥️ {daily_forecast['description']}\n\n"
             f"💇🏽‍♀️ Hair Tip: {daily_forecast['hair_tip']}",
        wraplength=350,
        justify="left",
        font=("Helvetica", 11)
    )
    temp_label.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
