import tkinter as tk
from PIL import ImageTk, Image
import requests
import io
from urllib.request import urlopen
import ssl
ssl_content = ssl._create_unverified_context

# Emoji mapping for weather descriptions
WEATHER_EMOJIS = {
    "sunny": "☀️",
    "clear": "🌤️",
    "cloud": "☁️",
    "rain": "🌧️",
    "snow": "❄️",
    "thunder": "⚡",
    "fog": "🌫️",
    "overcast": "☁️",
    "mist": "🌫️"
}

def get_weather_emoji(condition):
    condition = condition.lower()
    for key in WEATHER_EMOJIS:
        if key in condition:
            return WEATHER_EMOJIS[key]
    return "❓"  # question mark emoji for unknown


# ForecastHer soft pink/blue aesthetic
CARD_BG = "#fff5fb"
FONT_MAIN = ("Helvetica", 10, "bold")
FONT_SUB = ("Helvetica", 9)
TEXT_GRAY = "#888"

def create_forecast_card(parent, day, temp, hi_lo, condition, icon_url, hair_tip=""):
    card = tk.Frame(parent, bg="#fff5fb", width=140, height=160, relief="raised", bd=2)
    card.pack_propagate(False)
    card.pack(side="left", padx=8)

    tk.Label(card, text=day, bg="#fff5fb", fg="#4b0082", font=("Helvetica", 10, "bold")).pack()

    # Try to load icon image
    try:
        image_bytes = urlopen("https:" + icon_url).read()
        image_data = Image.open(io.BytesIO(image_bytes))
        image_data = image_data.resize((35, 35), Image.ANTIALIAS)
        icon_img = ImageTk.PhotoImage(image_data)

        icon_label = tk.Label(card, image=icon_img, bg="#fff5fb")
        icon_label.image = icon_img  # store reference
        icon_label.pack(pady=(2, 0))
    except Exception as e:
        print("[WARN] Could not load icon:", e)
        emoji = get_weather_emoji(condition)
        tk.Label(card, text=emoji, font=("Helvetica", 20), bg="#fff5fb").pack(pady=(2, 0))

    # Temperature Info
    tk.Label(card, text=f"{temp}°F", bg="#fff5fb", fg="#4b0082", font=("Helvetica", 12)).pack()
    tk.Label(card, text=hi_lo, bg="#fff5fb", fg="#666", font=("Helvetica", 8)).pack()

    # Hair Tip
    tip_label = tk.Label(
        card,
        text=hair_tip,
        bg="#fff5fb",
        fg="#cc6699",
        font=("Helvetica", 7),
        wraplength=120,
        justify="center"
    )
    tip_label.pack(pady=(5, 2))
