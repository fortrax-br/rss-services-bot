from time import time, strftime
from pyrogram.types import InlineKeyboardButton


chatIdErrors: dict = {
    -1: "Canal/grupo para iniciar a sessão não informado!",
    -2: "Erro ao obter as informações do chat!",
    -3: "Você não pode colocar um chat privado ou um bot!",
    -4: "Eu não estou nesse canal/grupo ou não sou administrador!",
    -5: "Você não é um administrador do grupo/canal!"
}


async def getChatId(client, message, add=False) -> int:
    parameters: list = message.text.split(" ")
    if add is True and len(parameters) == 1:
        return -1
    elif add and len(parameters) >= 2:
        user: str = parameters[-1].strip()
        if "t.me" in user:
            user: str = user.split("/")[-1]
        try:
            chatInfo = await client.get_chat(user)
        except Exception:
            return -2
        if chatInfo.type in ("private", "bot"):  # Private not is permited
            return -3
        try:
            admins = await client.get_chat_members(
                chatInfo.id,
                filter="administrators"
            )
        except Exception:
            return -4
        for admin in admins:
            if admin.user.id == message.from_user.id:
                return chatInfo.id
        return -5
    else:
        session = client.database.getSession(message.chat.id)
        if not session:
            return message.chat.id
        if (time() - session[2]) > 3600:
            client.database.deleteSession(message.chat.id)
            await message.reply("Sessão anterior fechada!")
            return message.chat.id
        return session[1]


def getUTC() -> str:
    fusoName: str = strftime("%Z")
    if fusoName == "UTC":
        fuso: int = 0
    else:
        try:
            fuso: int = int(fusoName)
        except ValueError:
            fuso: int = 0
    hours: int = int(strftime("%H")) + -(fuso)
    result: str = addZero(hours) + ":" + strftime("%M")
    return result


def addZero(time: int) -> str:
    result: str = ""
    if time < 10:
        result += "0"
    result += str(time)
    return result


def back(f: str) -> list:
    return [InlineKeyboardButton("« Voltar", callback_data=f)]
