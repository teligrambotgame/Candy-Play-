# main.py
import os
import sqlite3
from flask import Flask, render_template, request, jsonify, g
import requests

app = Flask(__name__, template_folder="templates", static_folder="static")

DATABASE = 'progress.db'
BOT_TOKEN = os.environ.get('7999216513:AAHTWGFPbFAd5j8CfCs2Hgw0CxExKpREOYQ')  # Telegram Bot Token
BASE_TELEGRAM_API = f"https://api.telegram.org/bot{7999216513:AAHTWGFPbFAd5j8CfCs2Hgw0CxExKpREOYQ}" if BOT_TOKEN else None

# ---------------- DATABASE ----------------
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

def init_db():
    db = get_db()
    db.execute('''
        CREATE TABLE IF NOT EXISTS progress(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id TEXT,
            level INTEGER,
            score INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    db.commit()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.before_first_request
def startup():
    init_db()

# ---------------- ROUTES ----------------
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/report_score', methods=['POST'])
def report_score():
    data = request.get_json()
    telegram_id = str(data.get("telegram_id")) if data.get("telegram_id") else None
    level = int(data.get("level", 0))
    score = int(data.get("score", 0))

    db = get_db()
    db.execute('INSERT INTO progress(telegram_id, level, score) VALUES (?, ?, ?)',
               (telegram_id, level, score))
    db.commit()

    # Telegram notification
    if telegram_id and BOT_TOKEN:
        try:
            requests.post(f"{BASE_TELEGRAM_API}/sendMessage", json={
                "chat_id": telegram_id,
                "text": f"🎉 Congrats! You cleared Candy Play Level {level} with {score} points!"
            }, timeout=5)
        except:
            pass

    return jsonify({"status": "ok"})

@app.route('/progress', methods=['GET'])
def progress():
    db = get_db()
    cur = db.execute("SELECT telegram_id, level, score, timestamp FROM progress ORDER BY id DESC LIMIT 200")
    rows = [dict(r) for r in cur.fetchall()]
    return jsonify(rows)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
