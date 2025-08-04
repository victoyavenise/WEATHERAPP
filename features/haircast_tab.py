import customtkinter as ctk
import random
from config.weather_api_handler import fetch_weather_data, get_user_location, get_hair_tip

class HairCastTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#fb03b5")  # Bright pink background
        self.pack(fill="both", expand=True)
        
        # Fun, sassy subtitles
        haircast_subtitles = [
            "See what today’s weather got planned for your hair, sis 💁🏽‍♀️",
            "Find out if today’s forecast is hair goals… or hair drama 😅",
            "Is today a silk press day or a bun day? Let’s check 👀",
            "Your hair forecast is in — let’s see what we’re working with 💕",
            "Weather check: Will your style slay or stray today? ✨"
        ]
        random_subtitle = random.choice(haircast_subtitles)

        # Title (random subtitle)
        ctk.CTkLabel(
            self,
            text=random_subtitle,
            font=("Helvetica", 20, "bold"),
            text_color="white",
            fg_color="transparent",
            wraplength=500,
            justify="center"
        ).pack(pady=20)

        # Subtitle description
        ctk.CTkLabel(
            self,
            text="See how today’s weather will treat your hair!",
            font=("Helvetica", 16, "italic"),
            text_color="white",
            fg_color="transparent"
        ).pack(pady=5)

        # City entry field
        self.city_entry = ctk.CTkEntry(
            self,
            placeholder_text="Enter city name...",
            width=250,
            font=("Helvetica", 14)
        )
        self.city_entry.pack(pady=10)

        # Bind Enter key to trigger search
        self.city_entry.bind("<Return>", lambda event: self.display_hair_tip())

        # Search button
        self.search_button = ctk.CTkButton(
            self,
            text="Get Hair Tip",
            command=self.display_hair_tip,
            fg_color="#FF69B4",  # Hot pink button
            hover_color="#FF1493",
            font=("Helvetica", 14, "bold"),
            corner_radius=10
        )
        self.search_button.pack(pady=5)

        # Result label
        self.result_label = ctk.CTkLabel(
            self,
            text="Loading your hair tip...",
            wraplength=450,
            justify="center",
            font=("Helvetica", 14),
            text_color="white"
        )
        self.result_label.pack(pady=20)

        # Auto-load current location hair tip when tab opens
        self.after(500, self.load_current_location_tip)

    def load_current_location_tip(self):
        try:
            # Get user's current location
            location_data = get_user_location()
            city = location_data["city"]

            # Fetch weather data for current location
            data = fetch_weather_data(city)
            humidity = data["current"]["humidity"]

            # Get hair tip
            hair_tip = get_hair_tip(humidity)

            # Display results
            self.result_label.configure(
                text=f"📍 City: {city}\n💧 Humidity: {humidity}%\n💇 Tip: {hair_tip}"
            )

        except Exception as e:
            self.result_label.configure(text=f"⚠️ Error getting ya lo: {str(e)}")

    def display_hair_tip(self):
        city = self.city_entry.get().strip()
        if not city:
            self.result_label.configure(text="Sis that's not a real city!")
            return

        try:
            # Get weather data for entered city
            data = fetch_weather_data(city)
            humidity = data["current"]["humidity"]

            # Get hair tip
            hair_tip = get_hair_tip(humidity)

            # Display results
            self.result_label.configure(
                text=f"📍 City: {city}\n💧 Humidity: {humidity}%\n💇 Tip: {hair_tip}"
            )

        except Exception as e:
            self.result_label.configure(
                text=f"⚠️ Error Sis Try again '{city}': {str(e)}"
            )
