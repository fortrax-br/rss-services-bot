from .extra import getUTC
from .database import types
from time import sleep, gmtime
from bs4 import BeautifulSoup
from threading import Thread
from pyrogram import Client
from typing import List, Union
from feedparser import parse as getNews


def run(app: Client):
    print("Bot iniciado")
    lastUpdate: int = gmtime().tm_min
    while True:
        minutes: int = gmtime().tm_min
        if lastUpdate != minutes:
            lastUpdate = minutes
            update(app)
            continue
        sleep(10)


def update(app: Client):
    hour: str = getUTC()
    timers: List[types.Timer] = app.database.getUsersByHours(hour)
    for time in timers:
        services: List[types.Service] = app.database.getServices(
            chatId=time.chat_id
        )
        Thread(
            target=sendNews,
            args=(app, time.chat_id, services,)
        ).start()


def sendNews(app: Client, chatId: int, services: List[types.Service]):
    style: types.Style = app.database.getStyle(chatId)
    for service in services:
        if not service.max_news:
            config: Union[types.Config, types.Error] = app.database.getConfig(
                chatId=chatId
            )
            service.max_news = config.max_news
        count = 0
        news: dict = getNews(service.url)
        for new in news["entries"]:
            if "published" not in new and "updated" not in new:
                news["entries"].remove(new)
                continue
            published = new.get("published") or new.get("updated")
            if service.lastUpdate == published:
                break
            description = BeautifulSoup(
                new["description"],
                "html.parser"
            ).text.replace("\n\n\n\n", "\n\n\n")
            try:
                text = style.title+new['title']+style.title+"\n"
            except TypeError:
                continue
            if service.tags:
                text += f"{service.tags}\n"
            text += f"{style.hour_and_services}{service.title}» {published}{style.hour_and_services}\n\n"
            text += f"{style.description}{description.strip()}{style.description}\n\n"
            text += f"🌐 [Ler mais!]({new['link']})"
            if len(text) > 4096:
                continue
            app.send_message(
                chat_id=chatId,
                text=text,
                parse_mode="markdown"
            )
            count += 1
            if count == service.max_news:
                break
            sleep(1)
        if len(news["entries"]) > 0:
            firstNews = news["entries"][0]
            published = firstNews.get("published") or firstNews.get("updated")
            app.database.setLastUpdate(
                chatId=chatId,
                urlId=service.url_id,
                lastUpdate=published
            )
