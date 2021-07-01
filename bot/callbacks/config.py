from ..extra import back, getChatId
from pyrogram.types import InlineKeyboardMarkup
from pyrogram import Client
from pyrogram.types import CallbackQuery


async def config(client: Client, callback: CallbackQuery):
    msg = callback.message
    chatId: int = await getChatId(client, msg)
    if chatId != msg.chat.id:
        isSession = "Sim"
    else:
        isSession = "Não"
    config = client.database.getConfig(chatId)
    timers = client.database.getTimers(chatId)
    text = f"""Você está em uma sessão? {isSession}
O limite padrão de novas noticias é {config.max_news}\n\n"""
    if timers:
        text += "Os horários de envio são:\n\n"
        for time in timers:
            text += f" - {time.timer}\n"
    else:
        text += "Você ainda não registrou o horário de envio de suas noticias!"
    await client.edit_message_text(
        message_id=msg.message_id,
        chat_id=msg.chat.id,
        text=text,
        reply_markup=InlineKeyboardMarkup([back("menu")])
    )
