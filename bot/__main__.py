from threading import Thread
from app import App
from pyrogram import idle

import update
import commands
import sys


print("Pressione CTRL+\\ quando quiser sair...")
App.start()
up = Thread(target=update.run, args=(App,))
up.start()
idle()
