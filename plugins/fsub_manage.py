from pyrogram import Client, filters
from pyrogram.types import Message
from helper.database import MongoDB
from config import ADMINS

db = MongoDB()

@Client.on_message(filters.command("add_fsub") & filters.user(ADMINS))
async def add_fsub_cmd(client, message: Message):
    await message.reply("Forward a message from the channel you want to add.")

@Client.on_message(filters.forwarded & filters.user(ADMINS))
async def save_fsub_channel(client, message: Message):
    if not message.forward_from_chat:
        return
    
    channel = message.forward_from_chat
    channel_id = channel.id
    channel_username = channel.username

    data = await db.get_fsub_channels()
    data[str(channel_id)] = {
        "username": channel_username,
        "title": channel.title
    }

    await db.set_fsub_channels(data)

    await message.reply(f"✅ Added FSUB Channel:\n{channel.title}")
