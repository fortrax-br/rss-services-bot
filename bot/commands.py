import extra
from app import App
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message


@App.on_message(filters.command("start"))
async def start(client, message: Message) -> None:
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
async def help(client, message: Message) -> None:
    await message.reply(
        """Muito bem, eu tenho os seguintes comandos:\n
`/add url <tags>` - Adiciona um serviço na lista, `tags` é opcional e você pode adicionar quantas quiser, isso vai te ajudar a se guiar no meio das noticias;\n
`/list` - Lista os seus serviços já adicionados;\n
`/remove` - Lhe envia a sua lista de serviços para você escolher qual remover;
`/limit N` - Define o limite de noticias por serviço para N.""",
        parse_mode="markdown"
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
    await message.reply(f"Ok, O serviço de noticias {rssService['feed']['title']} foi adicionado.")


@App.on_message(filters.command("list"))
async def listRss(client, message: Message):
    userId = await extra.getChatId(client, message)
    rssList: list = client.database.getUserUrls(userId)
    if not rssList:
        await message.reply("Você ainda não adicionou nenhum serviço!")
        return
    text: str = "Os seguintes serviços estão cadastrados no chat:\n\n"
    for rssService in rssList:
        text += f"  - [{rssService[1]}]({rssService[2]}) Tags: {rssService[3]}\n"
    await message.reply(text)


@App.on_message(filters.command("remove"))
async def remove(client, message: Message):
    chatId = await extra.getChatId(client, message)
    rssList: list = client.database.getUserUrls(chatId)
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
async def limit(client, message: Message):
    chatId = await extra.getChatId(client, message)
    params: list = message.text.split()
    if len(params) == 1:
        limit = client.database.getLimit(chatId)
        await message.reply(f"O limite atual é: {limit}.")
        return
    try:
        limit = int(params[1])
    except:
        await message.reply("Eu preciso de um número!")
        return
    if limit < 1:
        await message.reply("Só posso mandar algo se o número for maior que 0(zero)!")
        return
    client.database.setLimit(chatId, limit)
    await message.reply("Limite atualizado.")