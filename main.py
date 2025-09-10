import os
from flask import Flask, request
import requests

app = Flask(__name__)

BOT_TOKEN = "7999216513:AAEITyORi5Hr6Iwp3ytkRxLx-4MHwn3JBug"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

@app.route("/", methods=["GET"])
def home():
    return "✅ Candy Play Bot is Live!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("📩 Incoming update:", data)  # DEBUG LINE

    if data and "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        if text.lower() == "/start":
            reply = "🍭 Welcome to Candy Play!\nClick below to play 👇"
            play_button = {
                "inline_keyboard": [[{
                    "text": "▶ Play Candy Play",
                    "url": "https://candy-play.onrender.com"
                }]]
            }
            send_message(chat_id, reply, play_button)

        elif text.lower() == "/play":
            send_message(chat_id, "🎮 Game started! Collect candies and earn points!")

        else:
            send_message(chat_id, f"You said: {text}")

    return {"ok": True}

def send_message(chat_id, text, reply_markup=None):
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup

    r = requests.post(url, json=payload)
    print("📤 Message sent:", r.json())  # DEBUG LINE

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
