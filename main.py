from flask import Flask, request
import os
from telegram import Bot, Update
import threading

app = Flask(__name__)
BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)

@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    threading.Thread(target=bot.send_message, args=(update.message.chat.id, "Webhook received!")).start()
    return "ok"

@app.route("/")
def index():
    return "Candy Play Bot Running!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
