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

App.database = database.crub(
    environ.get(
        "DATABASE_URL",
        "sqlite:///rssBot.db"
    )
)
App.add_handler(CallbackQueryHandler(handler))
