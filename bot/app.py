from re import findall
from json import load
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.handlers import CallbackQueryHandler
import database, rss, callbacks


App = Client("RSS")
App.config: dict = load(open("bot.json"))
App.database = database.mysql(**App.config["mysql"])
App.add_handler(CallbackQueryHandler(callbacks.handler))


async def getChatId(client: Client, message: Message) -> int:
    marked = findall(r"\((.*)\)", message.text)
    if marked:
        message.text = marked[0]
    try:
        return int(message.text)
    except ValueError:
        pass
    if "t.me" in message.text:
        message.text = message.text.split("/")[-1]
    try:
        chat = await client.get_chat(message.text)
        return chat.id
    except:
        pass
    return message.chat.id


async def havePermition(client: Client, message: Message, id: int) -> bool:
    chat = await client.get_chat(id)
    if chat.type == "private" and message.from_user.id != id:
        await message.reply("Você não pode editar as configurações de outro usuário!")
        return False
    try:
        admins = await client.get_chat_members(group, filter="administrators")
    except:
        await message.reply("Eu não estou nesse canal/grupo!")
        return False
    for admin in admins:
        if admin.id == user:
            return True
    return True

@App.on_message(filters.command("start"))
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


@App.on_message(filters.command("help"))
async def help(client: Client, message: Message) -> None:
    await message.reply(
        """Muito bem, eu tenho os seguintes comandos:\n
`/add url <tags>` - Adiciona um serviço na lista, `tags` é opcional e você pode adicionar quantas quiser, isso vai te ajudar a se guiar no meio das noticias;\n
`/list` - Lista os seus serviços já adicionados;\n
`/remove` - Lhe envia a sua lista de serviços para você escolher qual remover;
`/limit N` - Define o limite de noticias por serviço para N.""",
        parse_mode="markdown"
    )


@App.on_message(filters.command("add"))
async def add(client: Client, message: Message):
    userId = await getChatId(client, message.text)
    permition = havePermition(client, message, userId)
    if not permition:
        return
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


@App.on_message(filters.command("list"))
async def listRss(client: Client, message: Message):
    userId = await getChatId(client, message.text)
    permition = havePermition(client, message, userId)
    if not permition:
        return
    rssList: list = client.database.getRSS(userId)
    if not rssList:
        await message.reply("Você ainda não adicionou nenhum serviço!")
        return
    text: str = "Os seguintes serviços estão cadastrados no chat:\n\n"
    for rssService in rssList:
        text += f"  - [{rssService[1]}]({rssService[2]}) Tags: {rssService[3]}\n"
    await message.reply(text)


@App.on_message(filters.command("remove"))
async def remove(client: Client, message: Message):
    userId = await getChatId(client, message.text)
    permition = havePermition(client, message, userId)
    if not permition:
        return
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

@App.on_message(filters.command("limit"))
async def limit(client: Client, message: Message):
    userId = await getChatId(client, message.text)
    permition = havePermition(client, message, userId)
    if not permition:
        return
    params: list = message.split()
    if len(params) == 1:
        limit = client.database.getLimit(userId)
        await message.reply(f"O limite atual é: {limit[0][0]}.")
        return
    try:
        limit = int(params[1])
    except:
        await message.reply("Eu preciso de um número!")
        return
    cleint.database.setLimit(userId, limit)
    await message.reply("Limite atualizado.")
