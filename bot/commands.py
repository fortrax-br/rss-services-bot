import extra
import rss
from app import App
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message


@App.on_message(filters.command("start"))
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


@App.on_message(filters.command("add"))
async def add(client, message: Message):
    userId = await extra.getChatId(client, message)
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
        tags=[tag.strip() for tag in params[2:]]
    )
    title: str = rssService["feed"]["title"]
    await message.reply(
        f"Ok, O serviço de noticias {title} foi adicionado."
    )


@App.on_message(filters.command("remove"))
async def remove(client, message: Message):
    chatId = await extra.getChatId(client, message)
    rssList: list = client.database.getUserUrls(chatId)
    if not rssList:
        await message.reply(
            "Você ainda não conectou este chat em nenhum serviço RSS."
        )
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


@App.on_message(filters.command("session"))
async def session(client, message: Message):
    chatId: int = await extra.getChatId(client, message, True)
    if chatId < 0 and chatId >= -5:
        if chatId == -1:
            err = "Canal/grupo para iniciar a sessão não informado!"
        elif chatId == -2:
            err = "Erro ao obter as informações do chat!"
        elif chatId == -3:
            err = "Você não pode colocar um chat privado ou um bot!"
        elif chatId == -4:
            err = "Eu não estou nesse canal/grupo!"
        elif chatId == -5:
            err = "Você não é um administrador do grupo/canal!"
        await message.reply(err)
        return
    ok: bool = client.database.createSession(message.chat.id, chatId)
    if ok:
        await message.reply("Ok, sessão iniciada.")
    else:
        await message.reply("Você já tem uma sessão ativa, para ele primeiro.")


@App.on_message(filters.command("delsession"))
async def delSession(client, message: Message):
    client.database.deleteSession(message.chat.id)
    await message.reply("Quaisquer sessão que estivesse ativa foi desativada.")
