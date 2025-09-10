from flask import Flask, request
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Dispatcher
import logging
import os

# ------------------------------
# Logging setup
# ------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ------------------------------
# Flask app setup
# ------------------------------
app = Flask(__name__)

# ------------------------------
# Bot token from environment
# ------------------------------
BOT_TOKEN = os.getenv("BOT_TOKEN", "7999216513:AAEITyORi5Hr6Iwp3ytkRxLx-4MHwn3JBug")
bot = Bot(token=BOT_TOKEN)

# ------------------------------
# Telegram webhook route
# ------------------------------
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        update = Update.de_json(request.get_json(force=True), bot)
        handle_update(update)
    except Exception as e:
        logger.error(f"Webhook error: {e}")
    return "ok"

# ------------------------------
# Handle incoming messages
# ------------------------------
def handle_update(update):
    try:
        if update.message:
            chat_id = update.message.chat.id
            text = update.message.text or ""

            if text.lower() == "/start":
                keyboard = [[InlineKeyboardButton("▶ Play Candy Play", url="https://candy-play.onrender.com")]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                bot.send_message(
                    chat_id=chat_id,
                    text=(
                        f"🍭 Welcome {update.effective_user.first_name}!\n"
                        f"🎮 Level: 1\n"
                        f"⭐ Score: 0\n\n"
                        f"Click below to start playing 👇"
                    ),
                    reply_markup=reply_markup
                )

            elif text.lower() == "/play":
                bot.send_message(chat_id=chat_id, text="🎮 Game started! Collect candies and earn points!")

            else:
                bot.send_message(chat_id=chat_id, text=f"You said: {text}")

    except Exception as e:
        logger.error(f"handle_update error: {e}")

# ------------------------------
# Home route
# ------------------------------
@app.route('/')
def home():
    return "Candy Play Telegram Bot is running!"

# ------------------------------
# Run locally
# ------------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
