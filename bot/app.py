from json import load

import callbacks
import database
import extra
import rss
from pyrogram import Client, filters
from pyrogram.handlers import CallbackQueryHandler

App: Client = Client("RSS")
App.config: dict = load(open("bot.json"))
App.database = database.mysql(**App.config["mysql"])
App.add_handler(CallbackQueryHandler(callbacks.handler))