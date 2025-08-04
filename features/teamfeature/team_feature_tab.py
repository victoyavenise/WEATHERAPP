import customtkinter as ctk
import pandas as pd
import random
import glob
import os

class TeamFeatureTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#fb03b5")  # Pink background

        # Path to CSV folder
        self.csv_folder = "/Users/beeexpressdesigns/FORECASTHER_MAIN.PY/features/teamfeature/Data"


        # Title
        self.title_label = ctk.CTkLabel(
            self,
            text="🔥 Team Weather Face-off 🔥",
            font=("Helvetica", 22, "bold"),
            text_color="white"
        )
        self.title_label.pack(pady=(20, 10))

        # Comparison label
        self.comparison_label = ctk.CTkLabel(
            self,
            text="Click 'Compare Cities' to see who’s hotter!",
            font=("Helvetica", 16),
            text_color="white",
            wraplength=500,
            justify="center"
        )
        self.comparison_label.pack(pady=10)

        # Compare button
        self.compare_button = ctk.CTkButton(
            self,
            text="Compare Cities",
            command=self.compare_temperatures,
            fg_color="#ff66c4",  # Light pink
            hover_color="#ff3399"
        )
        self.compare_button.pack(pady=20)

    def compare_temperatures(self):
        # Get all CSV files in the folder
        csv_files = glob.glob(os.path.join(self.csv_folder, "*.csv"))

        if len(csv_files) < 2:
            self.comparison_label.configure(text="❌ Not enough CSV files to compare.")
            return

        # Load CSVs into DataFrames
        dataframes = [pd.read_csv(file) for file in csv_files]

        # Pick two different CSVs randomly
        df1, df2 = random.sample(dataframes, 2)

        # Pick a random row from each
        row1 = df1.sample(n=1).iloc[0]
        row2 = df2.sample(n=1).iloc[0]

        # Adjust these column names to match your CSVs
        city1 = row1['City']
        temp1 = row1['Temperature']

        city2 = row2['City']
        temp2 = row2['Temperature']

        print("[DEBUG] Looking for CSV files in:", self.csv_folder)
        print("[DEBUG] Found CSV files:", csv_files)

        # Compare temps and update label
        if temp1 > temp2:
            text = f"Ohhhh, it’s hotter in {city1} ({temp1}°) than in {city2} ({temp2}°)! 🌞🔥"
        elif temp1 < temp2:
            text = f"Ohhhh, it’s hotter in {city2} ({temp2}°) than in {city1} ({temp1}°)! 🌞🔥"
        else:
            text = f"Looks like {city1} and {city2} are equally hot at {temp1}°! 😎☀️"

        self.comparison_label.configure(text=text)


