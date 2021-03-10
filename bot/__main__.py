from threading import Thread
from app import App
from pyrogram import idle

import update
import commands


print("Pressione CTRL+\\ quando quiser sair...")
commands.register(App)
App.start()
Thread(target=update.run, args=(App,)).start()
idle()
