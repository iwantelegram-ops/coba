from pyrogram import filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from config import (
    OWNER_ID,
    MAIN_CHANNEL_ID,
    CHANNELS_PER_PAGE
)

from database import mongo
from app import bot


async def check_membership(client, user_id):

    try:
        member = await client.get_chat_member(
            MAIN_CHANNEL_ID,
            user_id
        )

        if member:
            return True

    except:
        pass

    return False


@bot.app.on_callback_query()
async def callback_handler(client, callback):

    data = callback.data
    user_id = callback.from_user.id

    # =====================
    # CHECK JOIN
    # =====================

    if data == "check_join":

        joined = await check_membership(
            client,
            user_id
        )

        if not joined:

            return await callback.answer(
                "Anda belum join channel utama",
                show_alert=True
            )

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📁 My Channel",
                        callback_data="my_channels"
                    )
                ]
            ]
        )

        await callback.message.edit_text(
            """
✅ Verifikasi Berhasil

Anda sudah bergabung
ke channel utama.

Sekarang Anda dapat:

• Menambahkan bot ke channel
• Mengelola partner channel
• Mengaktifkan / menghentikan forwarding
            """,
            reply_markup=keyboard
        )

        return

    # =====================
    # MY CHANNELS
    # =====================

    if data == "my_channels":

        channels = []

        async for item in mongo.channels.find(
            {
                "owner_id": user_id
            }
        ):
            channels.append(item)

        if not channels:

            return await callback.answer(
                "Belum ada channel",
                show_alert=True
            )

        text = "📁 Channel Anda\n\n"

        keyboard = []

        for channel in channels[:10]:

            status = channel.get(
                "status",
                "active"
            )

            icon = (
                "🟢"
                if status == "active"
                else "⏸"
            )

            text += (
                f"{icon} "
                f"{channel['title']}\n"
                f"ID : {channel['unique_id']}\n\n"
            )

            keyboard.append(
                [
                    InlineKeyboardButton(
                        f"{channel['title'][:25]}",
                        callback_data=f"channel_{channel['unique_id']}"
                    )
                ]
            )

        await callback.message.edit_text(
            text,
            reply_markup=InlineKeyboardMarkup(
                keyboard
            )
        )

        return

    # =====================
    # DETAIL CHANNEL
    # =====================

    if data.startswith("channel_"):

        unique_id = data.split("_")[1]

        channel = await mongo.channels.find_one(
            {
                "unique_id": unique_id
            }
        )

        if not channel:
            return

        status = channel.get(
            "status",
            "active"
        )

        text = f"""
📢 {channel['title']}

🆔 {channel['unique_id']}

Status :
{status.upper()}

Owner :
{callback.from_user.first_name}
"""

        if status == "active":

            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "⏸ Pause",
                            callback_data=f"userpause_{unique_id}"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "⬅ Kembali",
                            callback_data="my_channels"
                        )
                    ]
                ]
            )

        else:

            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "▶ Continue",
                            callback_data=f"userrun_{unique_id}"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "⬅ Kembali",
                            callback_data="my_channels"
                        )
                    ]
                ]
            )

        await callback.message.edit_text(
            text,
            reply_markup=keyboard
        )

        return

    # =====================
    # USER PAUSE
    # =====================

    if data.startswith("userpause_"):

        unique_id = data.replace(
            "userpause_",
            ""
        )

        await mongo.channels.update_one(
            {
                "unique_id": unique_id
            },
            {
                "$set": {
                    "status": "paused"
                }
            }
        )

        await callback.answer(
            "Channel dipause"
        )

        return

    # =====================
    # USER RUN
    # =====================

    if data.startswith("userrun_"):

        unique_id = data.replace(
            "userrun_",
            ""
        )

        await mongo.channels.update_one(
            {
                "unique_id": unique_id
            },
            {
                "$set": {
                    "status": "active"
                }
            }
        )

        await callback.answer(
            "Channel diaktifkan"
        )

        return

    # =====================
    # OWNER STATS
    # =====================

    if data == "owner_stats":

        if user_id != OWNER_ID:
            return

        total_users = await mongo.users.count_documents(
            {}
        )

        total_channels = await mongo.channels.count_documents(
            {}
        )

        total_posts = await mongo.posts.count_documents(
            {}
        )

        active_channels = await mongo.channels.count_documents(
            {
                "status": "active"
            }
        )

        paused_channels = await mongo.channels.count_documents(
            {
                "status": "paused"
            }
        )

        text = f"""
📊 Statistik Bot

👥 User :
{total_users}

📢 Channel :
{total_channels}

🟢 Active :
{active_channels}

⏸ Paused :
{paused_channels}

📝 Repost :
{total_posts}
"""

        await callback.message.edit_text(
            text
        )

        return
