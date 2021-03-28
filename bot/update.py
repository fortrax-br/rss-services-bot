from bs4 import BeautifulSoup
from rss import getNews
from time import sleep, strftime
from extra import getUTC
from threading import Thread


def run(app) -> None:
    print("Bot iniciado")
    lastUpdate: int = int(strftime("%M"))
    while True:
        sleep(10)
        minutes: int = int(strftime("%M"))
        if not ((minutes % 5) == 0 and lastUpdate != minutes):
            continue
        print("Atualizando...")
        update(app)
        lastUpdate = minutes


def update(app) -> None:
    utc: int = getUTC()
    chats: list = app.database.getChatsByHours(utc)
    for chat in chats:
        chatId: int = chat[1]
        informations: list = app.database.getUserServices(chatId)
        Thread(target=sendNews, args=(app, chatId, informations,)).start()


def sendNews(app, chatId: int, informations: list) -> None:
    for info in informations:
        title = info[1]
        url = info[2]
        tags = info[3]
        limit: int = info[4]
        lastUpdate: str = info[5]
        if not limit:
            limit = app.database.getDefaultLimit(chatId)
        count = 1
        news: dict = getNews(url)
        for new in news["entries"]:
            if lastUpdate == new["published"]:
                break
            description = BeautifulSoup(new["description"], "html.parser").text
            text: str = f"**{new['title']}**\n"
            text += f"{tags}\n"
            text += f"__{new['published']} pelo serviço de noticias {news['feed']['title']}__\n\n"
            text += f"```{description}```\n\n"
            text += f"🌐 [Ler mais!]({new['link']})"
            if len(text) > 4096:
                continue
            app.send_message(
                chat_id=chatId,
                text=text,
                parse_mode="markdown"
            )
            count += 1
            if count == limit:
                break
        app.database.setLastUpdate(
            chatId=chatId,
            urlId=info[0],
            lastUpdate=news["entries"][0]["published"]
        )
