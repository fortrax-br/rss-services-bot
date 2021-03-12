from callbacks import config, listServices, remove, timer, cancel, menu


async def handler(client, callback):
    data: list = callback.data.split()
    command: str = data[0].strip()
    data.pop(0)
    if command == "menu":
        await menu.menu(client, callback)
    elif command == "removeServiceMenu":
        await remove.removeServiceMenu(client, callback)
    elif command == "removeServiceConfirm":
        await remove.removeServiceConfirm(client, callback, int(data[0]))
    elif command == "removeServiceOk":
        await remove.removeServiceOk(client, callback, int(data[0]))
    elif command == "services":
        await listServices.listServices(client, callback)
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
    elif command == "cancel":
        await cancel.cancel(client, callback)
