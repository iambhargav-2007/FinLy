import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

async def verify():
    load_dotenv()
    uri = os.getenv("MONGO_URI")
    print(f"Checking URI: {uri[:20]}... (hidden)" if uri else "❌ MONGO_URI is missing")
    
    if not uri:
        return

    try:
        client = AsyncIOMotorClient(uri, serverSelectionTimeoutMS=5000)
        # Force a connection verification
        await client.admin.command('ping')
        print("\n✅ SUCCESS: Connected to MongoDB Atlas!")
    except Exception as e:
        print(f"\n❌ CONNECTION FAILED: {str(e)}")

if __name__ == "__main__":
    asyncio.run(verify())
