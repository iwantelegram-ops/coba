from database import mongo
from config import CHANNEL_PREFIX, MONO_PREFIX


async def generate_channel_id():

    last_channel = await mongo.channels.find_one(
        {},
        sort=[("_id", -1)]
    )

    if not last_channel:
        return f"{CHANNEL_PREFIX}000001"

    last_id = last_channel.get(
        "unique_id",
        f"{CHANNEL_PREFIX}000000"
    )

    number = int(
        last_id.replace(CHANNEL_PREFIX, "")
    ) + 1

    return f"{CHANNEL_PREFIX}{number:06d}"


async def generate_mono_id():

    last_post = await mongo.posts.find_one(
        {},
        sort=[("_id", -1)]
    )

    if not last_post:
        return f"{MONO_PREFIX}000001"

    last_id = last_post.get(
        "mono_id",
        f"{MONO_PREFIX}000000"
    )

    number = int(
        last_id.replace(MONO_PREFIX, "")
    ) + 1

    return f"{MONO_PREFIX}{number:06d}"
