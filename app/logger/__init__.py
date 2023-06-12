import os
from dotenv import load_dotenv
import datetime
import motor.motor_asyncio

load_dotenv('configurations/main.env')

class Logger:
    
    uri = os.getenv('MONGO_URL')
    db_name = 'logger'
    client = motor.motor_asyncio.AsyncIOMotorClient(uri)
    db = client[db_name]
    
    
    def __init__(self, collection_name):
        self.collection = self.db[collection_name]
    
    async def log(log_type: str, *args):
        message = ' '.join(str(arg) for arg in args)
        log = {            
            'message': message,
            'timestamp': datetime.datetime.utcnow()
        }
        await Logger.db[log_type].insert_one(log)
    
        