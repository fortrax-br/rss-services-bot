from . import update, commands
from . import App
from pyrogram import idle
from threading import Thread
from pyrogram.handlers import CallbackQueryHandler
from .callbacks import handler as callbacksHandler


print("Pressione CTRL+\\ quando quiser sair...")
App.add_handler(CallbackQueryHandler(callbacksHandler))
commands.registerCommands(App)
App.start()
Thread(target=update.run, args=(App,)).start()
idle()
