from pymongo import MongoClient
from backend.config import MONGO_URI, DB_NAME

# Connect to MongoDB Atlas
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
