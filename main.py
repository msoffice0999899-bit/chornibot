import os
import logging
import telebot

# Logging setup taaki logs clear dikhein
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Railway ke environment variables read karna
BOT_TOKEN = os.getenv("BOT_TOKEN")
TARGET_CHAT_ID = os.getenv("TARGET_CHAT_ID")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))

if not BOT_TOKEN:
    logging.error("BOT_TOKEN missing! Please set BOT_TOKEN in Railway Variables.")
    exit(1)

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(func=lambda message: True, content_types=[
    'text', 'photo', 'video', 'document', 'audio', 
    'voice', 'sticker', 'video_note', 'animation'
])
def process_message(message):
    # Check: message private chat me ho aur OWNER ne bheja ho
    is_private = message.chat.type == "private"
    is_owner = message.from_user and message.from_user.id == OWNER_ID

    if is_private and is_owner:
        try:
            bot.copy_message(
                chat_id=TARGET_CHAT_ID,
                from_chat_id=message.chat.id,
                message_id=message.message_id
            )
            logging.info(f"Successfully copied message {message.message_id} to {TARGET_CHAT_ID}")
        except Exception as e:
            logging.error(f"Failed to copy message {message.message_id}: {e}")

if __name__ == "__main__":
    logging.info("Telegram Copy Bot started listening...")
    bot.infinity_polling(skip_pending=True)
