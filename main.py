import customtkinter as ctk
from PIL import Image
import os
from tkinter import messagebox
from config.weather_api_handler import fetch_weather_data, get_user_location, get_hair_tip
from features.favorite_cities_tab import FavoriteCitiesTab
from datetime import datetime

# App Settings
APP_WIDTH = 600
APP_HEIGHT = 550
MAIN_BG_COLOR = "#D4A0FB"  # Use relative path
LOGO_PATH = "./images/forecasther.png"  # Use relative path


# Weather emoji image paths
WEATHER_EMOJIS = {
    "sunny": "./images/sun.png",
    "clear": "./images/sun_cloud.png",
    "cloud": "./images/cloudy.png",
    "rain": "./images/cloud_rain.png",
    "snow": "./images/snowy.png",
    "thunder": "./images/thunder_storm.png",
    "fog": "./images/cloudy.png",
    "overcast": "./images/cloudy.png",
    "mist": "🌫️"
}

def get_weather_emoji_icon(condition_text):
    condition = condition_text.lower()
    for key in WEATHER_EMOJIS:
        if key in condition:
            return WEATHER_EMOJIS[key]
    return None  # fallback

class ForecastHerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ForecastHer")
        self.root.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
        self.root.resizable(False, False)

        self.root.configure(fg_color=MAIN_BG_COLOR) # Use fg_color for CTk
        self.create_top_navbar()

        # Create Tab View
        self.tabview = ctk.CTkTabview(self.root, width=APP_WIDTH - 20, height=APP_HEIGHT - 100, fg_color="transparent")
        self.tabview.place(relx=0.5, rely=0.52, anchor="center")

        self.home_tab = self.tabview.add("Home")
        self.favorites_tab = self.tabview.add("Favorites")

        self.home_tab.configure(fg_color="transparent")
        self.favorites_tab.configure(fg_color="transparent")

        self.build_home_tab(self.home_tab)
        self.build_favorites_tab(self.favorites_tab)

    


    def create_top_navbar(self):
        navbar = ctk.CTkFrame(self.root, fg_color="transparent")
        navbar.place(x=10, y=10)
        

        ctk.CTkButton(navbar, text="Home", command=lambda: self.tabview.set("Home"),
                      fg_color="white", text_color="black", hover_color="#ff02c0").pack(side="left", padx=5)
        ctk.CTkButton(navbar, text="Favorites", command=lambda: self.tabview.set("Favorites"),
                      fg_color="white", text_color="black", hover_color="#ff02c0").pack(side="left", padx=5)
        ctk.CTkButton(navbar, text="HairCast", command=lambda: print("HairCast"),
                      fg_color="white", text_color="black", hover_color="#ff02c0").pack(side="left", padx=5)

        if os.path.exists(LOGO_PATH):
            logo = Image.open(LOGO_PATH).resize((120, 120))
            logo_img = ctk.CTkImage(light_image=logo, size=(120, 120))
            logo_label = ctk.CTkLabel(self.root, image=logo_img, text="", fg_color="#d4a0fb")
            logo_label.image = logo_img
            logo_label.place(x=APP_WIDTH - 100, y=2)
            

    def build_home_tab(self, tab):
        title = ctk.CTkLabel(tab, text="forecastHer", font=("Helvetica", 26, "bold"),
                             text_color="white", fg_color="transparent")
        title.place(relx=0.5, y=30, anchor="center")

        subtitle = ctk.CTkLabel(tab, text="Weather Forecast for Her", font=("Helvetica", 16, "italic"),
                                text_color="white", fg_color="transparent")
        subtitle.place(relx=0.5, y=60, anchor="center")

        self.forecast_scroll = ctk.CTkScrollableFrame(tab, orientation="horizontal", width=APP_WIDTH - 60,
                                                      height=180, fg_color="transparent")
        self.forecast_scroll.place(relx=0.5, y=100, anchor="n")

        btn = ctk.CTkButton(tab, text="Find Your City", font=("Helvetica", 14, "bold"),
                            fg_color="#d94fe4", text_color="white", hover_color="#ff02c0",
                            command=self.find_city)
        btn.place(relx=0.5, y=350, anchor="center")

        self.load_forecast_by_location()

    def build_favorites_tab(self, tab):
        FavoriteCitiesTab(tab)

    def display_forecast_cards(self, forecast_days):
        for widget in self.forecast_scroll.winfo_children():
            widget.destroy()

        for day in forecast_days:
            card = ctk.CTkFrame(self.forecast_scroll, width=140, height=160, corner_radius=10, fg_color="#fff5fb")
            card.pack(side="left", padx=10, pady=10)

            # Convert date to weekday and month-day
            try:
                date_obj = datetime.strptime(day["date"], "%Y-%m-%d")
                weekday = date_obj.strftime("%A")  # e.g., Tuesday
                month_day = date_obj.strftime("%b %d").upper()  # e.g., JUL 29
            except Exception as e:
                weekday = day["date"]
                month_day = ""

            ctk.CTkLabel(card, text=weekday, font=("Helvetica", 12, "bold"), text_color="#4b0082").pack(pady=5)
            ctk.CTkLabel(card, text=month_day, font=("Helvetica", 10), text_color="#4b0082").pack(pady=5)
            ctk.CTkLabel(card, text=f'{round(day["temp"])}°F', font=("Helvetica", 12), text_color="#4b0082").pack()
            ctk.CTkLabel(card, text=f'Hi: {round(day["hi"])}° | Lo: {round(day["lo"])}°', font=("Helvetica", 10),  text_color="#4b0082").pack()

            emoji_path = get_weather_emoji_icon(day["condition"])
            if emoji_path and os.path.exists(emoji_path):
                icon_img = Image.open(emoji_path).resize((30, 30))
                icon_ctk_img = ctk.CTkImage(light_image=icon_img, size=(30, 30))  # Convert to CTkImage
                icon_label = ctk.CTkLabel(card, image=icon_ctk_img, text="", fg_color="#fff5fb")
                icon_label.image = icon_ctk_img  # Ensure the image reference is saved
                icon_label.pack(pady=2)
            else:
                ctk.CTkLabel(card, text="🌤️", font=("Helvetica", 20)).pack(pady=2)

            ctk.CTkLabel(card, text=day["hair_tip"], font=("Helvetica", 9), wraplength=120,
                         justify="center", text_color="#cc6699").pack(pady=5)

    def find_city(self):
        popup = ctk.CTkInputDialog(title="Search City", text="Enter your city:")
        city = popup.get_input()

        if not city or len(city.strip()) < 3:
            messagebox.showerror("Try Again", "Sis, that’s too short to be a real city. Drop your Lo and try again 💁🏽‍♀️")
            return

        try:
            data = fetch_weather_data(city)
            if not data or "location" not in data:
                messagebox.showerror("Error", "Sorry sis, that city couldn’t be found. Try again.")
                return

            forecast_list = []
            for day in data["forecast"]["forecastday"]:
                forecast_list.append({
                    "date": day["date"],
                    "temp": day["day"]["avgtemp_f"],
                    "hi": day["day"]["maxtemp_f"],
                    "lo": day["day"]["mintemp_f"],
                    "condition": day["day"]["condition"]["text"],
                    "icon": day["day"]["condition"]["icon"],
                    "hair_tip": get_hair_tip(day["day"]["avghumidity"])
                })

            self.display_forecast_cards(forecast_list)
        except Exception as e:
            messagebox.showerror("Oops!", f"Something went wrong: {e}")

    def load_forecast_by_location(self):
        try:
            lat, lon, city = get_user_location()
            data = fetch_weather_data(city)
            if not data:
                return

            forecast_list = []
            for day in data["forecast"]["forecastday"]:
                forecast_list.append({
                    "date": day["date"],
                    "temp": day["day"]["avgtemp_f"],
                    "hi": day["day"]["maxtemp_f"],
                    "lo": day["day"]["mintemp_f"],
                    "condition": day["day"]["condition"]["text"],
                    "icon": day["day"]["condition"]["icon"],
                    "hair_tip": get_hair_tip(day["day"]["avghumidity"])
                })

            self.display_forecast_cards(forecast_list)
        except Exception as e:
            print(f"[ERROR] Failed to auto-load forecast: {e}")

if __name__ == "__main__":
    ctk.set_appearance_mode("dark") 
    root = ctk.CTk()
    app = ForecastHerApp(root)
    root.mainloop()
