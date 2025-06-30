
# 🌦️ ForecastHer

**ForecastHer** is a personalized weather dashboard designed with women in mind. It goes beyond the forecast by suggesting beauty tips, self-care activities, and allowing users to track weather across their favorite cities — all with a feminine, user-friendly design.

---

## 💡 Project Overview

ForecastHer is a Python-based desktop application that uses the WeatherAPI to display live and future weather data in a styled Tkinter GUI. It’s built to help users make decisions about their day — especially when humidity, heat, or sudden rain might affect hair, mood, or plans.

---

## 🛠️ Features

| Feature              | Description                                                                 |
|----------------------|-----------------------------------------------------------------------------|
| 🌸 Humidity Hair Tips | Personalized hair care advice based on real-time humidity levels           |
| 🧘 Activity Suggestor | Recommends self-care or productivity activities based on current conditions |
| 📍 Favorite Cities     | Save and view weather for multiple cities                                   |
| 🎨 Styled GUI         | Feminine design using a pink/purple/blue theme with custom fonts & layout  |

---

## 📸 Screenshots

*Coming Soon: UI previews of ForecastHer in action*

---

## 🔧 Technologies Used

- **Python 3**
- **Tkinter** – for the desktop GUI
- **WeatherAPI** – for real-time and forecasted weather data
- **Matplotlib** – for 5-day visual forecasts (in progress)
- **CSV & JSON** – for saving weather history and user preferences
- **dotenv** – for storing API keys securely

---

## 📂 Project Structure

```
/forecasther/
├── main.py               # App entry point
├── config.py             # API setup
├── gui.py                # Interface layout
├── features/
│   ├── activity_suggestor.py
│   ├── favorite_cities.py
│   └── humidity_tips.py
├── data/
│   ├── weather_history.csv
│   └── favorite_cities.json
├── assets/               # Icons, images, custom fonts
└── README.md
```

---

## 🚧 Roadmap

### ✅ Completed:
- Basic weather API integration
- Functional GUI with city input
- Humidity-based hair care tips
- Favorite city list (saved locally)

### 🛠️ In Progress:
- Activity suggestion logic
- Data visualization for 5-day forecast
- Save/load weather history



---

## ⚠️ Setup Instructions

1. Clone the repo:
   ```bash
   git clone https://github.com/yourusername/forecasther.git
   cd forecasther
   ```

2. Create a `.env` file and add your WeatherAPI key:
   ```
   WEATHER_API_KEY=your_api_key_here
   ```

3. Install dependencies (optional if using virtualenv):
   ```bash
   pip install -r requirements.txt
   ```

4. Run the app:
   ```bash
   python main.py
   ```

---

## 👩‍💻 About the Creator

**Victoya Venise**  
Designer + Developer | Columbia University Tech Fellow | Founder of Bee Express Designs  
✨ Building tools for creativity, confidence, and community.

[LinkedIn](https://www.linkedin.com/in/victoya-venise-66a1a6a0/) • [Portfolio](https://drive.google.com/file/d/12mwNI7nfB7wh_U1q73MR2mn3D8hiXKeZ/view)

---



## 🫶 Contributions & Feedback

Got a feature idea? Want to collaborate?  
Open an issue or reach out via LinkedIn!
