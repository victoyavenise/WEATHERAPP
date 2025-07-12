import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import simpledialog
from PIL import Image, ImageTk
from datetime import datetime
import os
import csv
from tkinter import messagebox
import re

import re

def is_valid_city_name(city_name):
    """Validates that the city name contains only letters, spaces, hyphens, or apostrophes."""
    pattern = r"^[a-zA-Z\s\-']+$"
    return re.match(pattern, city_name) is not None






from config.weather_api_handler import fetch_weather_data, get_user_location, parse_daily_weather
from data.weather_csv_saver import save_to_csv
from features.favorite_cities_tab import FavoriteCitiesTab
from config.weather_api_handler import get_hair_tip 


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

def get_weather_icon_path(condition):
    condition = condition.lower()
    if "sunny" in condition:
        return "/Users/beeexpressdesigns/FORECASTHER_MAIN.PY/images/sun.svg"
    elif "cloudy" in condition:
        return "/Users/beeexpressdesigns/FORECASTHER_MAIN.PY/images/cloudy.svg"
    elif "rain" in condition or "drizzle" in condition:
        return "/Users/beeexpressdesigns/FORECASTHER_MAIN.PY/images/cloud_rain.svg"
    elif "thunder" in condition:
        return "/Users/beeexpressdesigns/FORECASTHER_MAIN.PY/images/thunder storm.svg"
    elif "snow" in condition:
        return "/Users/beeexpressdesigns/FORECASTHER_MAIN.PY/images/snowy.svg"
    else:
        return "/Users/beeexpressdesigns/FORECASTHER_MAIN.PY/images/sun.svg"

class ForecastHerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ForecastHer")
        self.root.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)

        self.setup_styles()
        self.create_hamburger_menu()
        self.create_tabs()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Custom.TFrame", background=BG_COLOR)
        style.configure("TNotebook.Tab", font=("Helvetica", 10, "bold"))

#menu
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
#tabs
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

#home screen
    def build_home_screen(self, parent):
        self.bg_canvas = tk.Canvas(parent, width=APP_WIDTH, height=APP_HEIGHT, highlightthickness=0)
        self.bg_canvas.pack(fill="both", expand=True)

    # Background Image
        try:
            bg_image = Image.open(BG_IMAGE_PATH).resize((APP_WIDTH, APP_HEIGHT))
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            self.bg_canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
        except Exception as e:
            print("Failed to load background:", e)

    # Logo
        try:
            logo = Image.open(LOGO_PATH).resize((200, 200))
            self.logo_photo = ImageTk.PhotoImage(logo)
            self.bg_canvas.create_image(APP_WIDTH // 2, 100, image=self.logo_photo)
        except Exception as e:
            print("Logo failed to load:", e)

    # ForecastHer Title
        self.bg_canvas.create_text(APP_WIDTH // 2, 220, text="forecastHer", font=("Helvetica", 22, "bold"), fill="white")
        self.bg_canvas.create_text(APP_WIDTH // 2, 250, text="Weather Forecast for Her", font=("Helvetica", 14, "italic"), fill="white")

    # Labels to be updated dynamically
        self.city_label = self.bg_canvas.create_text(APP_WIDTH // 2, 290, text="", font=("Helvetica", 14, "bold"), fill="white")
        self.weather_icon = None  # To store image reference
        self.weather_icon_id = self.bg_canvas.create_image(APP_WIDTH // 2, 275, anchor="center", image=None)

        self.temp_label = self.bg_canvas.create_text(APP_WIDTH // 2, 320, text="", font=("Helvetica", 12), fill="white")
        self.hilo_label = self.bg_canvas.create_text(APP_WIDTH // 2, 345, text="", font=("Helvetica", 11, "italic"), fill="white")
        self.condition_label = self.bg_canvas.create_text(APP_WIDTH // 2, 370, text="", font=("Helvetica", 11), fill="white")
        self.hair_tip_label = self.bg_canvas.create_text(APP_WIDTH // 2, 410, text="", font=("Helvetica", 10, "italic"), fill="white", width=260)



    # Search Button
        self.find_btn = tk.Button(
        self.bg_canvas,
        text="Find Your City",
        font=("Helvetica", 12, "bold"),
        bg="white",
        fg="PURPLE",
        relief="raised",
        padx=10,
        pady=5,
        command=self.open_city_search_page
    )
        self.bg_canvas.create_window(APP_WIDTH // 2, 450, window=self.find_btn)


   

#search yo city window
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

            if len(city) < 3:
                messagebox.showerror("Too Short", "Sis... that’s too short to be a real city 😩 Try typing at least 3 letters.")
                return

            if not is_valid_city_name(city):
                messagebox.showerror("Oops!", "Sorry babe, you must enter a real city 💁🏽‍♀️")
                return

            try:
                data = fetch_weather_data(city)
                if not data or "current" not in data or "location" not in data:
                    messagebox.showerror("Oops!", "Is that a real city sis? Cause, that city doesn’t exist or couldn’t be found. Try again and drop your real Lo this time!")
                    return

                actual_city_name = data["location"]["name"].lower()
                input_city_name = city.lower()

                if input_city_name not in actual_city_name:
                    messagebox.showerror("Oops!", f"Hmm... that doesn't look like a real city. You entered '{city}', but we couldn’t match it.")
                    return

                current = data["current"]
                temp = round(current["temp_f"])
                condition = current["condition"]["text"]
                humidity = current["humidity"]
                hair_tip_text = get_hair_tip(humidity)


        # Show weather icon
                try:
                    icon_path = get_weather_icon_path(condition)
                    icon_img = Image.open(icon_path).resize((60, 60))
                    self.weather_icon = ImageTk.PhotoImage(icon_img)
                    self.bg_canvas.itemconfig(self.weather_icon_id, image=self.weather_icon)
                except Exception as e:
                    print("Error loading weather icon:", e)

    
        # Update GUI
                self.bg_canvas.itemconfig(self.city_label, text=actual_city_name.title())
                self.bg_canvas.itemconfig(self.temp_label, text=f"{temp}°F")
                self.bg_canvas.itemconfig(self.hilo_label, text=f"High: {round(data['forecast']['forecastday'][0]['day']['maxtemp_f'])}°F | Low: {round(data['forecast']['forecastday'][0]['day']['mintemp_f'])}°F")
                self.bg_canvas.itemconfig(self.condition_label, text=f"Condition: {condition}")
                self.bg_canvas.itemconfig(self.hair_tip_label, text=hair_tip_text)
    
        # Save to CSV
                parsed = parse_daily_weather(data)
                save_to_csv(parsed)

        # Close the window
                search_window.destroy()
            
            except Exception as e:
                messagebox.showerror("Error", f"Something went wrong: {e}")
               
    
            # Bind the Enter key (Return) to run submit_city
        city_entry.bind("<Return>", lambda event: submit_city())


        tk.Button(
            search_window,
            text="Search",
            font=("Helvetica", 12, "bold"),
            bg="pink",
            fg="pink",
            command=submit_city
        ).pack(pady=20)

#top 5 cities 
    def build_fav_screen(self, parent):
        FavoriteCitiesTab(parent)
        tk.Label(parent, text="Your Top 5 Cities", font=("Helvetica", 14, "bold"), fg=FONT_COLOR, bg=BG_COLOR).pack(pady=20)


#hair cast tab
    def build_hair_screen(self, parent):
        tk.Label(parent, text="Today's HairCast", font=("Helvetica", 14, "bold"), fg=FONT_COLOR, bg=BG_COLOR).pack(pady=20)

    def select_tab(self, index):
        self.tab_control.select(index)

if __name__ == "__main__":
    root = tk.Tk()
    app = ForecastHerApp(root)
    root.mainloop()
