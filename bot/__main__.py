from threading import Thread
from time import sleep

import commands
import update
from app import App
from pyrogram import idle

App.start()

#Thread(target=update.run, args=(App,)).start()

idle()

App.stop()
