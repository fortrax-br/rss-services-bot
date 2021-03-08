from threading import Thread

import update
import commands as _
from app import App
from pyrogram import idle

print("iniciando...")
App.start()
Thread(target=update.run, args=(App,)).start()
print("Travando")
idle()
App.stop()
print("Saindo...")
exit()
