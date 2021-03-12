from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


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
                callback_data="services"
            )],
            [InlineKeyboardButton(
                "🗑 Remover algum serviço",
                callback_data="removeServiceMenu"
            )],
            [InlineKeyboardButton(
                "⏲ Remover um horário de envio",
                callback_data="timers"
            )]
        ])
    )
