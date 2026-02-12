from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from helper.helper_func import is_bot_admin
import random

MAX_CHANNELS = 5  # Only 5 channels per user

# =============================================================== #

async def get_random_fsub_channels(client, user_id: int):
    all_channels = list(client.fsub_dict.keys())

    if not all_channels:
        return []

    user_status = await client.mongodb.get_user_fsub_statuses(user_id)

    not_joined = [
        ch for ch in all_channels
        if user_status.get(ch) != "joined"
    ]

    if len(not_joined) <= MAX_CHANNELS:
        return not_joined

    return random.sample(not_joined, MAX_CHANNELS)

# =============================================================== #

async def check_force_sub(client, user_id: int):
    required_channels = await get_random_fsub_channels(client, user_id)

    if not required_channels:
        return True

    buttons = []

    for channel_id in required_channels:
        try:
            member = await client.get_chat_member(channel_id, user_id)

            if member.status in ["member", "administrator", "creator"]:
                await client.mongodb.update_fsub_status(user_id, channel_id, "joined")
                continue

            # Create fresh invite link (works for private/public)
            invite = await client.create_chat_invite_link(channel_id)
            link = invite.invite_link

            buttons.append([
                InlineKeyboardButton("Join Channel", url=link)
            ])

        except:
            continue

    if not buttons:
        return True

    buttons.append([
        InlineKeyboardButton("🔄 Try Again", callback_data="recheck_fsub")
    ])

    return InlineKeyboardMarkup(buttons)

# =============================================================== #

@Client.on_callback_query(filters.regex("^recheck_fsub$"))
async def recheck_fsub(client: Client, query: CallbackQuery):
    user_id = query.from_user.id

    required_channels = await get_random_fsub_channels(client, user_id)

    all_joined = True

    for channel_id in required_channels:
        try:
            member = await client.get_chat_member(channel_id, user_id)

            if member.status in ["member", "administrator", "creator"]:
                await client.mongodb.update_fsub_status(user_id, channel_id, "joined")
            else:
                all_joined = False

        except:
            all_joined = False

    if all_joined:
        await query.message.edit_text("✅ All required channels joined successfully!")
    else:
        markup = await check_force_sub(client, user_id)
        await query.message.edit_reply_markup(markup)

# =============================================================== #
# ADMIN SIDE
# =============================================================== #

@Client.on_callback_query(filters.regex('^add_fsub$'))
async def add_fsub(client: Client, query: CallbackQuery):
    await query.answer()

    ask = await client.ask(
        query.from_user.id,
        "Send channel id (example: -1001234567890)",
        timeout=60
    )

    try:
        channel_id = int(ask.text)

        if channel_id in client.fsub_dict:
            return await ask.reply("Channel already exists.")

        val, res = await is_bot_admin(client, channel_id)
        if not val:
            return await ask.reply(f"Error: {res}")

        chat = await client.get_chat(channel_id)

        client.fsub_dict[channel_id] = [chat.title]

        await client.mongodb.add_fsub_channel(channel_id, [chat.title])

        await ask.reply(f"✅ Added: {chat.title}")

    except Exception as e:
        await ask.reply(f"Error: {e}")

# =============================================================== #

@Client.on_callback_query(filters.regex('^rm_fsub$'))
async def rm_fsub(client: Client, query: CallbackQuery):
    await query.answer()

    ask = await client.ask(
        query.from_user.id,
        "Send channel id to remove:",
        timeout=60
    )

    try:
        channel_id = int(ask.text)

        if channel_id not in client.fsub_dict:
            return await ask.reply("Channel not found.")

        client.fsub_dict.pop(channel_id)

        await client.mongodb.remove_fsub_channel(channel_id)

        await ask.reply("✅ Removed successfully.")

    except Exception as e:
        await ask.reply(f"Error: {e}")
