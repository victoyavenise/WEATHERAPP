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
        return set(row["date"] for row in reader if "date" in row and row["date"])

def save_to_csv(daily_data):
    """Appends valid weather data to CSV if date is new."""
    if isinstance(daily_data, dict):
        daily_data = [daily_data]  # wrap single dict in a list

    print(f"[DEBUG] Received {len(daily_data)} forecast day(s)")

    existing_dates = get_existing_dates()
    file_exists = os.path.isfile(CSV_FILE)

    with open(CSV_FILE, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=CSV_FIELDS)
        if not file_exists:
            writer.writeheader()

        new_rows = 0
        for day in daily_data:
            print(f"[DEBUG] Current day: {day}")
            
            # Validate each row
            if not isinstance(day, dict):
                print("❌ Skipping invalid row (not a dict):", day)
                continue
            if "date" not in day or not isinstance(day["date"], str):
                print("❌ Skipping row with missing or invalid 'date':", day)
                continue
            if day["date"] in existing_dates:
                print(f"⏩ Skipping duplicate date: {day['date']}")
                continue

            writer.writerow(day)
            new_rows += 1

    print(f"✅ {new_rows} new row(s) added.")

# Optional: Run test when this script is run directly
if __name__ == "__main__":
    dummy_data = {
        "date": "2025-06-24",
        "temp": 84.2,
        "humidity": 68,
        "description": "partly cloudy",
        "hair_tip": "Uh oh. Hair’s starting to puff, wave up, or lose its press. That’s reversion knocking."
    }
    save_to_csv(dummy_data)
