from datetime import datetime, timezone
from time import time
from pyrogram import Client
from pyrogram.types import InlineKeyboardButton, Message
from typing import List, Union
from .database.types import Error


async def getChatId(client: Client, message: Message) -> int:
    session = client.database.getSession(message.chat.id)
    if isinstance(session, Error):
        return message.chat.id
    if (time() - session.started) >= 3600:
        client.database.deleteSession(message.chat.id)
        await message.reply("Sessão anterior fechada!")
        return message.chat.id
    return session.control_id


async def getChatIdByUsername(client: Client, userId: int, chatId: Union[str, int]):
    if "t.me" in str(chatId):
        chatId: str = chatId.split("/")[-1]
    try:
        chatInfo = await client.get_chat(chatId)
    except Exception:
        raise Exception("Erro ao obter informações do chat!")
    if chatInfo.type in ("private", "bot"):
        raise Exception("Você não pode controlar outra pessoa ou um bot!")
    try:
        chatAdmins = await client.get_chat_members(
            chat_id=chatInfo.id,
            filter="administrators"
        )
    except Exception:
        raise Exception(
            "Eu não estou nesse canal/grupo ou não sou administrador!"
        )
    isAdmin = any(filter(
        lambda admin: admin.user.id == userId,
        chatAdmins
    ))
    if isAdmin:
        return chatInfo.id
    raise Exception("Você não é um administrador do grupo/canal!")


def getUTC() -> str:
    timeNow = datetime.now(timezone.utc)
    result = f"{addZero(timeNow.hour)}:{addZero(timeNow.minute)}"
    return result


def addZero(number: int) -> str:
    if number < 10:
        return f"0{number}"
    return str(number)


def back(data: str) -> List:
    return [
        InlineKeyboardButton(
            text="« Voltar",
            callback_data=data
        )
    ]
