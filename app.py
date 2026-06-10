import asyncio
from pyrogram import Client
from config import (
    API_ID,
    API_HASH,
    BOT_TOKEN
)
from database import mongo


class PartnerHubBot:

    def __init__(self):

        self.app = Client(
            "PartnerHubBot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=100
        )

    async def startup(self):

        print("=" * 50)
        print("Partner Hub Bot Starting...")
        print("=" * 50)

        await mongo.create_indexes()

        print("MongoDB Connected")
        print("Bot Ready")

    def run(self):

        self.app.start()

        self.app.loop.run_until_complete(
            self.startup()
        )

        print("Bot Online")

        self.app.idle()

        self.app.stop()


bot = PartnerHubBot()

if __name__ == "__main__":
    bot.run()
