# 🌦️ ForecastHer

**ForecastHer** is a personalized weather dashboard designed with women in mind.  
It goes beyond the forecast by suggesting beauty tips, self-care activities, and allowing users to track weather across their favorite cities — all with a feminine, user-friendly design.

---

## 💡 Project Overview

ForecastHer is a **Python-based desktop application** built with **CustomTkinter**.  
It integrates the **WeatherAPI** to display live and forecast weather data in a styled, interactive GUI.  
The app helps users make better decisions about their day — especially when humidity, heat, or sudden rain might impact hair, mood, or plans.

---

## 🛠️ Core Features

| Feature                | Description                                                                 |
|------------------------|-----------------------------------------------------------------------------|
| 🌸 **Humidity Hair Tips** | Personalized hair care advice based on real-time humidity levels           |
| 📍 **Favorite Cities**    | Save and view weather for multiple cities                                 |
| 🎨 **Styled GUI**         | Feminine design with a pink/purple theme, custom fonts, and modern layout |
| 🤝 **Team Feature**       | Compares random weather data from multiple CSV datasets                   |

---

## 🆕 About the Team Feature

The **Team Feature** is a fun, collaborative addition that:

- Pulls **two random rows** from **two different CSV files** in the `/features/teamfeature/Data/` folder.
- Compares temperatures and shows a playful message like:

> “Ohhhh, it’s hotter in Miami (89°) than in Los Angeles (82°)! 🌞🔥”

- **Data Format Requirement:** CSVs must include at least `City` and `Temperature` columns.
- **Minimum Requirement:** 2 CSV files (but works best with more).
- **Custom Output:** Fun, emoji-filled responses for user engagement.

**Example CSV Structure:**
```csv
City,Temperature,Humidity
New York,78,65
Los Angeles,85,50
Chicago,72,55


## ⚙️ Setup Instructions

1. **Clone the repo**
   ```bash
   git clone https://github.com/yourusername/forecasther.git
   cd forecasther
   ```

2. **Create `.env`** and add your WeatherAPI key:
   ```
   WEATHER_API_KEY=your_api_key_here
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app**
   ```bash
   python main.py
   ```

---

## 👩‍💻 About the Creator

**Victoya Venise**  
Designer + Developer | Columbia University Tech Fellow | Founder, Bee Express Designs  
✨ Building tools for creativity, confidence, and community.

[LinkedIn](https://www.linkedin.com/in/victoya-venise-66a1a6a0/) • [Portfolio](https://drive.google.com/file/d/12mwNI7nfB7wh_U1q73MR2mn3D8hiXKeZ/view)

---

## 🫶 Contributions & Feedback

Got ideas? Want to collaborate?  
Open an issue or reach out on LinkedIn!

Your baby hairs will ball up into a fist and fight you. Line credited to [@nolacomics](https://www.instagram.com/backatown_comics/)
Custom Icons provided by https://linktr.ee/nainmade
