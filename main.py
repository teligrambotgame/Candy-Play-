import os
from flask import Flask, request
import requests

app = Flask(__name__)

# Telegram Bot Token
BOT_TOKEN = "7999216513:AAEITyORi5Hr6Iwp3ytkRxLx-4MHwn3JBug"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

# Home route to check server status
@app.route("/", methods=["GET"])
def home():
    return "✅ Candy Play Bot is Live!"

# Webhook route
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if data and "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        # If user sends /start command
        if text.lower() == "/start":
            reply = "🍭 Welcome to Candy Play!\nClick below to play 👇"
            play_button = {
                "inline_keyboard": [[{
                    "text": "▶ Play Candy Play",
                    "url": "https://candy-play.onrender.com"
                }]]
            }
            send_message(chat_id, reply, play_button)

        # If user sends /play command
        elif text.lower() == "/play":
            send_message(chat_id, "🎮 Game started! Collect candies and earn points!")

        # For other messages
        else:
            send_message(chat_id, f"You said: {text}")

    return {"ok": True}

# Function to send message
def send_message(chat_id, text, reply_markup=None):
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup
    requests.post(url, json=payload)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
