from .. import extra
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import Client
from pyrogram.types import CallbackQuery


async def listTimers(client: Client, callback: CallbackQuery):
    msg = callback.message
    chatId = await extra.getChatId(client, msg)
    buttons = []
    timers = client.database.getTimers(chatId)
    for time in timers:
        buttons.append([InlineKeyboardButton(
            text=time.timer,
            callback_data=f"removeTimerConfirm {time.timer}"
        )])
    buttons.append(extra.back("menu"))
    await client.edit_message_text(
        message_id=msg.message_id,
        chat_id=msg.chat.id,
        text="Os seguintes horários estão registrados:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


async def confirm(client: Client, callback: CallbackQuery, time: str):
    msg = callback.message
    await client.edit_message_text(
        message_id=msg.message_id,
        chat_id=msg.chat.id,
        text=f"Você realmente quer remover o horário de envio {time}?",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    text="☑️ Sim",
                    callback_data=f"removeTimerOk {time}"
                ),
                InlineKeyboardButton(
                    text="❌ Não",
                    callback_data="cancel"
                )
            ]
        ])
    )


async def ok(client: Client, callback: CallbackQuery, timer: str):
    chatId: int = await extra.getChatId(client, callback.message)
    client.database.deleteTimer(chatId, timer)
    await client.answer_callback_query(callback.id, "Removido!")
    await listTimers(client, callback)
