import extra
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def listTimers(client, callback):
    msg = callback.message
    chatId: int = await extra.getChatId(client, msg)
    buttons: list = []
    timers: list = client.database.getTimers(chatId)
    for time in timers:
        buttons.append([InlineKeyboardButton(
            time[2],
            callback_data=f"removeTimerConfirm {time[2]}"
        )])
    buttons.append(extra.back("menu"))
    await client.edit_message_text(
        message_id=msg.message_id,
        chat_id=msg.chat.id,
        text="Os seguintes horários estão registrados:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


async def confirm(client, callback, time):
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


async def ok(client, callback, timer):
    chatId: int = await extra.getChatId(client, callback.message)
    client.database.deleteTimer(chatId, timer)
    await client.answer_callback_query(callback.id, "Removido!")
    await listTimers(client, callback)
