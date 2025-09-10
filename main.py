import logging
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)
from flask import Flask

# Flask app for Render health check
app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "✅ Candy Play Bot is Live!"

# Telegram bot token
BOT_TOKEN = "7999216513:AAEITyORi5Hr6Iwp3ytkRxLx-4MHwn3JBug"

# Enable logging for debugging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[
        InlineKeyboardButton("▶ Play Candy Play", url="https://candy-play.onrender.com")
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"🍭 Welcome {update.effective_user.first_name}!\n"
        "🎮 Click below to start playing 👇",
        reply_markup=reply_markup
    )

# /play command handler
async def play(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎮 Game started! Collect candies and earn points!")

async def main():
    # Build Telegram app
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("play", play))

    # Start polling Telegram for updates
    print("🚀 Candy Play Bot is running...")
    await application.run_polling()

if __name__ == "__main__":
    # Start Telegram bot in background
    import threading
    threading.Thread(target=lambda: os.system("python3 main.py run_bot"), daemon=True).start()

    # Start Flask for Render health check
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
