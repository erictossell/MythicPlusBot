import os
from dotenv import load_dotenv
import datetime
import motor.motor_asyncio

load_dotenv()


class Logger:
    uri = os.getenv("MONGO_URL")
    db_name = "logger"
    client = motor.motor_asyncio.AsyncIOMotorClient(uri)
    db = client[db_name]

    def __init__(self, collection_name):
        self.collection = self.db[collection_name]

    async def log(self, log):
        await self.db["python_logs"].insert_one(log)

    async def build_item_log(self, log_type, item, message):
        log = {
            "log_type": log_type,
            "item_id": item.id,
            "item_type": item.__class__.__name__,
            "message": message,
            "timestamp": datetime.datetime.utcnow(),
        }
        await self.log(self, log)

    async def build_manual_log(self, log_type, item_type, message):
        log = {
            "log_type": log_type,
            "item_type": item_type,
            "message": message,
            "timestamp": datetime.datetime.utcnow(),
        }
        await self.log(self, log)

    async def check_previous_errors(self, item, threshold=5):
        query = {
            "log_type": "error",
            "item_id": item.id,
            "item_type": item.__class__.__name__,
            "message": f"RadierIO API Error: Character is not found. {item.name} : 400",
        }
        count = await self.db["python_logs"].count_documents(query)
        return count >= threshold
