from pyrogram import Client, filters
from pyrogram.types import Message
from config import ADMINS


# ===============================================================
# ADD FSUB COMMAND
# ===============================================================

@Client.on_message(filters.command("add_fsub") & filters.user(ADMINS))
async def add_fsub_cmd(client, message: Message):
    await message.reply(
        "📢 Please forward any message from the channel you want to add as Force Subscribe."
    )


# ===============================================================
# SAVE FORWARDED CHANNEL
# ===============================================================

@Client.on_message(filters.forwarded & filters.user(ADMINS))
async def save_fsub_channel(client, message: Message):

    if not message.forward_from_chat:
        return

    channel = message.forward_from_chat
    channel_id = channel.id
    channel_username = channel.username
    channel_title = channel.title

    # Load existing fsub channels
    data = await client.mongodb.get_fsub_channels()

    # Add / Update channel
    data[str(channel_id)] = {
        "username": channel_username,
        "title": channel_title
    }

    # Save to database
    await client.mongodb.set_fsub_channels(data)

    await message.reply(
        f"✅ Force Subscribe Channel Added Successfully!\n\n"
        f"📌 Title: {channel_title}\n"
        f"🆔 ID: `{channel_id}`"
    )
