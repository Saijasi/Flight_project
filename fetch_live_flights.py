import requests
import psycopg2

# Your AviationStack API key (Replace with your actual key)
API_KEY = "5f7a1b0f05b4aabc706523da715dbb14"
API_URL = f"http://api.aviationstack.com/v1/flights?access_key=5f7a1b0f05b4aabc706523da715dbb14"

# Connect to PostgreSQL
DB_NAME = "flights_db"
DB_USER = "postgres"
DB_PASSWORD = "ss1234"  # Replace with your password
DB_HOST = "localhost"
DB_PORT = "5432"

try:
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    print("✅ Connected to PostgreSQL!")
except Exception as e:
    print(f"❌ Database connection error: {e}")

# Fetch live flight data
API_URL = "http://api.aviationstack.com/v1/flights?access_key=5f7a1b0f05b4aabc706523da715dbb14"
response = requests.get(API_URL)

data = response.json()

if "data" in data:
    flights = data["data"]
    cur = conn.cursor()
    
    for flight in flights[:10]:  # Fetch first 10 flights
        flight_number = flight["flight"]["iata"] or "Unknown"
        airline = flight["airline"]["name"] or "Unknown"
        departure_airport = flight["departure"]["iata"] or "Unknown"
        arrival_airport = flight["arrival"]["iata"] or "Unknown"
        departure_time = flight.get("departure", {}).get("estimated")
        arrival_time = flight.get("arrival", {}).get("estimated")
        status = flight.get("status", "On Time")  # Default to "On Time" if status is missing

# Map API status to allowed values
        status_mapping = {
    "scheduled": "On Time",  # Map scheduled to "On Time"
    "active": "On Time",
    "landed": "On Time",
    "delayed": "Delayed",
    "cancelled": "Cancelled"
}

# Get status from API response
api_status = flight.get("status", "On Time")  # Default to "On Time" if missing

# Convert API status to allowed values
status = status_mapping.get(api_status.lower(), "On Time")  # Map to allowed values
delay = flight.get("delay", 0)

if departure_time in [None, "Unknown"]:
    departure_time = "1970-01-01 00:00:00"
if arrival_time in [None, "Unknown"]:
    arrival_time = "1970-01-01 00:00:00"
if delay is None or delay == 0:
    delay = "0 minutes"  # INTERVAL expects a string like '0 minutes'
else:
    delay = f"{delay} minutes"
    allowed_statuses = ["scheduled", "active", "landed", "cancelled", "delayed"]
    if status not in allowed_statuses:
        status = "scheduled"    
        
        cur.execute("""
    INSERT INTO flights (flight_number, airline, departure_airport, arrival_airport, departure_time, arrival_time, status, delay_duration)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
""", (flight_number, airline, departure_airport, arrival_airport, departure_time, arrival_time, status, delay))
        conn.commit()
        cur.close()
        conn.close()
        print(f"Inserting: {flight_number}, {airline}, {departure_airport}, {arrival_airport}, {departure_time}, {arrival_time}, {status}, {delay}")
    else:
        print("❌ Failed to fetch data")

