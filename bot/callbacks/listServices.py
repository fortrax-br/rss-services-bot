from extra import back, getChatId
from pyrogram.types import InlineKeyboardMarkup


async def listServices(client, callback):
    msg = callback.message
    userId = await getChatId(client, msg)
    rssList: list = client.database.getUserUrlsSimple(userId)
    if not rssList:
        await client.edit_message_text(
            message_id=msg.message_id,
            chat_id=msg.chat.id,
            text="Você ainda não adicionou nenhum serviço!",
            reply_markup=InlineKeyboardMarkup([back("menu")])
        )
        return
    text: str = "Os seguintes serviços estão cadastrados no chat:\n\n"
    for service in rssList:
        text += f" - [{service[1]}]({service[2]})\n"
        text += f"   Limite: {service[3] or 'Padrão'}\n"
        text += f"   Tags: {service[4]}\n\n"
    await client.edit_message_text(
        message_id=msg.message_id,
        chat_id=msg.chat.id,
        text=text,
        reply_markup=InlineKeyboardMarkup([back("menu")])
    )
