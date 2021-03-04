from pyrogram import idle
from app import App
from threading import Thread
from time import sleep
import update

App.start()

#Thread(target=update.run, args=(App,)).start()

idle()

App.stop()
