import os
from flask import Flask, request
import telegram

TOKEN = os.getenv("BOT_TOKEN")
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

@app.route('/')
def home():
    return "Candy Play Bot is running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    
    if update.message:
        chat_id = update.message.chat.id
        text = update.message.text
        
        if text == "/start":
            bot.sendMessage(chat_id=chat_id, text="🍬 Welcome to Candy Play! Let's start playing!")
        else:
            bot.sendMessage(chat_id=chat_id, text="I didn't understand that. Type /start to play!")
    
    return "ok"

if __name__ == "__main__":
    app.run(port=5000)
