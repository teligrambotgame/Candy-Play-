# ================= Candy Play Main.py =================
from flask import Flask, render_template, request, jsonify
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update
import os
import threading
import sqlite3

# ---------------- Flask app initialize ----------------
app = Flask(__name__)

# ---------------- Telegram Bot Token ----------------
BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
BOT_USERNAME = "candyplay_bot"  # Apna bot username

# ---------------- Database setup ----------------
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

# ---------------- User database functions ----------------
def save_user(user_id, username):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)", (user_id, username))
    conn.commit()
    conn.close()

def get_score(user_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT score FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0

def get_level(user_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT level FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 1

# ---------------- Telegram Bot handle_update ----------------
def handle_update(update, bot: Bot):
    """
    Handles incoming Telegram messages for Candy Play.
    """
    try:
        chat_id = update.message.chat.id
        text = update.message.text

        if text.lower() == "/start":
            save_user(chat_id, update.effective_user.username or "Unknown")
            keyboard = [[InlineKeyboardButton("▶ Play Candy Play", url="https://candy-play.onrender.com")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            bot.send_message(
                chat_id=chat_id,
                text=f"🍭 Welcome {update.effective_user.first_name}!\n"
                     f"🎮 Level: {get_level(chat_id)}\n"
                     f"⭐ Score: {get_score(chat_id)}\n\nClick below to start playing 👇",
                reply_markup=reply_markup
            )
        elif text.lower() == "/play":
            bot.send_message(chat_id=chat_id, text="Game started! Collect candies and earn points!")
        else:
            bot.send_message(chat_id=chat_id, text=f"You said: {text}")
    except Exception as e:
        print(f"handle_update error: {e}")

# ---------------- Flask route for game ----------------
@app.route("/")
def index():
    return render_template("index.html")

# ---------------- Update progress route ----------------
@app.route("/update_progress", methods=["POST"])
def update_progress():
    data = request.get_json()
    user_id = data["user_id"]
    added_score = data["score"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT score, level FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    if result:
        current_score, current_level = result
        new_score = current_score + added_score
        new_level = min(100, 1 + new_score // 500)
        cursor.execute("UPDATE users SET score = ?, level = ? WHERE user_id = ?", (new_score, new_level, user_id))
        conn.commit()
    conn.close()
    return jsonify({"success": True})

# ---------------- Flask webhook route ----------------
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        update = Update.de_json(request.get_json(force=True), bot)
        threading.Thread(target=handle_update, args=(update, bot)).start()
        return "ok"
    except Exception as e:
        print(f"Webhook Error: {e}")
        return "error"

# ---------------- Run Flask app ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
