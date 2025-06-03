# app.py — точка входа. Flask приложение и webhook обработка

from flask import Flask, request
from bot import handle_update
import config

app = Flask(__name__)

@app.route(f"/{config.BOT_TOKEN}/", methods=["POST"])
def webhook():
    update = request.get_json(force=True)
    return handle_update(update), 200
