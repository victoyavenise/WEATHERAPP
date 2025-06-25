import csv
import os

CSV_FILE = "weather_data.csv"
CSV_FIELDS = ["date", "temp", "humidity", "description", "hair_tip"]

def get_existing_dates():
    """Reads the existing CSV and returns a set of dates already saved."""
    if not os.path.isfile(CSV_FILE):
        return set()
    with open(CSV_FILE, mode="r") as file:
        reader = csv.DictReader(file)
        return set(row["date"] for row in reader)

def save_to_csv(daily_data):
    """Appends new daily weather data to CSV (avoids duplicates)."""
    file_exists = os.path.isfile(CSV_FILE)
    existing_dates = get_existing_dates()

    with open(CSV_FILE, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=CSV_FIELDS)
        
        if not file_exists:
            writer.writeheader()

        new_rows = 0
        for day in daily_data:
            if day["date"] not in existing_dates:
                writer.writerow(day)
                new_rows += 1

    print(f"✅ {new_rows} new row(s) added to {CSV_FILE}." if new_rows else "ℹ️ No new data added.")

# Optional: test the saver with dummy data
if __name__ == "__main__":
    dummy_data = [
        {
            "date": "2025-06-24",
            "temp": 84.2,
            "humidity": 68,
            "description": "partly cloudy",
            "hair_tip": "Uh oh. Hair’s starting to puff, wave up, or lose its press. That’s reversion knocking."
        }
    ]
    save_to_csv(dummy_data)
