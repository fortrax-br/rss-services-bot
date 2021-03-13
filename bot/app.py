from json import load

import database
from os import environ
from callbacks.handler import handler
from pyrogram import Client
from pyrogram.handlers import CallbackQueryHandler

App: Client = Client(
    "RSS",
    api_id=int(environ.get("TELEGRAM_API_ID")),
    api_hash=environ.get("TELEGRAM_API_HASH"),
    bot_token=environ.get("BOT_TOKEN")
)
App.config: dict = {
    "mysql": {
        "user": environ.get("MYSQL_USER"),
        "password": environ.get("MYSQL_PASSWORD"),
        "host": environ.get("MYSQL_HOST", "localhost"),
        "port": int(environ.get("MYSQL_PORT", "3306"))
    }
}
App.database = database.mysql(**App.config["mysql"])
App.add_handler(CallbackQueryHandler(handler))
