import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import urllib.request
import io
import json
import os

from config.weather_api_handler import fetch_weather_data

FAV_CITIES_FILE = os.path.join(os.path.dirname(__file__), "../data/fav_cities.json")


def get_hair_tip(humidity):
    if humidity <= 50:
        return "Hair stays laid. No issues."
    elif 50 < humidity <= 65:
        return "Might get a lil frizzy or swell."
    elif 65 < humidity <= 75:
        return "Hair’s starting to puff or wave."
    else:
        return "Yeah… it’s a wrap. Press is gone."


class FavoriteCitiesTab:
    def __init__(self, parent):
        self.parent = parent
        self.fav_city_data = []
        self.cards_container = None
        self.fav_entry = None

        self.build_ui()
        self.load_fav_cities()

    def build_ui(self):
        tk.Label(self.parent, text="Your Top 5 Cities", font=("Helvetica", 14, "bold"),
                 fg="white", bg="#d9a5ff").pack(pady=10)

        self.fav_entry = tk.Entry(self.parent, font=("Helvetica", 12), width=20)
        self.fav_entry.pack(pady=5)

        tk.Button(self.parent, text="Add City", font=("Helvetica", 10, "bold"),
                  bg="white", fg="purple", command=self.add_fav_city).pack()
        tk.Button(self.parent, text="Clear All", font=("Helvetica", 10, "bold"),
                  bg="#ffcccc", fg="red", command=self.clear_all_cities).pack(pady=(0, 5))


        self.cards_container = tk.Frame(self.parent, bg="#d9a5ff")
        self.cards_container.pack(pady=10, fill="both", expand=True)

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

        # Reject blank input
        if not city:
            messagebox.showwarning("Missing", "Please enter a city name.")
            return

        # Reject numbers, special characters, or single letters
        if not city.replace(" ", "").isalpha() or len(city) < 2:
            messagebox.showerror("Invalid", "Sorry babe, you must enter a real city.")
            return

        # Duplicate check
        if any(c["city"].lower() == city.lower() for c in self.fav_city_data):
            messagebox.showinfo("Duplicate", f"{city.title()} is already in your favorites.")
            return

        # Max 5 cities
        if len(self.fav_city_data) >= 5:
            messagebox.showwarning("Limit Reached", "You can only save 5 cities.")
            return

        try:
            data = fetch_weather_data(city)

            # ⛔ Verify the location in the response matches input
            api_city = data["location"]["name"].lower()
            input_city = city.lower()

            # Optional: normalize spacing and remove punctuation if needed
            if api_city != input_city:
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
            self.fav_entry.delete(0, tk.END)

        except Exception:
            messagebox.showerror("City Not Found", "Sorry babe, you must enter a real city.")

    def create_city_card(self, city_data):
        frame = tk.Frame(self.cards_container, bg="#b866e6", padx=10, pady=10)
        frame.pack(pady=6, fill="x")

        header = tk.Frame(frame, bg="#b866e6")
        header.pack(anchor="w", fill="x")

        tk.Label(header, text=city_data["city"], font=("Helvetica", 16, "bold"),
                 bg="#b866e6", fg="white").pack(side="left")

        try:
            icon_url = "http:" + city_data["icon"]
            raw_data = urllib.request.urlopen(icon_url).read()
            img = Image.open(io.BytesIO(raw_data)).resize((30, 30))
            icon = ImageTk.PhotoImage(img)
            icon_label = tk.Label(header, image=icon, bg="#b866e6")
            icon_label.image = icon
            icon_label.pack(side="left", padx=10)
        except:
            pass

        tk.Label(header, text=f"{city_data['temp']}°F", font=("Helvetica", 16),
                 bg="#b866e6", fg="white").pack(side="left")

        # 🗑️ DELETE BUTTON
        def delete_city():
            self.fav_city_data = [c for c in self.fav_city_data if c["city"] != city_data["city"]]
            self.save_fav_cities()
            frame.destroy()

        delete_btn = tk.Button(header, text="🗑️", font=("Helvetica", 10),
                               bg="#b866e6", fg="white", borderwidth=0,
                               command=delete_city)
        delete_btn.pack(side="right")

        # Hair tip below
        tk.Label(frame, text=city_data["hair_tip"], font=("Helvetica", 10, "italic"),
                 wraplength=250, bg="#b866e6", fg="white", justify="left").pack(anchor="w", pady=5)

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
