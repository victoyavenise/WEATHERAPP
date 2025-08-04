# 🌦️ ForecastHer

**ForecastHer** is a personalized weather dashboard designed with women in mind. It goes beyond the forecast by giving **beauty tips**, **self-care suggestions**, and allowing users to **track multiple favorite cities** — all wrapped in a feminine, user-friendly design.

---

## 💡 Project Overview

ForecastHer is a **Python-based desktop app** that integrates with the **WeatherAPI** and **GeoPy** to provide **real-time and 5-day forecasts** in a styled `customtkinter` GUI.  
It’s built to help women make smart, stylish, and self-care–focused decisions based on weather, especially when **humidity** can make or break a look.

---

## 🛠️ Key Features

| Feature                    | Description                                                                 |
|----------------------------|-----------------------------------------------------------------------------|
| 🌸 **Humidity Hair Tips**  | Live hair care advice based on real-time humidity levels                     |
| 🧘 **Activity Suggestor**  | Recommends self-care & lifestyle activities tailored to current conditions  |
| 📍 **Favorite Cities Tab** | Save, view, and scroll through weather for multiple cities                   |
| 🎨 **Styled GUI**          | Feminine pink/purple/blue theme, custom fonts, hover effects, and icons     |
| 🖼️ **Custom Weather Icons**| Replaces generic icons with styled PNG images for each condition            |
| 📊 **5-Day Forecast**      | Auto-generated daily forecast cards with highs, lows, and icons              |
| 📂 **CSV Data Tracking**   | Saves weather history and favorite cities locally for offline access         |
| 🛡️ **Error Handling**      | Friendly messages for invalid city input and API issues                      |

---

## 📸 Screenshots

*Coming Soon — Live UI previews of ForecastHer in action.*

---

## 🔧 Technologies Used

- **Python 3.11+**
- **CustomTkinter** – modern themed Tkinter UI
- **WeatherAPI** – real-time and forecasted weather data
- **GeoPy** – detects user location automatically
- **Matplotlib** – planned 5-day data visualization
- **CSV & JSON** – data persistence for history & settings
- **dotenv** – secure API key storage

---

## 📂 Project Structure

```
/forecasther/
├── main.py                         # App entry point
├── config/
│   ├── weather_api_handler.py      # API calls & geolocation
├── features/
│   ├── haircast_tab.py             # Hair tips UI logic
│   ├── favorite_cities_tab.py      # Scrollable favorite cities tab
│   ├── activity_suggestor.py       # Activity suggestion logic
├── data/
│   ├── weather_history.csv
│   └── favorite_cities.json
├── images/                         # Icons, weather emojis, logo
├── .env                            # API key
└── README.md
```

---

## 🚧 Roadmap

### ✅ Completed:
- WeatherAPI + GeoPy integration
- Gradient-free clean GUI
- Custom weather icons
- Humidity-based hair care tips
- Favorite cities tab (scrollable list)
- Error handling for bad input
- Local CSV/JSON saving

### 🛠️ In Progress:
- Activity suggestion feature
- Matplotlib visual forecast
- Skin care tips based on weather
- Exportable daily weather reports

### 💭 Future Plans:
- Integration with beauty product APIs
- Push notifications for “bad hair day” alerts
- Social media sharing of forecasts

---

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
