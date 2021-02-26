from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.handlers import CallbackQueryHandler
from json import load
from re import findall
import database, rss, callbacks


App = Client("RSS")
App.config: dict = load(open("bot.json"))
App.database = database.mysql(**App.config["mysql"])
App.add_handler(CallbackQueryHandler(callbacks.handler))


async def getChatId(client: Client, text: str) -> int:
    try:
        return int(text)
    except ValueError:
        pass
    channel = findall(r"\((.*)\)", text)
    if channel:
        text = channel[0]
    if "t.me" in text:
        text = text.split("/")[-1]
    try:
        chat = await client.get_chat(text)
    except:
        return -1
    return chat.id


@App.on_message(filters.command(["start"]))
async def start(client: Client, message: Message) -> None:
    me = await client.get_me()
    await message.reply(
        text="Olá, sou um bot de noticias usando RSS, saiba como me usar com o comando /help",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "Adicionar em um canal/grupo",
                    url=f"http://t.me/{me.username}?startgroup=botstart")
             ]
        ])
    )


@App.on_message(filters.command(["help"]))
async def help(client: Client, message: Message) -> None:
    await message.reply(
        """Muito bem, eu tenho os seguintes comandos:\n
`/add url <tags>` - Adiciona um serviço na lista, `tags` é opcional e você pode adicionar quantas quiser, isso vai te ajudar a se guiar no meio das noticias;\n
`/list` - Lista os seus serviços já adicionados;\n
`/remove` - Lhe envia a sua lista de serviços para você escolher qual remover.""",
        parse_mode="markdown"
    )


@App.on_message(filters.command(["add"]))
async def add(client: Client, message: Message):
    userId = await getChatId(client, message.text)
    if userId == -1:
        userId = message.chat.id
    user = findall(r"\(.*\)", message.text)
    if user:
        message.text = message.text.replace(user[0], "")
    params: list = message.text.split()
    if len(params) == 1:
        await message.reply("Informe o link do serviço!")
        return
    url: str = params[1].strip()
    rssService: dict = rss.getNews(url)
    if "title" not in rssService["feed"]:
        await message.reply("Este não é um serviço RSS valido!")
        return
    client.database.addRSS(
        chat_id=userId,
        title=rssService["feed"]["title"],
        url=url,
        tags=[tag.strip() for tag in params[2:]]
    )
    await message.reply(f"Ok, O serviço de noticias {rssService['feed']['title']} foi adicionado.")


@App.on_message(filters.command(["list"]))
async def listRss(client: Client, message: Message):
    userId = await getChatId(client, message.text)
    if userId == -1:
        userId = message.chat.id
    rssList: list = client.database.getRSS(userId)
    if not rssList:
        await message.reply("Você ainda não adicionou nenhum serviço!")
        return
    text: str = "Os seguintes serviços estão cadastrados no chat:\n\n"
    for rssService in rssList:
        text += f"  - [{rssService[1]}]({rssService[2]}) Tags: {rssService[3]}\n"
    await message.reply(text)


@App.on_message(filters.command(["remove"]))
async def remove(client: Client, message: Message):
    userId = await getChatId(client, message.text)
    if userId == -1:
        userId = message.chat.id
    rssList: list = client.database.getRSS(userId)
    if not rssList:
        await message.reply("Você ainda não conectou este chat em nenhum serviço RSS.")
        return
    buttons: list = []
    for rssService in rssList:
        buttons.append([
            InlineKeyboardButton(
                rssService[1],
                callback_data=f"remove {rssService[0]}"
            )
        ])
    await message.reply(
        "Escolha qual você deseja remover:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )
