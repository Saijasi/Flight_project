import psycopg2
import pandas as pd

# Database connection details
DB_NAME = "flights_db"
DB_USER = "postgres"
DB_PASSWORD = "your_postgres_password"  # Replace with your actual password
DB_HOST = "localhost"
DB_PORT = "5432"

# Connect to PostgreSQL
try:
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    print("✅ Connection to PostgreSQL successful!")
except Exception as e:
    print(f"❌ Error connecting to PostgreSQL: {e}")

# Create a cursor to interact with the database
cur = conn.cursor()

# Run a query to fetch all flights from Frankfurt (FRA)
query = "SELECT * FROM flights WHERE departure_airport = 'FRA';"
cur.execute(query)

# Fetch all results
rows = cur.fetchall()

# Convert to pandas DataFrame for better display
df = pd.DataFrame(rows, columns=["ID", "Flight Number", "Airline", "Departure Airport", "Arrival Airport", "Departure Time", "Arrival Time", "Status", "Delay Duration"])
print(df)

# Close the connection
cur.close()
conn.close()
