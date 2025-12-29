import requests
import os
import sys

# --- SECRETS ---
API_KEY = os.environ["MAPS_API_KEY"]
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

# --- CONFIG ---
ORIGIN = "Times Square, New York, NY"      
DESTINATION = "JFK Airport, New York, NY" 

def main():
    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        "origins": ORIGIN,
        "destinations": DESTINATION,
        "key": API_KEY,
        "departure_time": "now",
        "traffic_model": "best_guess"
    }
    
    print(f"--- DEBUG LOG START ---")
    print(f"Checking route: {ORIGIN} -> {DESTINATION}")
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        # PRINT THE EXACT ERROR FROM GOOGLE
        print("GOOGLE SAYS:", data)
        
        if data.get('status') == 'OK':
             print("Status is OK. Checking elements...")
             element = data['rows'][0]['elements'][0]
             if element.get('status') == 'OK':
                 duration = element['duration_in_traffic']['value'] / 60
                 print(f"SUCCESS! Time: {duration} mins")
             else:
                 print(f"ROUTE ERROR: {element.get('status')}")
                 sys.exit(1)
        else:
             print(f"API ERROR: {data.get('status')}")
             if 'error_message' in data:
                 print(f"DETAILS: {data['error_message']}")
             sys.exit(1)

    except Exception as e:
        print(f"PYTHON CRASH: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
