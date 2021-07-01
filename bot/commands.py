from . import extra
from feedparser import parse as getNews
from re import findall
from pyrogram import Client
from pyrogram.filters import command
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pyrogram.handlers import MessageHandler


def registerCommands(app: Client) -> None:
    app.add_handler(MessageHandler(start, command("start")))
    app.add_handler(MessageHandler(addService, command("add")))
    app.add_handler(MessageHandler(limit, command("limit")))
    app.add_handler(MessageHandler(session, command("session")))
    app.add_handler(MessageHandler(delSession, command("delsession")))
    app.add_handler(MessageHandler(addTimer, command("addtime")))


async def start(client: Client, message: Message) -> None:
    me = await client.get_me()
    try:
        client.database.addUser(message.chat.id)
        client.database.createConfig(message.chat.id)
    except Exception:
        pass
    await message.reply(
        "Olá, clique no botão do painel de controle e veja o que eu faço ;)",
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


async def addService(client: Client, message: Message):
    chatId = await extra.getChatId(client, message)
    limitExists: list = findall(r"\(([0-9]+)\)", message.text)
    if limitExists:
        message.text = message.text.replace(f"({limitExists[0]})", "")
        limit = int(limitExists[0])
    else:
        limit = 0
    args = message.text.split()
    if len(args) == 1:
        await message.reply("Informe o link do serviço!")
        return
    informedUrl = args[1].strip()
    rssService: dict = getNews(informedUrl)
    if "title" not in rssService["feed"]:
        await message.reply("Este não é um serviço RSS válido!")
        return
    realUrl: str = rssService["href"]
    title: str = rssService["feed"]["title"]
    try:
        client.database.addUrl(title, realUrl)
    except Exception:
        pass
    serviceExists = any(filter(
        lambda service: service.url == realUrl,
        client.database.getServices(chatId)
    ))
    if serviceExists:
        await message.reply("O serviço informado já existe!")
        return
    client.database.addService(
        chatId=chatId,
        url=realUrl,
        tags=" ".join(args[2:]).strip(),
        limit=limit
    )
    await message.reply(
        f"Ok, O serviço de noticias {title} foi adicionado."
    )


async def limit(client: Client, message: Message):
    chatId: int = await extra.getChatId(client, message)
    args = message.text.split()
    if len(args) == 1:
        config = client.database.getConfig(chatId)
        await message.reply(f"O limite padrão atual é: {config.max_news}.")
        return
    try:
        limit = int(args[1])
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


async def session(client: Client, message: Message):
    args = message.text.split()
    if len(args) == 1:
        await message.reply("Qual canal/grupo você quer controlar?")
        return
    try:
        chatId: int = await extra.getChatIdByUsername(
            client=client,
            userId=message.from_user.id,
            chatId=args[1]
        )
    except Exception as error:
        await message.reply(error.args()[0])
        return
    try:
        client.database.addUser(chatId)
        client.database.createConfig(chatId)
    except Exception:
        pass
    try: client.database.createDefaultStyle(chatId)
    except Exception: pass
    try:
        client.database.createSession(message.chat.id, chatId)
    except Exception:
        await message.reply("Você já está em uma sessão, pare ela primeiro!")
        return
    await message.reply("Ok, sessão iniciada.")


async def delSession(client, message: Message):
    client.database.deleteSession(message.chat.id)
    await message.reply("Quaisquer sessão que estivesse ativa foi desativada.")


async def addTimer(client: Client, message: Message):
    chatId: int = await extra.getChatId(client, message)
    args = message.text.split()
    if len(args) == 1:
        await message.reply(
            "Preciso que me informe uma hora para o envio!\n" +
            f"O horário deve ser baseado no UTC(0), a hora atual nele é {extra.getUTC()}."
        )
        return
    # Se o usuário mandar apenas um número o bot vai completar e colocar
    # um 0 no fim para enviar na hora pedida
    # Ex: 12 -> 12:00
    timerList = (args[1]+":00").split(":")
    hours = int(timerList[0])
    minutes = int(timerList[1])
    hourIsValid = hours >= 0 and hours <= 23
    minutesIsValid = minutes >= 0 and minutes <= 59
    if not (minutesIsValid and hourIsValid):
        await message.reply("Esté horário não é válido!")
        return
    timer = f"{extra.addZero(hours)}:{extra.addZero(minutes)}"
    existentTimers: tuple = client.database.getTimers(chatId)
    exists = any(filter(lambda item: item.timer == timer, existentTimers))
    if exists:
        await message.reply("Esté horário já esta registrado!")
        return
    client.database.addTimer(chatId, timer)
    await message.reply(f"Ok, horário {timer} registrado.")
