import streamlit as st
import requests

st.set_page_config(page_title="Travel Planner MVP", layout="centered")

st.title("✈️ Travel Planner MVP")

source = st.text_input("Source City", "Chennai")
destination = st.text_input("Destination City", "Bangalore")
days = st.number_input("Number of Days", min_value=1, max_value=30, value=3)
budget = st.number_input("Budget (INR)", min_value=1000, value=20000)

if st.button("Plan My Trip"):
    payload = {
        "source": source,
        "destination": destination,
        "days": days,
        "budget": budget
    }
    try:
        res = requests.post("http://127.0.0.1:8000/plan_trip", json=payload)
        if res.status_code == 200:
            data = res.json()
            st.subheader("📅 Itinerary")
            for day in data["itinerary_summary"]:   # FIXED KEY
                st.write(f"**Day {day['day']}** → {day['plan']}")
            st.write(f"💰 Total Cost: ₹{data['total_cost']}")
            st.write(f"✅ Within Budget: {data['within_budget']}")
        else:
            st.error("Failed to fetch plan. Backend not running?")
    except Exception as e:
        st.error(f"Error: {e}")
