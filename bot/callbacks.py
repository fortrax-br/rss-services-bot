import extra
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def back(f):
    return [InlineKeyboardButton("« Voltar", callback_data=f)]


async def handler(client, callback):
    data: list = callback.data.split()
    command: str = data[0].strip()
    data.pop(0)
    if command == "menu":
        await menu(client, callback)
    elif command == "removeServiceMenu":
        await removeServiceMenu(client, callback)
    elif command == "removeServiceConfirm":
        await removeServiceConfirm(client, callback, int(data[0]))
    elif command == "removeServiceOk":
        await removeServiceOk(client, callback, int(data[0]))


async def menu(client, callback):
    msg = callback.message
    await client.edit_message_text(
        message_id=msg.message_id,
        chat_id=msg.chat.id,
        text="Escolha o que deseja ver/fazer:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(
                "📠 Todos os comandos",
                callback_data="commands"
            )],
            [InlineKeyboardButton(
                "🛠 Suas configurações",
                callback_data="config"
            )],
            [InlineKeyboardButton(
                "🗞 Seus serviços",
                callback_data="show"
            )],
            [InlineKeyboardButton(
                "🗑 Remover algum serviço",
                callback_data="removeServiceMenu"
            )]
        ])
    )


async def removeServiceMenu(client, callback):
    message = callback.message
    chatId = await extra.getChatId(client, message)
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
