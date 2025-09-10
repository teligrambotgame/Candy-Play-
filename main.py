from flask import Flask, render_template, request, jsonify
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os
import threading
import sqlite3

# Flask app initialize
app = Flask(__name__)

# Telegram Bot Token
BOT_TOKEN = os.environ.get("BOT_TOKAN")
BOT_USERNAME = "candyplay_bot"  # Apna bot username yaha dalna

# Database setup
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            score INTEGER DEFAULT 0,
            level INTEGER DEFAULT 1
        )
    """)
    conn.commit()
    conn.close()

init_db()

# Telegram Bot Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    save_user(user.id, user.username)

    keyboard = [[
        InlineKeyboardButton("▶ Play Candy Play", url="https://candy-play.onrender.com")
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"🍭 Welcome {user.first_name}!\n"
        f"🎮 Your current level: {get_level(user.id)}\n"
        f"⭐ Score: {get_score(user.id)}\n\n"
        "Click below to start playing 👇",
        reply_markup=reply_markup
    )

# Save new users into database
def save_user(user_id, username):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)", (user_id, username))
    conn.commit()
    conn.close()

# Get user score
def get_score(user_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT score FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0

# Get user level
def get_level(user_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT level FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 1

# Update score & level
@app.route("/update_progress", methods=["POST"])
def update_progress():
    data = request.get_json()
    user_id = data["user_id"]
    added_score = data["score"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Update score
    cursor.execute("SELECT score, level FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    if result:
        current_score, current_level = result
        new_score = current_score + added_score
        new_level = min(100, 1 + new_score // 500)  # 500 points per level

        cursor.execute("UPDATE users SET score = ?, level = ? WHERE user_id = ?", (new_score, new_level, user_id))
        conn.commit()

    conn.close()
    return jsonify({"success": True})

# Flask route for game
@app.route("/")
def index():
    return render_template("index.html")

# Run both Flask + Telegram bot together
def run_telegram_bot():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling()

if __name__ == "__main__":
    threading.Thread(target=run_telegram_bot).start()
    app.run(host="0.0.0.0", port=5000)
# --- Add this in your main.py ---

from telegram import Bot

def handle_update(update, bot: Bot):
    """
    This function handles incoming Telegram messages for Candy Play.
    It receives 'update' from Telegram and the bot instance.
    Add your game logic inside this function.
    """

    try:
        chat_id = update.message.chat.id
        text = update.message.text

        # --- Example game logic ---
        # Replace this with your actual Candy Play commands
        if text.lower() == "/start":
            bot.send_message(chat_id=chat_id, text="Welcome to Candy Play! 🍬\nType /play to start the game.")
        elif text.lower() == "/play":
            bot.send_message(chat_id=chat_id, text="Game started! Collect candies and earn points!")
        else:
            # Echo any other message (you can replace this with actual game logic)
            bot.send_message(chat_id=chat_id, text=f"You said: {text}")

    except Exception as e:
        print(f"handle_update error: {e}")
# ================= Candy Play Telegram Bot Webhook =================
# File name: webhook.py

from flask import Flask, request
from telegram import Bot, Update
import os
import threading
import main  # tumhara existing main.py

app = Flask(__name__)

# BOT_TOKEN ko Render Environment Variables me set karo
BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        # Telegram update receive
        update = Update.de_json(request.get_json(force=True), bot)

        # Thread me existing main.py ka handle_update call karo
        threading.Thread(target=main.handle_update, args=(update, bot)).start()

        return "ok"
    except Exception as e:
        print(f"Webhook Error: {e}")
        return "error"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
