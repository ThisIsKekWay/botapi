import motor.motor_asyncio as mt
from config import settings

client = mt.AsyncIOMotorClient(settings.MONGO_HOST)
db = client["messages"]


class MessageDAO:
    def __init__(self, database):
        self.collection = database['msg']

    async def insert(self, data):
        await self.collection.insert_one(data)

    async def get_msg_with_pagination(self, page, page_size):
        skip = (page - 1) * page_size
        cursor = self.collection.find().skip(skip).limit(page_size)
        msgs = await cursor.to_list(length=page_size)
        msgs.insert(0, {"page": page})
        return msgs
