from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import Client
from pyrogram.types import CallbackQuery


async def menu(client: Client, callback: CallbackQuery):
    msg = callback.message
    await client.edit_message_text(
        message_id=msg.message_id,
        chat_id=msg.chat.id,
        text="Escolha o que deseja ver/fazer:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(
                "🖋 Mudar o estilo das noticias",
                callback_data="stylesMenu"
            )],
            [InlineKeyboardButton(
                "🗑 Remover algum serviço",
                callback_data="removeServiceMenu"
            )],
            [InlineKeyboardButton(
                "⏲ Remover um horário de envio",
                callback_data="timers"
            )],
            [InlineKeyboardButton(
                "🛠 Suas configurações",
                callback_data="config"
            )],
            [InlineKeyboardButton(
                "🗞 Seus serviços",
                callback_data="services"
            )],
            [InlineKeyboardButton(
                "📠 Todos os comandos",
                callback_data="help"
            )]
        ])
    )
