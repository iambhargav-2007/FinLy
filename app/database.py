# app/database.py

import os
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = None
db = None

def get_db():
    global client, db
    if db is None:
        if not MONGO_URI:
            print("⚠️ MONGO_URI not set. Database disabled.")
            return None
        try:
            client = AsyncIOMotorClient(MONGO_URI, serverSelectionTimeoutMS=5000)
            db = client.get_database() # Uses database from URI if present, or default
            print("✅ Connected to MongoDB")
        except Exception as e:
            print(f"❌ Database Connection Failed: {e}")
            return None
    return db

async def save_analysis_result(data: dict) -> bool:
    """
    Saves analysis result to MongoDB, falling back to local JSON if DB is unavailable.
    """
    database = get_db()
    
    # Add timestamp
    data["created_at"] = datetime.utcnow().isoformat()

    # Strategy 1: MongoDB
    if database is not None:
        try:
            result = await database["analysis_history"].insert_one(data)
            print(f"💾 Analysis saved to MongoDB with ID: {result.inserted_id}")
            return True
        except Exception as e:
            print(f"⚠️ MongoDB save failed: {e}. Switching to local backup...")

    # Strategy 2: Local JSON Fallback
    try:
        import json
        file_path = "history.json"
        
        # Read existing
        history = []
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                try:
                    history = json.load(f)
                except json.JSONDecodeError:
                    pass # Start fresh if corrupt
        
        # Append & Save
        history.append(data)
        with open(file_path, "w") as f:
            json.dump(history, f, indent=2, default=str)
        
        print(f"💾 Analysis saved locally to {file_path}")
        return True
    except Exception as e:
        print(f"❌ Failed to save locally: {e}")
        return False
