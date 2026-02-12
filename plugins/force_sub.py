from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
import random

MAX_CHANNELS = 5  # 👈 Only 5 channels per user

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

            # Always create fresh invite link
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
