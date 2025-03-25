✈️ Flight Project

📌 Overview
This project fetches live flight data and stores it in a PostgreSQL database. It consists of two Python scripts:
-db_connect.py: Handles the database connection.
-fetch_live_flights.py: Fetches live flight data and inserts it into the database.

🛠️ Technologies Used
-Python
-PostgreSQL
-psycopg2 (Python library for PostgreSQL)

📂 Project Structure
📁 Flight Project  
 ├── 📜 db_connect.py           # Database connection script  
 ├── 📜 fetch_live_flights.py   # Fetches and stores flight data  
 ├── 📜 README.md               # Project documentation  

🚀 How to Run the Project
-Clone the Repository
git clone https://github.com/Saijasi/Flight_project.git
cd Flight_project
-Install Dependencies
pip install psycopg2
-Run the Scripts
-First, establish the database connection:
python db_connect.py
-Then, fetch live flight data:
python fetch_live_flights.py

📌 Notes
-Ensure PostgreSQL is installed and running.
-Update database credentials in db_connect.py before running.
