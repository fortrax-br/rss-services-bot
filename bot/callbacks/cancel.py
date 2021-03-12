from .menu import menu

async def cancel(client, callback):
    await client.answer_callback_query(callback.id, "Cancelado!")
    await menu(client, callback)


