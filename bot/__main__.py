import update
import commands
from app import App
from pyrogram import idle
from threading import Thread

print("Pressione CTRL+\\ quando quiser sair...")
commands.registerCommands(App)
App.start()
Thread(target=update.run, args=(App,)).start()
idle()
