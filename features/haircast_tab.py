
import customtkinter as ctk
from tkinter import messagebox
from config.weather_api_handler import fetch_weather_data, get_hair_tip


class HairCastTab:
    def __init__(self, tab):
        self.tab = tab
        self.build_haircast_tab()

    def build_haircast_tab(self):
        # Add input button for city search and weather details
        self.haircast_city_input = ctk.CTkEntry(self.tab, placeholder_text="Enter your city", width=200)
        self.haircast_city_input.place(relx=0.5, y=20, anchor="center")

        self.haircast_btn = ctk.CTkButton(self.tab, text="Get Weather", command=self.get_haircast_data, fg_color="#D94FE4",
                                          text_color="white", hover_color="#FF02C0")
        self.haircast_btn.place(relx=0.5, y=60, anchor="center")

        self.haircast_result_label = ctk.CTkLabel(self.tab, text="", font=("Helvetica", 14), text_color="black")
        self.haircast_result_label.place(relx=0.5, y=120, anchor="center")

    def get_haircast_data(self):
        city = self.haircast_city_input.get()
        if len(city.strip()) < 3:
            messagebox.showerror("Input Error", "Please enter a valid city name.")
            return
        
        data = fetch_weather_data(city)
        if not data:
            messagebox.showerror("Error", "Could not fetch weather data for the city.")
            return
        
        # Extract data
        day_data = data["forecast"]["forecastday"][0]
        temp = round(day_data["day"]["avgtemp_f"])
        high = round(day_data["day"]["maxtemp_f"])
        low = round(day_data["day"]["mintemp_f"])
        humidity = day_data["day"]["avghumidity"]
        hair_tip = get_hair_tip(humidity)
        
        # Update result label
        result_text = f"City: {city}\nTemp: {temp}°F\nHigh: {high}°F | Low: {low}°F\nHumidity: {humidity}%\nHair Tip: {hair_tip}"
        self.haircast_result_label.configure(text=result_text)
