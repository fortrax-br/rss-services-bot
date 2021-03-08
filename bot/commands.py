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
    if chatId in extra.errors:
        await message.reply(extra.errors[chatId])
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
