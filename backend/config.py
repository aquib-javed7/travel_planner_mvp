import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# MongoDB configuration
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "travel_planner")

# FastAPI port
PORT = int(os.getenv("PORT", 8000))

# Local Llama GGUF model path
LLAMA_GGUF_PATH = os.getenv(
    "LLAMA_GGUF_PATH",
    r"D:\Projects\Travel Planner MVP\models\Llama-3.1-8B-Instruct-travelplanner-SFT.i1-Q4_K_M.gguf"
)
