import os
import logging
from logging.handlers import RotatingFileHandler

# ================= LOGGING =================
LOG_FILE_NAME = "bot.log"
PORT = int(os.getenv("PORT", 5010))
OWNER_ID = int(os.getenv("OWNER_ID", 6497757690))

MSG_EFFECT = 5046509860389126442

# ================= SHORTENER =================
SHORT_URL = os.getenv("SHORT_URL", "linkshortify.com")
SHORT_API = os.getenv("SHORT_API", "")
SHORT_TUT = os.getenv("SHORT_TUT", "https://t.me/How_to_Download_7x/26")

# ================= TELEGRAM =================
SESSION = os.getenv("SESSION", "yato")
TOKEN = os.getenv("BOT_TOKEN")
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
WORKERS = int(os.getenv("WORKERS", 5))

# ================= DATABASE =================
DB_URI = os.getenv("DB_URI")
DB_NAME = os.getenv("DB_NAME", "yato")

# Force Subscribe Channels
# format: [channel_id, request_enabled, timer_minutes]
FSUBS = [[-1002517849305, True, 10]]

# ✅ FIXED — NO EMPTY VALUE
DB_CHANNEL = int(os.getenv("DB_CHANNEL"))

# Auto delete (seconds)
AUTO_DEL = int(os.getenv("AUTO_DEL", 300))

# Admins
ADMINS = list(map(int, os.getenv("ADMINS", "").split()))

# Bot Settings
DISABLE_BTN = os.getenv("DISABLE_BTN", "False") == "True"
PROTECT = os.getenv("PROTECT", "True") == "True"

# ================= MESSAGES =================
MESSAGES = {
    "START": "<b>›› ʜᴇʏ!!, {first} ~ <blockquote>ʟᴏᴠᴇ ᴘᴏʀɴʜᴡᴀ? ɪ ᴀᴍ ᴍᴀᴅᴇ ᴛᴏ ʜᴇʟᴘ ʏᴏᴜ ᴛᴏ ғɪɴᴅ ᴡʜᴀᴛ ʏᴏᴜ ᴀʀᴇ ʟᴏᴏᴋɪɴɢ ꜰᴏʀ.</blockquote></b>",
    "FSUB": "<b><blockquote>›› ʜᴇʏ ×</blockquote>\n  ʏᴏᴜʀ ғɪʟᴇ ɪs ʀᴇᴀᴅʏ ‼️ ʟᴏᴏᴋs ʟɪᴋᴇ ʏᴏᴜ ʜᴀᴠᴇɴ'ᴛ sᴜʙsᴄʀɪʙᴇᴅ ᴛᴏ ᴏᴜʀ ᴄʜᴀɴɴᴇʟs ʏᴇᴛ</b>",
    "ABOUT": "<b>›› ᴅᴇᴠᴇʟᴏᴘᴇʀ: @cosmic_freak</b>",
    "REPLY": "<b>For More Join - @Hanime_Arena</b>",
    "SHORT_MSG": "<b>📊 ʜᴇʏ {first}, ʏᴏᴜʀ ʟɪɴᴋ ɪꜱ ʀᴇᴀᴅʏ</b>",
    "START_PHOTO": "https://graph.org/file/510affa3d4b6c911c12e3.jpg",
    "FSUB_PHOTO": "https://telegra.ph/file/7a16ef7abae23bd238c82-b8fbdcb05422d71974.jpg",
    "SHORT_PIC": "https://telegra.ph/file/7a16ef7abae23bd238c82-b8fbdcb05422d71974.jpg",
    "SHORT": "https://telegra.ph/file/8aaf4df8c138c6685dcee-05d3b183d4978ec347.jpg"
}

# ================= LOGGER =================
def LOGGER(name: str, client_name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    formatter = logging.Formatter(
        f"[%(asctime)s - %(levelname)s] - {client_name} - %(name)s - %(message)s",
        datefmt="%d-%b-%y %H:%M:%S",
    )

    file_handler = RotatingFileHandler(
        LOG_FILE_NAME, maxBytes=50_000_000, backupCount=10
    )
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger
