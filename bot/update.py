from bs4 import BeautifulSoup
from rss import getNews
from time import sleep, strftime
from extra import getUTC
from threading import Thread


def run(app) -> None:
    print("Bot iniciado")
    lastUpdate: int = int(strftime("%M"))
    while True:
        sleep(30)
        minutes: int = int(strftime("%M"))
        if not ((minutes % 5) == 0 and lastUpdate != minutes):
            continue
        print("atulizando...")
        update(app)
        lastUpdate = minutes


def update(app) -> None:
    hour: str = getUTC()
    chats: list = app.database.getChatsByHours(hour)
    for chat in chats:
        chatId: int = chat[1]
        services: list = app.database.getUserServices(chatId)
        Thread(target=sendNews, args=(app, chatId, services,)).start()


def sendNews(app, chatId: int, services: list) -> None:
    style: tuple = app.database.getStyle(chatId)
    for service in services:
        serviceTitle: str = service[1]
        url: str = service[2]
        tags: str = service[3]
        limit: int = service[4]
        lastUpdate: str = service[5]
        if not limit:
            limit: int = app.database.getDefaultLimit(chatId)
        count: int = 0
        news: dict = getNews(url)
        for new in news["entries"]:
            if "published" not in new and "updated" not in new:
                news["entries"].remove(new)
                continue
            try:
                published: str = new["published"]
            except Exception:
                published: str = new["updated"]
            if lastUpdate == published:
                break
            description: str = BeautifulSoup(
                new["description"],
                "html.parser"
            ).text
            text: str = style[1]+new['title']+style[1]+"\n"
            if tags:
                text += f"{tags}\n"
            text += style[2]+serviceTitle+"» "+published+style[2]+"\n\n"
            text += style[3]+description+style[3]+"\n\n"
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
            sleep(1)
        if len(news["entries"]) > 0:
            try:
                published: str = news["entries"][0]["published"]
            except Exception:
                published: str = news["entries"][0]["updated"]
            app.database.setLastUpdate(
                chatId=chatId,
                urlId=service[0],
                lastUpdate=published
            )
