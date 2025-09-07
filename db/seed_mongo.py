"""
Run: python seed_mongo.py
This inserts sample documents (5-8 per collection). Adjust or expand as needed.
"""
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME", "travel_planner")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

# drop old collections (for quick re-seed; optional)
db.flights.drop()
db.hotels.drop()
db.transfers.drop()
db.events.drop()

flights = [
    {"flight_id": 1, "airline": "IndiGo", "source": "Chennai", "destination": "Bangalore", "price": 5000, "time": "10:00 AM"},
    {"flight_id": 2, "airline": "Air India", "source": "Chennai", "destination": "Bangalore", "price": 5500, "time": "2:00 PM"},
    {"flight_id": 3, "airline": "SpiceJet", "source": "Chennai", "destination": "Bangalore", "price": 4800, "time": "6:00 AM"},
    {"flight_id": 4, "airline": "Vistara", "source": "Chennai", "destination": "Bangalore", "price": 6200, "time": "9:00 PM"},
    {"flight_id": 5, "airline": "IndiGo", "source": "Chennai", "destination": "Hyderabad", "price": 4500, "time": "11:00 AM"},
]

hotels = [
    {"hotel_id": 1, "city": "Bangalore", "name": "Ibis", "price_per_night": 3000, "rating": 4.0},
    {"hotel_id": 2, "city": "Bangalore", "name": "The Park", "price_per_night": 4000, "rating": 4.3},
    {"hotel_id": 3, "city": "Bangalore", "name": "Budget Lodge", "price_per_night": 1800, "rating": 3.2},
    {"hotel_id": 4, "city": "Bangalore", "name": "Prestige Inn", "price_per_night": 3500, "rating": 4.1},
    {"hotel_id": 5, "city": "Bangalore", "name": "Luxury Suites", "price_per_night": 7000, "rating": 4.8},
]

transfers = [
    {"transfer_id": 1, "city": "Bangalore", "type": "cab", "price": 1000},
    {"transfer_id": 2, "city": "Bangalore", "type": "shuttle", "price": 500},
    {"transfer_id": 3, "city": "Bangalore", "type": "private_car", "price": 2500},
    {"transfer_id": 4, "city": "Bangalore", "type": "metro_pass", "price": 300},
]

events = [
    {"event_id": 1, "city": "Bangalore", "name": "City Tour", "price": 2000, "day": 2},
    {"event_id": 2, "city": "Bangalore", "name": "Lalbagh Visit", "price": 500, "day": 1},
    {"event_id": 3, "city": "Bangalore", "name": "Museum Tour", "price": 700, "day": 2},
    {"event_id": 4, "city": "Bangalore", "name": "Shopping Circuit", "price": 1500, "day": 3},
    {"event_id": 5, "city": "Bangalore", "name": "Food Walk", "price": 800, "day": 1},
]

db.flights.insert_many(flights)
db.hotels.insert_many(hotels)
db.transfers.insert_many(transfers)
db.events.insert_many(events)

print("Inserted sample documents into MongoDB.")
