async def handler(client, callback):
    data: list = callback.data.split()
    if data[0] == "remove":
        await removeRSS(client, callback, int(data[1]))

async def removeRSS(client, callback, urlId: str):
    message = callback.message
    client.database.deleteService(message.chat.id, urlId)
    for button in callback.message.reply_markup.inline_keyboard:
        if button[0].callback_data == callback.data:
            title = button[0].text
            break
    await client.edit_message_text(
        message_id=message.message_id,
        chat_id=message.chat.id,
        text=f"Serviço de noticias {title} removido."
    )
    await client.answer_callback_query(callback.id, "Removido!")
