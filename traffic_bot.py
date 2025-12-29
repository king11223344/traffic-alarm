import requests
import os
import sys

# --- SECRETS (Fetched from Environment Variables) ---
API_KEY = os.environ["MAPS_API_KEY"]
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

# --- CONFIG ---
ORIGIN = "Phase I, Ashraya Layout, Garudachar Palya, Mahadevapura, Bengaluru, Karnataka 560048"      # Update this
DESTINATION = "2nd Main, 1st Cross Rd, JCR Layout, Panathur, Bengaluru, Karnataka 560087"  # Update this
TARGET_THRESHOLD_MINS = 10                 # Update this

def send_telegram_alert(minutes):
    message = f"🚨 TRAFFIC ALERT 🚨\n\nTravel time is down to {int(minutes)} mins!\nGo now!"
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, data=data)

def get_travel_time():
    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        "origins": ORIGIN,
        "destinations": DESTINATION,
        "key": API_KEY,
        "departure_time": "now",
        "traffic_model": "best_guess"
    }
    response = requests.get(url, params=params)
    data = response.json()
    try:
        duration_seconds = data['rows'][0]['elements'][0]['duration_in_traffic']['value']
        return duration_seconds / 60
    except:
        return None

def main():
    # GitHub Actions handles the scheduling, so we just run ONCE and exit.
    minutes = get_travel_time()
    
    if minutes:
        print(f"Current travel time: {minutes} mins")
        if minutes <= TARGET_THRESHOLD_MINS:
            send_telegram_alert(minutes)
    else:
        print("Error fetching data")
        sys.exit(1)

if __name__ == "__main__":
    main()
