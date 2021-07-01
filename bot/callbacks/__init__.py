from . import config, services, timer, cancel, menu, bothelp, styles
from pyrogram import Client
from pyrogram.types import CallbackQuery


async def handler(client: Client, callback: CallbackQuery):
    data = callback.data.split()
    command = data.pop(0).strip()
    if command == "menu":
        await menu.menu(client, callback)
    elif command == "removeServiceMenu":
        await services.removeServiceMenu(client, callback)
    elif command == "removeServiceConfirm":
        await services.removeServiceConfirm(client, callback, int(data[0]))
    elif command == "removeServiceOk":
        await services.removeServiceOk(client, callback, int(data[0]))
    elif command == "services":
        await services.listServices(client, callback)
    elif command == "config":
        await config.config(client, callback)
    elif command == "timers":
        await timer.listTimers(client, callback)
    elif command == "removeTimer":
        await timer.removeTimer(client, callback, data[0])
    elif command == "removeTimerConfirm":
        await timer.confirm(client, callback, data[0])
    elif command == "removeTimerOk":
        await timer.ok(client, callback, data[0])
    elif command == "stylesMenu":
        await styles.menu(client, callback)
    elif command == "selectStyle":
        await styles.select(client, callback, data[0])
    elif command == "setStyle":
        await styles.setStyle(client, callback, data[0], int(data[1]))
    elif command == "cancel":
        await cancel.cancel(client, callback)
    elif command == "help":
        await bothelp.botHelp(client, callback)
