from extra import back, getChatId
from pyrogram.types import InlineKeyboardMarkup


async def config(client, callback):
    msg = callback.message
    chatId: int = await getChatId(client, msg)
    if chatId != msg.chat.id:
        session: str = "Sim"
    else:
        session: str = "Não"
    config: tuple = client.database.getConfig(chatId)
    timers: tuple = client.database.getTimers(chatId)
    text: str = f"""Você está em uma sessão? {session}
O limite padrão de novas noticias é {config[2]}\n\n"""
    if timers:
        text += "Os horários de envio são:\n\n"
        for time in timers:
            text += f" - {time[2]}\n"
    else:
        text += "Você ainda não registrou o horário de envio de suas noticias!"
    await client.edit_message_text(
        message_id=msg.message_id,
        chat_id=msg.chat.id,
        text=text,
        reply_markup=InlineKeyboardMarkup([back("menu")])
    )
