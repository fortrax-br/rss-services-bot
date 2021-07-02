from ..extra import back, getChatId
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import Client
from pyrogram.types import CallbackQuery


async def removeServiceMenu(client: Client, callback: CallbackQuery):
    message = callback.message
    chatId = await getChatId(client, message)
    services = client.database.getServices(chatId)
    if not services:
        await client.edit_message_text(
            message_id=message.message_id,
            chat_id=message.chat.id,
            text="Você ainda não possui nenhum serviço registrado!",
            reply_markup=InlineKeyboardMarkup([back("menu")])
        )
        return
    buttons: list = []
    for service in services:
        buttons.append([
            InlineKeyboardButton(
                text=service.title,
                callback_data=f"removeServiceConfirm {service.url_id}"
            )
        ])
    buttons.append(back("menu"))
    await client.edit_message_text(
        message_id=message.message_id,
        chat_id=message.chat.id,
        text="Escolha qual você deseja remover:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


async def removeServiceConfirm(client: Client, callback: CallbackQuery, urlId: int):
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
                    callback_data="cancel"
                )
            ]
        ])
    )


async def removeServiceOk(client: Client, callback: CallbackQuery, urlId: int):
    message = callback.message
    userId = await getChatId(client, message)
    client.database.deleteService(userId, urlId)
    await removeServiceMenu(client, callback)
    await client.answer_callback_query(callback.id, "Removido!")


async def listServices(client: Client, callback: CallbackQuery):
    msg = callback.message
    userId = await getChatId(client, msg)
    services = client.database.getServices(userId)
    if not services:
        await client.edit_message_text(
            message_id=msg.message_id,
            chat_id=msg.chat.id,
            text="Você ainda não adicionou nenhum serviço!",
            reply_markup=InlineKeyboardMarkup([back("menu")])
        )
        return
    text: str = "Os seguintes serviços estão cadastrados no chat:\n\n"
    for service in services:
        text += f" - [{service.title}]({service.url})\n"
        text += f"   Limite: {service.max_news or 'Padrão'}\n"
        text += f"   Tags: {service.tags}\n\n"
    await client.edit_message_text(
        message_id=msg.message_id,
        chat_id=msg.chat.id,
        text=text,
        reply_markup=InlineKeyboardMarkup([back("menu")])
    )
