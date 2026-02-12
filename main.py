import asyncio
from bot import Bot, web_app
from pyrogram import compose
from config import *

async def main():
    apps = []

    # 🔥 Create bot instance
    bot = Bot(
        SESSION,
        WORKERS,
        DB_CHANNEL,
        FSUBS,
        TOKEN,
        ADMINS,
        MESSAGES,
        AUTO_DEL,
        DB_URI,
        DB_NAME,
        API_ID,
        API_HASH,
        PROTECT,
        DISABLE_BTN
    )

    apps.append(bot)

    # Start all clients
    await compose(apps)

    # 🔥 LOAD FSUB CHANNELS FROM DATABASE AFTER START
    bot.fsub_dict = {}
    bot.req_channels = []

    fsub_data = await bot.mongodb.get_fsub_channels()

    for ch_id, data in fsub_data.items():
        bot.fsub_dict[int(ch_id)] = data
        if data[2]:  # if request enabled
            bot.req_channels.append(int(ch_id))

    print("✅ Force Sub Channels Loaded:", bot.fsub_dict)


async def runner():
    await asyncio.gather(
        main(),
        web_app()
    )

if __name__ == "__main__":
    asyncio.run(runner())
