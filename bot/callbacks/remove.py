from extra import back, getChatId
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def removeServiceMenu(client, callback):
    message = callback.message
    chatId = await getChatId(client, message)
    rssList: list = client.database.getUserUrls(chatId)
    if not rssList:
        await client.edit_message_text(
            message_id=message.message_id,
            chat_id=message.chat.id,
            text="Você ainda não possui nenhum serviço registrado!",
            reply_markup=InlineKeyboardMarkup([back("menu")])
        )
        return
    buttons: list = []
    for rssService in rssList:
        buttons.append([
            InlineKeyboardButton(
                rssService[1],
                callback_data=f"removeServiceConfirm {rssService[0]}"
            )
        ])
    buttons.append(back("menu"))
    await client.edit_message_text(
        message_id=message.message_id,
        chat_id=message.chat.id,
        text="Escolha qual você deseja remover:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


async def removeServiceConfirm(client, callback, urlId: int):
    msg = callback.message
    for button in callback.message.reply_markup.inline_keyboard:
        if button[0].callback_data == callback.data:
            title = button[0].text
            break
    await client.edit_message_text(
        message_id=msg.message_id,
        chat_id=msg.chat.id,
        text=f"Você realmente quer remover o serviço de noticias '{title}'?",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "☑️ Sim",
                    callback_data=f"removeServiceOk {urlId}"
                ),
                InlineKeyboardButton(
                    "❌ Não",
                    callback_data="removeServiceMenu"
                )
            ]
        ])
    )


async def removeServiceOk(client, callback, urlId: str):
    message = callback.message
    client.database.deleteService(message.chat.id, urlId)
    await removeServiceMenu(client, callback)
    await client.answer_callback_query(callback.id, "Removido!")
