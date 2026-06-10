from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI, DATABASE_NAME


class MongoDB:

    def __init__(self):
        self.client = AsyncIOMotorClient(MONGO_URI)
        self.db = self.client[DATABASE_NAME]

        self.users = self.db.users
        self.channels = self.db.channels
        self.posts = self.db.posts
        self.logs = self.db.logs
        self.settings = self.db.settings

    async def create_indexes(self):

        await self.users.create_index(
            "user_id",
            unique=True
        )

        await self.channels.create_index(
            "channel_id",
            unique=True
        )

        await self.channels.create_index(
            "unique_id",
            unique=True
        )

        await self.posts.create_index(
            "mono_id",
            unique=True
        )

        await self.posts.create_index(
            "partner_message_id"
        )

        await self.posts.create_index(
            "main_message_id"
        )

        print("MongoDB indexes loaded")


mongo = MongoDB()
