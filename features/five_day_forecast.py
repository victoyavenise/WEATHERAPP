import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import urllib.request
import io
import os
import json

from config.weather_api_handler import fetch_weather_data


FAV_CITIES_FILE = os.path.join(os.path.dirname(__file__), "../data/fav_cities.json")

# Weather emoji icons
WEATHER_EMOJIS = {
    "sunny": "images/sun.png",
    "clear": "images/sun_cloud.png",
    "cloud": "images/cloudy.png",
    "rain": "images/cloud_rain.png",
    "snow": "images/snowy.png",
    "thunder": "images/thunder_storm.png",
    "fog": "images/cloudy.png",
    "overcast": "images/cloudy.png",
    "mist": "🌫️"
}

def get_weather_emoji_icon(condition):
    condition = condition.lower()
    for key in WEATHER_EMOJIS:
        if key in condition:
            return WEATHER_EMOJIS[key]
    return None

def get_hair_tip(humidity):
    if humidity <= 50:
        return "Hair stays laid. No issues."
    elif 50 < humidity <= 65:
        return "Might get a lil frizzy or swell."
    elif 65 < humidity <= 75:
        return "Hair’s starting to puff or wave."
    else:
        return "Yeah… it’s a wrap. Ya baby hairs will curl up in a fist and swing on you."


class FavoriteCitiesTab:
    def __init__(self, parent):
        self.parent = parent
        self.fav_city_data = []

        self.build_ui()
        self.load_fav_cities()

    def build_ui(self):
        ctk.CTkLabel(self.parent, text="Your Top 5 Cities", font=("Helvetica", 18, "bold"),
                     text_color="white").pack(pady=10)

        self.fav_entry = ctk.CTkEntry(self.parent, font=("Helvetica", 12), width=200, placeholder_text="Enter city name")
        self.fav_entry.pack(pady=5)

        ctk.CTkButton(self.parent, text="Add City", font=("Helvetica", 12, "bold"),
                      fg_color="white", text_color="purple", command=self.add_fav_city).pack(pady=(0, 4))

        ctk.CTkButton(self.parent, text="Clear All", font=("Helvetica", 12),
                      fg_color="#ffcccc", text_color="red", command=self.clear_all_cities).pack(pady=(0, 8))

        self.cards_container = ctk.CTkScrollableFrame(self.parent, width=500, height=250, fg_color="transparent")
        self.cards_container.pack(pady=10)

    def load_fav_cities(self):
        if os.path.exists(FAV_CITIES_FILE):
            with open(FAV_CITIES_FILE, "r") as f:
                self.fav_city_data = json.load(f)
                for city_data in self.fav_city_data:
                    self.create_city_card(city_data)

    def save_fav_cities(self):
        with open(FAV_CITIES_FILE, "w") as f:
            json.dump(self.fav_city_data, f)

    def add_fav_city(self):
        city = self.fav_entry.get().strip()

        if not city:
            messagebox.showwarning("Missing", "Please enter a city name.")
            return
        if not city.replace(" ", "").isalpha() or len(city) < 2:
            messagebox.showerror("Invalid", "Sorry sis, that’s not a real city. Drop ya lo and try again.")
            return
        if any(c["city"].lower() == city.lower() for c in self.fav_city_data):
            messagebox.showinfo("Duplicate", f"{city.title()} is already in your favorites.")
            return
        if len(self.fav_city_data) >= 5:
            messagebox.showwarning("Limit Reached", "You can only save 5 cities.")
            return

        try:
            data = fetch_weather_data(city)

            api_city = data["location"]["name"].lower()
            if api_city != city.lower():
                raise ValueError("City mismatch")

            temp = round(data["current"]["temp_f"])
            humidity = data["current"]["humidity"]
            icon_url = data["current"]["condition"]["icon"]
            hair_tip = get_hair_tip(humidity)

            new_city = {
                "city": api_city.upper(),
                "temp": temp,
                "humidity": humidity,
                "icon": icon_url,
                "hair_tip": hair_tip
            }

            self.fav_city_data.append(new_city)
            self.save_fav_cities()
            self.create_city_card(new_city)
            self.fav_entry.delete(0, "end")

        except Exception as e:
            print("[ERROR]", e)
            messagebox.showerror("City Not Found", "Sorry sis, that’s not a real city. Drop ya lo and try again.")

    def create_city_card(self, city_data):
        frame = ctk.CTkFrame(self.cards_container, fg_color="#b866e6", corner_radius=12)
        frame.pack(pady=6, padx=8, fill="x")

        header_frame = ctk.CTkFrame(frame, fg_color="#b866e6")
        header_frame.pack(fill="x", padx=8, pady=6)

        ctk.CTkLabel(header_frame, text=city_data["city"], font=("Helvetica", 16, "bold"), text_color="white").pack(side="left")

        try:
            icon_url = "http:" + city_data["icon"]
            raw_data = urllib.request.urlopen(icon_url).read()
            img = Image.open(io.BytesIO(raw_data)).resize((30, 30))
            icon = ImageTk.PhotoImage(img)

            icon_label = ctk.CTkLabel(header_frame, image=icon, text="", fg_color="#b866e6")
            icon_label.image = icon
            icon_label.pack(side="left", padx=8)
        except:
            pass

        ctk.CTkLabel(header_frame, text=f"{city_data['temp']}°F", font=("Helvetica", 16), text_color="white").pack(side="left")

        def delete_city():
            self.fav_city_data = [c for c in self.fav_city_data if c["city"] != city_data["city"]]
            self.save_fav_cities()
            frame.destroy()

        ctk.CTkButton(header_frame, text="🗑️", width=30, height=25, font=("Helvetica", 12),
                      fg_color="#b866e6", text_color="white", hover_color="#9933cc", command=delete_city).pack(side="right", padx=5)

        ctk.CTkLabel(frame, text=city_data["hair_tip"], font=("Helvetica", 10, "italic"),
                     text_color="white", wraplength=240, justify="left").pack(padx=10, pady=(0, 8))
    
    def clear_all_cities(self):
        if not self.fav_city_data:
            messagebox.showinfo("No Cities", "You don’t have any saved cities to clear.")
            return

        confirm = messagebox.askyesno("Clear All", "Are you sure you want to delete all your favorite cities?")
        if confirm:
            self.fav_city_data.clear()
            self.save_fav_cities()
            for widget in self.cards_container.winfo_children():
                widget.destroy()
