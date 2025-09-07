from fastapi import FastAPI
from pydantic import BaseModel
from backend.db_client import db
from backend.config import LLAMA_GGUF_PATH
from llama_cpp import Llama
import json

app = FastAPI(title="Travel Planner API")

# Load your local Llama model
llm = Llama(model_path=LLAMA_GGUF_PATH)

# Input model
class TripRequest(BaseModel):
    source: str
    destination: str
    days: int
    budget: int

def generate_llama_itinerary(req: TripRequest):
    # JSON-friendly prompt
    prompt = f"""
    Create a travel itinerary for {req.days} days from {req.source} to {req.destination} 
    with a budget of {req.budget} INR. 
    Output the itinerary as a JSON list of objects with keys: "day", "plan", "cost".
    Example:
    [
      {{"day": 1, "plan": "Flight Chennai → Bangalore at 10:00 AM", "cost": 5000}},
      {{"day": 1, "plan": "Check-in at Ibis", "cost": 3000}}
    ]
    """
    response = llm(prompt, max_tokens=1500)
    text = response['choices'][0]['text'].strip()

    try:
        itinerary_summary = json.loads(text)
    except json.JSONDecodeError:
        # Fallback: return empty if Llama output is not valid JSON
        itinerary_summary = []

    return itinerary_summary

@app.get("/")
def read_root():
    return {"message": "Hello"}

@app.get("/akib")
def read_root():
    return {"message": "Hello, World!"}

@app.post("/plan_trip")
def plan_trip(req: TripRequest):
    # Fetch from MongoDB
    flights = list(db.flights.find({"source": req.source, "destination": req.destination}))
    hotels = list(db.hotels.find({"city": req.destination}))
    events = list(db.events.find({"city": req.destination}))
    transfers = list(db.transfers.find({"city": req.destination}))

    itinerary_summary = []
    total_cost = 0

    # Select cheapest flight
    if flights:
        flights.sort(key=lambda x: x["price"])
        flight = flights[0]
        total_cost += flight["price"]
        itinerary_summary.append({
            "day": 1,
            "plan": f"Flight {req.source} → {req.destination} at {flight['time']} ({flight['price']} INR)",
            "cost": flight["price"]
        })

    # Select cheapest hotel
    if hotels:
        hotels.sort(key=lambda x: x["price_per_night"])
        hotel = hotels[0]
        cost = hotel["price_per_night"] * req.days
        total_cost += cost
        itinerary_summary.append({
            "day": 1,
            "plan": f"Check-in at {hotel['name']} ({hotel['price_per_night']} INR/night, total {cost} INR)",
            "cost": cost
        })

    # Add transfers (same cheapest transfer every day)
    if transfers:
        transfers.sort(key=lambda x: x["price"])
        transfer = transfers[0]
        for d in range(1, req.days + 1):
            itinerary_summary.append({
                "day": d,
                "plan": f"Use {transfer['type']} for travel ({transfer['price']} INR)",
                "cost": transfer["price"]
            })
            total_cost += transfer["price"]

    # Add events strictly grouped by day
    for d in range(1, req.days + 1):
        day_events = [e for e in events if e["day"] == d]
        for e in day_events:
            itinerary_summary.append({
                "day": d,
                "plan": f"Attend {e['name']} ({e['price']} INR)",
                "cost": e["price"]
            })
            total_cost += e["price"]

    # Fallback to Llama if MongoDB returns nothing
    if not itinerary_summary:
        itinerary_summary = generate_llama_itinerary(req)
        total_cost = sum(item.get("cost", 0) for item in itinerary_summary)

    llama_generated_itinerary = "\n".join([item['plan'] for item in itinerary_summary])

    return {
        "itinerary_summary": sorted(itinerary_summary, key=lambda x: x["day"]),  # Ensure ordered
        "total_cost": total_cost,
        "budget": req.budget,
        "within_budget": total_cost <= req.budget,
        "llama_generated_itinerary": llama_generated_itinerary
    }
