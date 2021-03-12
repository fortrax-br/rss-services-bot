import extra
import rss
from re import findall
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pyrogram.handlers import MessageHandler


def register(app) -> None:
    app.add_handler(MessageHandler(start, filters.command("start")))
    app.add_handler(MessageHandler(add, filters.command("add")))
    app.add_handler(MessageHandler(limit, filters.command("limit")))
    app.add_handler(MessageHandler(session, filters.command("session")))
    app.add_handler(MessageHandler(delSession, filters.command("delsession")))
    app.add_handler(MessageHandler(addTimer, filters.command("addtime")))


async def start(client, message: Message) -> None:
    me = await client.get_me()
    await message.reply(
        "Olá, você pode ver os meus comandos enviando /help",
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
    userId = await extra.getChatId(client, message)
    limit = findall(r"\(([0-9]+)\)", message.text)
    if limit:
        message.text = message.text.replace(f"({limit[0]})", "")
        limit = int(limit[0])
    else:
        limit = None
    params: list = message.text.split()
    if len(params) == 1:
        await message.reply("Informe o link do serviço!")
        return
    url: str = params[1].strip()
    rssService: dict = rss.getNews(url)
    if "title" not in rssService["feed"]:
        await message.reply("Este não é um serviço RSS válido!")
        return
    client.database.addService(
        chat_id=userId,
        title=rssService["feed"]["title"],
        url=url,
        tags=[tag.strip() for tag in params[2:]],
        limit=limit
    )
    title: str = rssService["feed"]["title"]
    await message.reply(
        f"Ok, O serviço de noticias {title} foi adicionado."
    )


async def limit(client, message: Message):
    chatId = await extra.getChatId(client, message)
    print(chatId)
    params: list = message.text.split()
    if len(params) == 1:
        limit = client.database.getLimit(chatId)
        await message.reply(f"O limite atual é: {limit}.")
        return
    try:
        limit = int(params[1])
    except ValueError:
        await message.reply("Eu preciso de um número!")
        return
    if limit < 1:
        await message.reply(
            "Só posso mandar algo se o número for maior que 0(zero)!"
        )
        return
    client.database.setLimit(chatId, limit)
    await message.reply("Limite atualizado.")


async def session(client, message: Message):
    chatId: int = await extra.getChatId(client, message, True)
    if chatId in extra.errors:
        await message.reply(extra.errors[chatId])
        return
    ok: bool = client.database.createSession(message.chat.id, chatId)
    if ok:
        await message.reply("Ok, sessão iniciada.")
    else:
        await message.reply("Você já tem uma sessão ativa, para ele primeiro.")


async def delSession(client, message: Message):
    client.database.deleteSession(message.chat.id)
    await message.reply("Quaisquer sessão que estivesse ativa foi desativada.")


async def addTimer(client, message: Message):
    params: list = message.text.split()
    if len(params) == 1:
        await message.reply(f"Preciso que me informe uma hora para o envio! \
O horário deve ser baseado no UTC, a hora atual nele é {extra.getUTC()}.")
        return
    timer: list = (params[1]+":").split(":")
    hours: int = int(timer[0])
    minutes: int = int(timer[1])
    hourIsValid: bool = hours >= 0 and hours <= 23
    minutesIsValid: bool = (minutes >= 0 and minutes <= 50) and \
        (minutes / 10).is_integer()
    if not (minutesIsValid and hourIsValid):
        await message.reply("Esté horário não é válido!")
        return
    time: str = extra.addZero(hours)+":"+timer[1]
    ok: bool = client.database.addTimer(message.chat.id, time)
    if not ok:
        await message.reply("Esté horário já esta registrado!")
        return
    await message.reply("Ok, horário registrado.")
