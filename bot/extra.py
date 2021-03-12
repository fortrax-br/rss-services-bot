from time import time, strftime

from pyrogram.types import InlineKeyboardButton

errors: dict = {
    -1: "Canal/grupo para iniciar a sessão não informado!",
    -2: "Erro ao obter as informações do chat!",
    -3: "Você não pode colocar um chat privado ou um bot!",
    -4: "Eu não estou nesse canal/grupo!",
    -5: "Você não é um administrador do grupo/canal!"
}


def getUTC() -> str:
    fuso: int = int(strftime("%Z"))
    hours = int(strftime("%H")) + -(fuso)
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


async def getChatId(client, message, add=False) -> int:
    params: list = message.text.split(" ")
    if add is True and len(params) == 1:
        return -1
    elif add and len(params) >= 2:
        user: str = params[-1].strip()
        if "t.me" in user:
            user = user.split("/")[-1]
        try:
            chatInfo = await client.get_chat(user)
        except Exception:
            return -2
        if chatInfo.type in ("private", "bot"):  # Private not is permited
            return -3
        elif not chatInfo.permissions:  # Bot not in group/channel
            return -4
        admins = await client.get_chat_members(
            chatInfo.id,
            filter="administrators"
        )
        for admin in admins:
            if admin.user.id == message.from_user.id:
                return chatInfo.id
        return -5
    else:
        session, started = client.database.getSession(message.chat.id)
        if session != -1 and (time() - started) > 3600:
            client.database.deleteSession(message.chat.id)
            await message.reply("Sessão anterior fechada!")
        elif session != -1:
            return session
        return message.chat.id
