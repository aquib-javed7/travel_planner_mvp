# ✈️ Travel Planner MVP

An end-to-end travel planner using **FastAPI + Streamlit + MongoDB + Llama**.

---

## 1. Setup MongoDB Atlas

1. Create a free MongoDB Atlas cluster.
2. Create a database named `travel_planner`.
3. Create collections: `flights`, `hotels`, `transfers`, `events`.
4. Insert sample data by running:
   ```bash
   python db/seed_mongo.py
   ```

---

## 2. Configure Environment

Copy `.env.example` to `.env` and update values:

```env
MONGO_URI="your_mongodb_connection_string"
DB_NAME="travel_planner"
LLAMA_GGUF_PATH="/path/to/your/local/model.gguf"
PORT=8000
```

---

## 3. (Optional) Fine-Tune Model

If you want the LLM to follow your dataset style more closely:

1. Prepare training data (`llm/train.jsonl`) like:

```json
{"instruction": "Plan a 3-day trip from Chennai to Bangalore under ₹20,000",
 "input": "Flights: Indigo 5000 INR; Hotels: Ibis 3000 INR/night; Events: Lalbagh 500 INR",
 "output": "Day 1: Fly Chennai → Bangalore, check in at Ibis, evening Lalbagh visit. Day 2: City Tour. Day 3: Shopping + return flight."}
```

2. Run fine-tuning script (see `llm/fine_tune_notes.md`).

*(You can skip this step; the system works without fine-tuning.)*

---

## 4. Run FastAPI Backend

```bash
cd backend
uvicorn app:app --reload --port 8000
```

Backend available at → `http://127.0.0.1:8000/docs`

---

## 5. Run Streamlit Frontend

```bash
cd frontend
python -m streamlit run app.py
```

Frontend available at → `http://127.0.0.1:8501`

---

## 6. Example Input/Output

**Input:**
```json
{
  "source": "Chennai",
  "destination": "Bangalore",
  "days": 3,
  "budget": 20000
}
```

**Output:**
```json
{
  "itinerary_summary": [
    {"day": 1, "plan": "Flight Chennai → Bangalore at 6:00 AM (4800 INR)", "cost": 4800},
    {"day": 1, "plan": "Check-in at Budget Lodge (1800 INR/night, total 5400 INR)", "cost": 5400},
    {"day": 2, "plan": "Attend City Tour (2000 INR)", "cost": 2000},
    {"day": 3, "plan": "Attend Shopping Circuit (1500 INR)", "cost": 1500}
  ],
  "total_cost": 16600,
  "budget": 20000,
  "within_budget": true
}
```

---

## 📂 Project Structure

```
.
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── db_client.py
│   └── __init__.py
├── db/
│   └── seed_mongo.py
├── frontend/
│   └── app.py
├── llm/
│   ├── train.jsonl (sample)
│   └── fine_tune_notes.md
├── requirements.txt
├── .env.example
└── README.md
```
