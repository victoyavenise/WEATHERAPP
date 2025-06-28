import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
from datetime import datetime

# Import your API and CSV handlers
from weather_api_handler import fetch_weather_data, get_user_location, parse_daily_weather
from weather_csv_saver import save_to_csv


# Debug print test
lat, lon, city = get_user_location()
print(f"Testing geolocation: {city} | Lat: {lat}, Lon: {lon}")


CSV_FILE = "weather_data.csv"
CSV_FIELDS = ["date", "temp", "humidity", "description", "hair_tip"]

# Brand colors (you can adjust)
BG_COLOR = "#ffe6f0"
HEADER_COLOR = "#ff66b2"
ROW_ALT_COLOR = "#fff5fb"
FONT_COLOR = "#4b0082"
ACCENT_BLUE = "#99ccff"


def read_last_7_days():
    if not os.path.isfile(CSV_FILE):
        return []
    with open(CSV_FILE, mode="r") as file:
        reader = list(csv.DictReader(file))
        return reader[-7:]


class WeatherAppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ForecastHer – Weekly Weather")
        self.root.geometry("940x350")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)

        self.setup_style()
        self.create_widgets()
        self.load_data()

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Treeview",
            background="white",
            foreground=FONT_COLOR,
            rowheight=32,
            fieldbackground=BG_COLOR,
            font=("Helvetica", 10),
        )
        style.configure(
            "Treeview.Heading",
            font=("Helvetica", 11, "bold"),
            background=HEADER_COLOR,
            foreground="white",
        )
        style.map(
            "Treeview",
            background=[("selected", ACCENT_BLUE)],
            foreground=[("selected", "black")],
        )

    def create_widgets(self):
        # Treeview setup
        self.tree = ttk.Treeview(self.root, columns=CSV_FIELDS, show="headings", height=7)
        self.tree.tag_configure("even", background=ROW_ALT_COLOR)
        self.tree.tag_configure("odd", background="white")

        for col in CSV_FIELDS:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=160 if col == "hair_tip" else 100, anchor="center")

        self.tree.pack(padx=12, pady=12, fill="x")

        # Refresh button
        self.refresh_button = ttk.Button(self.root, text="Refresh Data", command=self.refresh_data)
        self.refresh_button.pack(pady=(0, 10))

    def load_data(self):
        # Clear existing rows
        for row in self.tree.get_children():
            self.tree.delete(row)

        data = read_last_7_days()
        for i, row in enumerate(data):
            tag = "even" if i % 2 == 0 else "odd"
            self.tree.insert("", "end", values=[row.get(col, "") for col in CSV_FIELDS], tags=(tag,))

        self.show_today_hair_tip(data)

    def refresh_data(self):
        self.refresh_button.config(state="disabled")
        self.root.update_idletasks()
        try:
            weather_data = fetch_weather_data()
            if weather_data:
                daily_data = parse_daily_weather(weather_data)
                save_to_csv(daily_data)
                messagebox.showinfo("Success", "Weather data refreshed successfully!")
            else:
                messagebox.showwarning("Warning", "Failed to fetch weather data.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{e}")
        finally:
            self.refresh_button.config(state="normal")
            self.load_data()

    def show_today_hair_tip(self, data):
        today = datetime.now().strftime("%Y-%m-%d")
        today_data = next((row for row in data if row["date"] == today), None)
        if today_data:
            humidity = today_data.get("humidity", "?")
            tip = today_data.get("hair_tip", "No tip available.")
            messagebox.showinfo("Today's Hair Tip", f"Humidity: {humidity}%\n\n{tip}")


def create_weekly_viewer():
    root = tk.Tk()
    app = WeatherAppGUI(root)
    root.mainloop()


if __name__ == "__main__":
    create_weekly_viewer()

