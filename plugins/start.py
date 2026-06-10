from pyrogram import filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from config import (
    OWNER_ID,
    MAIN_CHANNEL_ID,
    MAIN_CHANNEL_USERNAME
)

from database import mongo

from app import bot


async def is_joined(client, user_id):

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


@bot.app.on_message(filters.private & filters.command("start"))
async def start_command(client, message):

    user = message.from_user

    user_data = {
        "user_id": user.id,
        "name": user.first_name,
        "username": user.username,
    }

    await mongo.users.update_one(
        {"user_id": user.id},
        {"$set": user_data},
        upsert=True
    )

    # OWNER
    if user.id == OWNER_ID:

        owner_text = f"""
👑 Owner Control Panel

Selamat datang {user.first_name}

Bot Partner Hub aktif.

Perintah Owner:

/pause ID alasan
/run ID alasan

Fitur:

• Statistik seluruh channel
• Kontrol partner channel
• Moderasi channel
• Monitoring repost
• Monitoring database

Status:
✅ Online
"""

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📊 Statistik",
                        callback_data="owner_stats"
                    )
                ]
            ]
        )

        return await message.reply_text(
            owner_text,
            reply_markup=keyboard
        )

    # FORCE JOIN
    joined = await is_joined(
        client,
        user.id
    )

    if not joined:

        text = f"""
👋 Selamat Datang

Bot ini digunakan untuk menghubungkan
channel partner ke channel utama.

Sebelum menggunakan bot:

1. Join channel utama
2. Klik tombol cek join

Setelah bergabung,
fitur bot akan terbuka.
"""

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📢 Join Channel",
                        url=f"https://t.me/{MAIN_CHANNEL_USERNAME}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "✅ Saya Sudah Join",
                        callback_data="check_join"
                    )
                ]
            ]
        )

        return await message.reply_text(
            text,
            reply_markup=keyboard
        )

    text = f"""
🎉 Selamat Datang

Anda sudah terverifikasi.

Bot ini memungkinkan channel Anda
menjadi Partner Channel.

Cara Menambahkan Channel:

1. Tambahkan bot sebagai admin
2. Beri izin posting
3. Beri izin hapus pesan
4. Channel akan terdeteksi otomatis

Fitur:

✅ Repost otomatis
✅ Sinkronisasi partner
✅ Kontrol channel
✅ Statistik channel
✅ MongoDB Cloud Storage
"""

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "📁 My Channel",
                    callback_data="my_channels"
                )
            ],
            [
                InlineKeyboardButton(
                    "➕ Tambahkan Bot",
                    url=f"https://t.me/{client.me.username}?startgroup=true"
                )
            ]
        ]
    )

    await message.reply_text(
        text,
        reply_markup=keyboard
    )
