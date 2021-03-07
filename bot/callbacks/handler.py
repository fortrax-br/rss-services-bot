from extra import *
from .remove import *
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


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
