from json import load

from callbacks.handler import handler
import database
from pyrogram import Client
from pyrogram.handlers import CallbackQueryHandler

App: Client = Client("RSS")
App.config: dict = load(open("bot.json"))
App.database = database.mysql(**App.config["mysql"])
App.add_handler(CallbackQueryHandler(handler))
