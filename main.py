import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import re

from config.weather_api_handler import fetch_weather_data, get_hair_tip
from data.weather_csv_saver import save_to_csv
from features.favorite_cities_tab import FavoriteCitiesTab

# Paths
CSV_FILE = os.path.join(os.path.dirname(__file__), "data/weather_data.csv")
LOGO_PATH = "images/forecasther.png"
BG_IMAGE_PATH = "images/Rectangle 4.png"

# Style
APP_WIDTH = 320
APP_HEIGHT = 600
BG_COLOR = "#d9a5ff"
BTN_COLOR = "#4b0082"
FONT_COLOR = "white"

# Weather condition → image path or emoji
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

def get_weather_icon_path(condition):
    condition = condition.lower()
    for keyword, path in WEATHER_EMOJIS.items():
        if keyword in condition:
            return path
    return None

def is_valid_city_name(city_name):
    """Validates that the city name contains only letters, spaces, hyphens, or apostrophes."""
    pattern = r"^[a-zA-Z\s\-']+$"
    return re.match(pattern, city_name) is not None

def parse_daily_weather(api_data):
    """
    Extract a list of daily weather dicts with keys matching CSV_FIELDS from API response.
    """
    daily_list = []
    
    forecast_days = api_data.get("forecast", {}).get("forecastday", [])
    
    for day in forecast_days:
        date = day.get("date")
        day_info = day.get("day", {})
        temp = day_info.get("avgtemp_f", 0)
        humidity = day_info.get("avghumidity", 0)
        description = day_info.get("condition", {}).get("text", "")
        
        hair_tip = get_hair_tip(humidity)
        
        daily_list.append({
            "date": date,
            "temp": temp,
            "humidity": humidity,
            "description": description,
            "hair_tip": hair_tip
        })
    
    return daily_list

class ForecastHerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ForecastHer")
        self.root.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)

        # Keep references to images here to prevent GC
        self.weather_icon = None
        self.logo_photo = None
        self.emoji_text_id = None

        self.setup_styles()
        self.create_hamburger_menu()
        self.create_tabs()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Custom.TFrame", background=BG_COLOR)
        style.configure("TNotebook.Tab", font=("Helvetica", 10, "bold"))

    def create_hamburger_menu(self):
        self.menu_button = tk.Menubutton(
            self.root, text="☰", relief=tk.FLAT,
            bg=BG_COLOR, fg=FONT_COLOR, font=("Arial", 16)
        )
        self.menu = tk.Menu(self.menu_button, tearoff=0)
        self.menu.add_command(label="Home", command=lambda: self.select_tab(0))
        self.menu.add_command(label="Favorite Cities", command=lambda: self.select_tab(1))
        self.menu.add_command(label="HairCast", command=lambda: self.select_tab(2))
        self.menu_button["menu"] = self.menu
        self.menu_button.place(x=APP_WIDTH - 40, y=10)

    def create_tabs(self):
        self.tab_control = ttk.Notebook(self.root)

        self.home_tab = ttk.Frame(self.tab_control, style="Custom.TFrame")
        self.fav_tab = ttk.Frame(self.tab_control, style="Custom.TFrame")
        self.hair_tab = ttk.Frame(self.tab_control, style="Custom.TFrame")

        self.tab_control.add(self.home_tab, text="Home")
        self.tab_control.add(self.fav_tab, text="Favorites")
        self.tab_control.add(self.hair_tab, text="HairCast")

        self.tab_control.pack(expand=1, fill="both", pady=(50, 0))

        self.build_home_screen(self.home_tab)
        self.build_fav_screen(self.fav_tab)
        self.build_hair_screen(self.hair_tab)

    def build_home_screen(self, parent):
        self.bg_canvas = tk.Canvas(parent, width=APP_WIDTH, height=APP_HEIGHT, highlightthickness=0, bg=BG_COLOR)
        self.bg_canvas.pack(fill="both", expand=True)

        # Load and display background image
        try:
            if os.path.exists(BG_IMAGE_PATH):
                bg_image = Image.open(BG_IMAGE_PATH).resize((APP_WIDTH, APP_HEIGHT))
                self.bg_photo = ImageTk.PhotoImage(bg_image)
                self.bg_canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
            else:
                print("⚠️ Background image not found:", BG_IMAGE_PATH)
        except Exception as e:
            print("Failed to load background image:", e)

        # Load and display logo image at top center
        try:
            if os.path.exists(LOGO_PATH):
                logo_img = Image.open(LOGO_PATH).resize((100, 100), Image.ANTIALIAS)
                self.logo_photo = ImageTk.PhotoImage(logo_img)
                self.bg_canvas.create_image(APP_WIDTH // 2, 80, image=self.logo_photo, anchor="center")
            else:
                print("⚠️ Logo image not found:", LOGO_PATH)
        except Exception as e:
            print("Failed to load logo image:", e)

        # Title text
        self.bg_canvas.create_text(APP_WIDTH // 2, 220, text="forecastHer", font=("Helvetica", 22, "bold"), fill="white")
        self.bg_canvas.create_text(APP_WIDTH // 2, 250, text="Weather Forecast for Her", font=("Helvetica", 14, "italic"), fill="white")

        # Rounded rectangle card
        self.bg_canvas.create_rectangle(20, 270, 300, 500, fill="white", outline="", width=0)
        self.bg_canvas.create_rectangle(22, 272, 298, 498, fill="white", outline="#eee")  # border effect

        # Weather icon + city text
        self.weather_icon_id = self.bg_canvas.create_image(80, 300, anchor="center", image=None)
        self.city_label = self.bg_canvas.create_text(160, 300, text="", font=("Helvetica", 16, "bold"), fill="#4b0082", anchor="w")

        # Details labels
        self.temp_label = self.bg_canvas.create_text(APP_WIDTH // 2, 340, text="", font=("Helvetica", 12), fill="black")
        self.hilo_label = self.bg_canvas.create_text(APP_WIDTH // 2, 365, text="", font=("Helvetica", 11, "italic"), fill="black")
        self.condition_label = self.bg_canvas.create_text(APP_WIDTH // 2, 390, text="", font=("Helvetica", 11), fill="black")
        self.hair_tip_label = self.bg_canvas.create_text(APP_WIDTH // 2, 430, text="", font=("Helvetica", 10, "italic"), fill="#444", width=260)

        # Find city button
        self.find_btn = tk.Button(
            self.bg_canvas,
            text="Find Your City",
            font=("Helvetica", 12, "bold"),
            bg="#d94fe4",
            fg="white",
            relief="raised",
            padx=10,
            pady=5,
            command=self.open_city_search_page
        )
        self.bg_canvas.create_window(APP_WIDTH // 2, 480, window=self.find_btn)

    def open_city_search_page(self):
        search_window = tk.Toplevel(self.root)
        search_window.title("Search City")
        search_window.geometry("300x200")
        search_window.configure(bg="white")
        search_window.resizable(False, False)

        tk.Label(search_window, text="Enter City Name:", font=("Helvetica", 12, "bold"), bg="white").pack(pady=(20, 5))
        city_entry = tk.Entry(search_window, font=("Helvetica", 12), width=25)
        city_entry.pack(pady=5)

        def submit_city():
            city = city_entry.get().strip()
            if not city:
                messagebox.showwarning("Required", "Please enter a city name.")
                return
            if len(city) < 3 or not is_valid_city_name(city):
                messagebox.showerror("Oops!", "Sis... enter a valid city 🏙️")
                return

            try:
                data = fetch_weather_data(city)
                if not data or "current" not in data or "location" not in data:
                    messagebox.showerror("Error", "Couldn’t find that city, boo 💅")
                    return

                actual_city_name = data["location"]["name"]
                current = data["current"]
                temp = round(current["temp_f"])
                condition = current["condition"]["text"]
                humidity = current["humidity"]
                hair_tip_text = get_hair_tip(humidity)

                # Handle icon: image or emoji
                icon_path_or_emoji = get_weather_icon_path(condition)
                if icon_path_or_emoji and icon_path_or_emoji.endswith(".png"):
                    try:
                        icon_img = Image.open(icon_path_or_emoji).resize((50, 50))
                        self.weather_icon = ImageTk.PhotoImage(icon_img)
                        self.bg_canvas.itemconfig(self.weather_icon_id, image=self.weather_icon)
                        # Remove emoji text if any
                        if self.emoji_text_id:
                            self.bg_canvas.delete(self.emoji_text_id)
                            self.emoji_text_id = None
                    except Exception as e:
                        print("Icon load error:", e)
                        self.bg_canvas.itemconfig(self.weather_icon_id, image=None)
                else:
                    self.bg_canvas.itemconfig(self.weather_icon_id, image=None)
                    # Show emoji instead
                    if self.emoji_text_id:
                        self.bg_canvas.delete(self.emoji_text_id)
                    self.emoji_text_id = self.bg_canvas.create_text(80, 300, text=icon_path_or_emoji or "", font=("Helvetica", 30), fill="#4b0082")

                # Update texts
                self.bg_canvas.itemconfig(self.city_label, text=actual_city_name.title())
                self.bg_canvas.itemconfig(self.temp_label, text=f"{temp}°F")
                self.bg_canvas.itemconfig(
                    self.hilo_label,
                    text=f"High: {round(data['forecast']['forecastday'][0]['day']['maxtemp_f'])}°F | Low: {round(data['forecast']['forecastday'][0]['day']['mintemp_f'])}°F"
                )
                self.bg_canvas.itemconfig(self.condition_label, text=f"Condition: {condition}")
                self.bg_canvas.itemconfig(self.hair_tip_label, text=hair_tip_text)

                save_to_csv(data)

                search_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Something went wrong: {e}")

        city_entry.bind("<Return>", lambda event: submit_city())
        tk.Button(search_window, text="Search", font=("Helvetica", 12, "bold"), bg="#d94fe4", fg="white", command=submit_city).pack(pady=20)

    def build_fav_screen(self, parent):
        FavoriteCitiesTab(parent)
        tk.Label(parent, text="Your Top 5 Cities", font=("Helvetica", 14, "bold"), fg=FONT_COLOR, bg=BG_COLOR).pack(pady=20)

    def build_hair_screen(self, parent):
        tk.Label(parent, text="Today's HairCast", font=("Helvetica", 14, "bold"), fg=FONT_COLOR, bg=BG_COLOR).pack(pady=20)

    def select_tab(self, index):
        self.tab_control.select(index)


if __name__ == "__main__":
    root = tk.Tk()
    app = ForecastHerApp(root)
    root.mainloop()
