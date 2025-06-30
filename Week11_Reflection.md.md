
# ForecastHer Capstone – Week 11 Planning & Reflection

## 🗓️ Week 11 Reflection & Project Planning

### ✍️ Section 1: Week 11 Reflection

#### ✅ Key Takeaways
- Capstone projects are expected to be functional, creative, and well-documented.
- We should include at least three features and one enhancement.
- The app should demonstrate personal growth and applied skills from Weeks 1–10.
- Stretching beyond basic functionality is encouraged.
- Final product should be easy to use and visually polished.

#### 🔗 Concept Connections
**Strongest Skills:**
- API integration (WeatherAPI)
- GUI design using Tkinter
- Data visualization using Matplotlib

**Needs More Practice:**
- File organization and modularization
- Exception handling and error messages
- Writing automated tests and packaging Python apps

#### 🚧 Early Challenges
- API key was invalid initially and had to be regenerated.
- Tkinter updates caused lag in GUI refresh.
- Difficulty separating features cleanly into modules.
- Minor Git merge issues during early push attempts.

#### 🧰 Support Strategies
- Attend office hours for help with GUI bugs and layout.
- Post in Slack for Matplotlib help and interface styling tips.
- Use past lessons as reference for API handling and data storage.
- Get peer feedback on feature logic (especially Activity Suggestor).

---

### 🧠 Section 2: Feature Selection Rationale

| #  | Feature Name         | Difficulty (1–3) | Why You Chose It / Learning Goal                                         |
|----|----------------------|------------------|---------------------------------------------------------------------------|
| 1  | Activity Suggestor   | 3                | Build logic that uses weather data to recommend mood-based activities.    |
| 2  | Favorite Cities      | 2                | Allow saving/viewing of multiple city forecasts. Practice local data storage. |
| 3  | Humidity Hair Tips   | 1                | Offer beauty-focused weather tips for user engagement.                   |
| –  | **Enhancement:** Styled GUI (ForecastHer Look) | – | Add brand personality through color, fonts, and a feminine visual design. |

---

### 🗂️ Section 3: High-Level Architecture

```
/forecasther/
├── main.py               # Entry point for app
├── config.py             # API key and base URL
├── gui.py                # Tkinter layout and control
├── features/
│   ├── activity_suggestor.py
│   ├── favorite_cities.py
│   └── humidity_tips.py
├── data/
│   ├── weather_history.csv
│   └── favorite_cities.json
├── assets/               # Icons, images, backgrounds
└── README.md
```

**Data Flow:**
- `main.py` pulls API data using `config.py`
- Feature modules generate outputs based on conditions
- GUI displays results and user interactions update local files

---

### 📊 Section 4: Data Model Plan

| File/Table Name         | Format | Example Row                                             |
|-------------------------|--------|----------------------------------------------------------|
| weather_history.csv      | CSV    | 2025-06-30,New Orleans,92°F,Sunny,High Humidity         |
| favorite_cities.json     | JSON   | { "cities": ["Atlanta", "Houston", "Miami"] }           |

---

### 📆 Section 5: Personal Timeline (Weeks 12–17)

| Week | Monday           | Tuesday          | Wednesday         | Thursday          | Key Milestone              |
|------|------------------|------------------|--------------------|--------------------|-----------------------------|
| 12   | API setup        | Error handling   | Tkinter shell      | Buffer day         | Basic working app           |
| 13   | Humidity Tips    | Style display    | GUI polish         | Review logic       | Feature 1 complete          |
| 14   | Favorite Cities  | Save/load        | Test with API data | Connect to GUI     | Feature 2 complete          |
| 15   | Activity Suggestor | Logic tree     | UI dropdowns       | File save checks   | Feature 3 complete          |
| 16   | Final GUI polish | Docs             | Tests              | Packaging          | Ready-to-ship version       |
| 17   | Rehearse         | Debug            | Showcase           | –                  | Demo Day                    |

---

### ⚠️ Section 6: Risk Assessment

| Risk                  | Likelihood | Impact | Mitigation Plan                                    |
|-----------------------|------------|--------|----------------------------------------------------|
| API Rate Limits       | Medium     | Medium | Add delay or cache city data locally               |
| GUI responsiveness    | Low        | High   | Modularize UI code, use `after()` method if needed |
| User data save errors | Medium     | Medium | Add file checks and user feedback messages         |

---

### 🤝 Section 7: Support Requests

- Help with conditional logic for the Activity Suggestor
- Styling guidance for Matplotlib charts inside Tkinter
- Peer review of GUI usability and layout
- Help troubleshooting file save/load bugs in `favorite_cities.json`

---

### ✅ Section 8: Before Monday (Start of Week 12)

- [x] Push `main.py`, `config.py`, and `/data/` to GitHub  
- [x] Add WeatherAPI key to `.env` file (excluded from Git)  
- [x] Create `/features/` folder with starter files for each module  
- [x] Draft and commit `README.md` with planning and overview  
- [x] Begin coding Feature 1 (Humidity Hair Tips)
