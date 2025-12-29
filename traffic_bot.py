import requests
import os
import sys

# --- SECRETS ---
API_KEY = os.environ["MAPS_API_KEY"]
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

# --- CONFIG ---
ORIGIN = "Times Square, New York, NY"      # MAKE SURE THESE ARE CORRECT
DESTINATION = "JFK Airport, New York, NY" 

def get_travel_time():
    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        "origins": ORIGIN,
        "destinations": DESTINATION,
        "key": API_KEY,
        "departure_time": "now",
        "traffic_model": "best_guess"
    }
    
    print(f"Connecting to Google Maps for route: {ORIGIN} to {DESTINATION}...")
    
    response = requests.get(url, params=params)
    data = response.json()

    # --- DEBUGGING PRINT ---
    # This will show us exactly what Google thinks went wrong
    print("GOOGLE RESPONSE:", data)
    # -----------------------

    # Check for top-level error status
    if data.get('status') != 'OK':
        print(f"API Error detected: {data.get('status')}")
        return None

    try:
        # Check specific element status (e.g., if route not found)
        element = data['rows'][0]['elements'][0]
        if element['status'] != 'OK':
             print(f"Route Error: {element['status']}")
             return None
             
        duration_seconds = element['duration_in_traffic']['value']
        return duration_seconds / 60
    except Exception as e:
        print(f"Parsing Error: {e}")
        return None

def main():
    minutes = get_travel_time()
    
    if minutes:
        print(f"SUCCESS! Travel time: {minutes} mins")
    else:
        print("FAILED to get travel time. Check the 'GOOGLE RESPONSE' above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
