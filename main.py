import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import simpledialog
from PIL import Image, ImageTk
from datetime import datetime
import os
import csv

from config.weather_api_handler import fetch_weather_data, get_user_location, parse_daily_weather
from data.weather_csv_saver import save_to_csv

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
        self.bg_canvas = tk.Canvas(parent, width=APP_WIDTH, height=APP_HEIGHT, highlightthickness=0)
        self.bg_canvas.pack(fill="both", expand=True)

        try:
            bg_image = Image.open(BG_IMAGE_PATH).resize((APP_WIDTH, APP_HEIGHT))
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            self.bg_canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
        except Exception as e:
            print("Failed to load background:", e)

        try:
            logo = Image.open(LOGO_PATH).resize((300, 300))
            self.logo_photo = ImageTk.PhotoImage(logo)
            self.bg_canvas.create_image(APP_WIDTH // 2, 100, image=self.logo_photo)
        except Exception as e:
            print("Logo failed to load:", e)

        self.bg_canvas.create_text(APP_WIDTH // 2, 240, text="forecastHer", font=("Helvetica", 22, "bold"), fill="white")
        self.bg_canvas.create_text(APP_WIDTH // 2, 270, text="Weather Forecast for Her", font=("Helvetica", 14, "italic"), fill="white")

        self.city_label = self.bg_canvas.create_text(APP_WIDTH // 2, 320, text="", font=("Helvetica", 12, "bold"), fill="white")
        self.weather_label = self.bg_canvas.create_text(APP_WIDTH // 2, 350, text="", font=("Helvetica", 12), fill="white")

        self.find_btn = tk.Button(
            self.bg_canvas,
            text="Find Your City",
            font=("Helvetica", 12, "bold"),
            bg=BTN_COLOR,
            fg="white",
            relief="raised",
            padx=10,
            pady=5,
            command=self.open_city_search_page
        )
        self.bg_canvas.create_window(APP_WIDTH // 2, 400, window=self.find_btn)

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
            city = city_entry.get()
            if not city:
                messagebox.showwarning("Required", "Please enter a city name.")
                return

            try:
                self.bg_canvas.itemconfig(self.city_label, text=city)

                data = fetch_weather_data(city)
                current = data["current"]
                temp = round(current["temp_f"])
                condition = current["condition"]["text"]
                self.bg_canvas.itemconfig(self.weather_label, text=f"{temp}°F – {condition}")

                parsed = parse_daily_weather(data)
                save_to_csv(parsed)

                search_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(
            search_window,
            text="Search",
            font=("Helvetica", 12, "bold"),
            bg=BTN_COLOR,
            fg="white",
            command=submit_city
        ).pack(pady=20)

    def build_fav_screen(self, parent):
        tk.Label(parent, text="Your Top 5 Cities", font=("Helvetica", 14, "bold"), fg=FONT_COLOR, bg=BG_COLOR).pack(pady=20)

    def build_hair_screen(self, parent):
        tk.Label(parent, text="Today's HairCast", font=("Helvetica", 14, "bold"), fg=FONT_COLOR, bg=BG_COLOR).pack(pady=20)

    def select_tab(self, index):
        self.tab_control.select(index)

if __name__ == "__main__":
    root = tk.Tk()
    app = ForecastHerApp(root)
    root.mainloop()
