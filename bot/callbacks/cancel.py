from .menu import menu
from pyrogram import Client
from pyrogram.types import CallbackQuery


async def cancel(client: Client, callback: CallbackQuery):
    await client.answer_callback_query(callback.id, "Cancelado!")
    await menu(client, callback)
