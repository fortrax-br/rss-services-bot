import extra
import rss
from re import findall
from pyrogram.filters import command
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pyrogram.handlers import MessageHandler


def registerCommands(app) -> None:
    app.add_handler(MessageHandler(start, command("start")))
    app.add_handler(MessageHandler(add, command("add")))
    app.add_handler(MessageHandler(limit, command("limit")))
    app.add_handler(MessageHandler(session, command("session")))
    app.add_handler(MessageHandler(delSession, command("delsession")))
    app.add_handler(MessageHandler(addTimer, command("addtime")))


async def start(client, message: Message) -> None:
    me = await client.get_me()
    try:
        client.database.addChat(message.chat.id)
        client.database.createConfig(message.chat.id)
    except Exception:
        pass
    await message.reply(
        "Olá, você pode ver os meus comandos pelo painel de controle, a maior parte a interação com o bot vai ser usando ele.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(
                "Adicionar em um canal/grupo",
                url=f"http://t.me/{me.username}?startgroup=botstart"
            )],
            [InlineKeyboardButton(
                "Painel de controle",
                callback_data="menu"
            )]
        ])
    )


async def add(client, message: Message):
    chatId = await extra.getChatId(client, message)
    limitExists: list = findall(r"\(([0-9]+)\)", message.text)
    if limitExists:
        message.text = message.text.replace(f"({limitExists[0]})", "")
        limit: int = int(limitExists[0])
    else:
        limit: int = 0
    parameters: list = message.text.split()
    if len(parameters) == 1:
        await message.reply("Informe o link do serviço!")
        return
    informedUrl: str = parameters[1].strip()
    rssService: dict = rss.getNews(informedUrl)
    if "title" not in rssService["feed"]:
        await message.reply("Este não é um serviço RSS válido!")
        return
    realUrl: str = rssService["href"]
    title: str = rssService["feed"]["title"]
    try:
        client.database.addUrl(title, realUrl)
    except Exception:
        pass
    serviceExists = [
        True
        for service in client.database.getUserServices(chatId)
        if service[2] == realUrl
    ]
    if serviceExists:
        await message.reply("O serviço informado já existe!")
        return
    client.database.addService(
        chatId=chatId,
        url=realUrl,
        tags=" ".join(parameters[2:]),
        limit=limit
    )
    await message.reply(
        f"Ok, O serviço de noticias {title} foi adicionado."
    )


async def limit(client, message: Message):
    chatId = await extra.getChatId(client, message)
    parameters: list = message.text.split()
    if len(parameters) == 1:
        limit: int = client.database.getDefaultLimit(chatId)
        await message.reply(f"O limite atual é: {limit}.")
        return
    try:
        limit: int = int(parameters[1])
    except ValueError:
        await message.reply("Eu preciso de um número!")
        return
    if limit < 1:
        await message.reply(
            "Só posso mandar algo se o número for maior que 0(zero)!"
        )
        return
    client.database.setDefaultLimit(chatId, limit)
    await message.reply("Limite atualizado.")


async def session(client, message: Message):
    chatId: int = await extra.getChatId(client, message, True)
    if chatId in extra.chatIdErrors:
        await message.reply(extra.chatIdErrors[chatId])
        return
    try:
        client.database.addChat(chatId)
        client.database.createConfig(chatId)
    except Exception:
        pass
    try:
        client.database.createSession(message.chat.id, chatId)
    except Exception:
        await message.reply("Você já está em uma sessão, pare ela primeiro!")
        return
    await message.reply("Ok, sessão iniciada.")


async def delSession(client, message: Message):
    client.database.deleteSession(message.chat.id)
    await message.reply("Quaisquer sessão que estivesse ativa foi desativada.")


async def addTimer(client, message: Message):
    chatId: int = await extra.getChatId(client, message)
    parameters: list = message.text.split()
    if len(parameters) == 1:
        await message.reply(f"Preciso que me informe uma hora para o envio! \
O horário deve ser baseado no UTC, a hora atual nele é {extra.getUTC()}.")
        return
    # Se o usuário mandar apenas um número o bot vai completar e colocar
    # um 0 no fim para enviar na hora pedida
    # Ex: 12 -> 12:00
    timerList: list = (parameters[1]+":0").split(":")
    hours: int = int(timerList[0])
    minutes: int = int(timerList[1])
    hourIsValid: bool = hours >= 0 and hours <= 24
    minutesIsValid: bool = (minutes >= 0 and minutes <= 55) and (minutes % 5) == 0
    if not (minutesIsValid and hourIsValid):
        await message.reply("Esté horário não é válido!")
        return
    timer: str = extra.addZero(hours)+":"+extra.addZero(minutes)
    exists = [True for t in client.database.getTimers(chatId) if t[2] == timer]
    if exists:
        await message.reply("Esté horário já esta registrado!")
        return
    client.database.addTimer(chatId, timer)
    await message.reply(f"Ok, horário {timer} registrado.")
