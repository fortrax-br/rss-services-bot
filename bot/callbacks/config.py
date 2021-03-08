from extra import back, getChatId
from pyrogram.types import InlineKeyboardMarkup


async def config(client, callback):
    msg = callback.message
    chatId: int = await getChatId(client, msg)
    client.database.createConfig(chatId)
    session: str = "Não"
    if chatId != msg.chat.id:
        session = "Sim"
    config: tuple = client.database.getConfig(chatId)
    text: str = f"""Você está em uma sessão? {session}
O limite de novas noticias por vez é {config[0]}
O tempo de espera entre um envio e outro é de {config[1]} horas
O primeiro envio é as {config[2]}:00 horas
O último envio é as {config[3]}:00 horas"""
    await client.edit_message_text(
        message_id=msg.message_id,
        chat_id=msg.chat.id,
        text=text,
        reply_markup=InlineKeyboardMarkup([back("menu")])
    )
