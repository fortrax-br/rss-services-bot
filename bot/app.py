from pyrogram import Client
from os import environ
from database import crub
from pyrogram.handlers import CallbackQueryHandler
from callbacks.handler import handler as callbacksHandler


App = Client(
    "RSS",
    api_id=int(environ.get("TELEGRAM_API_ID")),
    api_hash=environ.get("TELEGRAM_API_HASH"),
    bot_token=environ.get("BOT_TOKEN")
)
App.database = crub(
    url=environ.get(
        "DATABASE_URL",
        "sqlite:///rssBot.db"
    )
)
App.add_handler(CallbackQueryHandler(callbacksHandler))
