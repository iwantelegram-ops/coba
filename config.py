from dotenv import load_dotenv
import os

load_dotenv()

# Telegram
API_ID = int(os.getenv("API_ID", 0))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# MongoDB
MONGO_URI = os.getenv("MONGO_URI", "")

# Owner Bot
OWNER_ID = int(os.getenv("OWNER_ID", 0))

# Channel Utama
MAIN_CHANNEL_ID = int(os.getenv("MAIN_CHANNEL_ID", 0))
MAIN_CHANNEL_USERNAME = os.getenv("MAIN_CHANNEL_USERNAME", "")

# Nama Database
DATABASE_NAME = "partner_hub"

# Pagination
CHANNELS_PER_PAGE = 15

# Status
ACTIVE = "active"
PAUSED = "paused"

# Mono ID Prefix
MONO_PREFIX = "MONO"
CHANNEL_PREFIX = "CH"

# Timezone
TIMEZONE = "Asia/Jakarta"
