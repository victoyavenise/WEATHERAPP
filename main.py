from weather_api_handler import fetch_weather_data, parse_daily_weather, print_current_conditions
from weather_csv_saver import save_to_csv
from weekly_viewer_gui import WeatherAppGUI

import tkinter as tk

def main():
    # Step 1: Fetch Weather Data
    weather_data = fetch_weather_data()

    # Step 2: Show Current Humidity + Hair Tip in Terminal (optional)
    print_current_conditions(weather_data)

    # Step 3: Parse and Save Daily Forecast
    if weather_data:
        daily_forecast = parse_daily_weather(weather_data)
        save_to_csv(daily_forecast)
    else:
        print("⚠️ Skipping CSV save due to fetch error.")

    # Step 4: Launch the Weekly Viewer GUI
    root = tk.Tk()
    app = WeatherAppGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
