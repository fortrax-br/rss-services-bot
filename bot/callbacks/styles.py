from extra import back, getChatId
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


names = {
    "description": "Descrição",
    "hour_and_services": "Hora e serviço",
    "title": "Título"
}
styles = [
    {"name": "Italico", "value": "__"},
    {"name": "Mono Espaçado", "value": "```"},
    {"name": "Negrito", "value": "**"},
    {"name": "Tracejado", "value": "~~"}
]


async def menu(client, callback):
    chatId: int = await getChatId(client, callback.message)
    try:
        client.database.createDefaultStyle(chatId)
    except Exception:
        pass
    style = client.database.getStyle(chatId)
    text = f"""Escolha qual estilo você deseja alterar:

{style[1]}What is Lorem Ipsum?{style[1]}
#lorem #ipsum
{style[2]}Qua, 31 Mar 2021 04:00:00 -0300 pelo serviço de noticias Lorem Ipsum{style[2]}

{style[3]}Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.{style[3]}
"""
    buttons: list = []
    for key, value in names.items():
        buttons += [[InlineKeyboardButton(
            value,
            callback_data="selectStyle " + key
        )]]
    buttons.append(back("menu"))
    await client.edit_message_text(
        message_id=callback.message.message_id,
        chat_id=callback.message.chat.id,
        text=text,
        reply_markup=InlineKeyboardMarkup(buttons)
    )


async def select(client, callback, location):
    buttons = []
    for style in styles:
        index = str(styles.index(style))
        buttons += [[InlineKeyboardButton(
            style["name"],
            callback_data=f"setStyle {location} {index}"
        )]]
    buttons.append(back("stylesMenu"))
    await client.edit_message_text(
        message_id=callback.message.message_id,
        chat_id=callback.message.chat.id,
        text=f"Qual estilo você deseja para \"{names[location]}\": ",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


async def setStyle(client, callback, location: str, index: int):
    chatId: int = await getChatId(client, callback.message)
    client.database.setStyle(chatId, **{location: styles[index]["value"]})
    await client.answer_callback_query(callback.id, "Alterado com sucesso!")
    await menu(client, callback)
