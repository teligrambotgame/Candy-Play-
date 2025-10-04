import logging
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)
from flask import Flask
import asyncio

# Flask app for Render health check
@app.route('/<7999216513:AAH3fyMOn0YkvEgEyEJiAPEZNh1z9J-E8Ro>', methods=['POST'])
def receive_update(token):
    if token == TELEGRAM_BOT_TOKEN:
        update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
        bot.process_new_updates([update])
        return "!", 200
    else:
        return "Unauthorized", 403

# Enable logging for debugging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Telegram bot token from environment
BOT_TOKEN = os.getenv("BOT_TOKEN")

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

# Telegram bot runner
async def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("play", play))

    print("✅ Telegram bot is now polling for commands...")
    await application.run_polling()

# Entry point
if __name__ == "__main__":
    # Start Telegram bot
    asyncio.run(main())

    # Start Flask app for Render health check
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
