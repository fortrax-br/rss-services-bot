import rss
from extra import getUTC
from time import sleep, strftime
from threading import Thread


news: dict = {}


def run(client, *args) -> None:
    lastUpdate: int = None
    while True:
        minutes: int = int(strftime("%M"))
        if (minutes / 10).is_integer() and lastUpdate != minutes:
            lastUpdate = minutes
            Thread(target=update, args=(client,)).start()
        sleep(5)


def update(client) -> None:
    time = getUTC()
    chats: list = client.database.getChatsByHours(time)
    print(time, chats)
    for chatId in chats:
        urls: list = client.database.getUserUrls(chatId[0])
        for id, url, limit, lastUpdate, tags in urls:
            news: dict = rss.getNews(url)
            Thread(
                target=sendNews,
                args=(client, id, chatId[0], limit, lastUpdate, tags, news,)
            ).start()


def sendNews(client, urlId: int, chatId: int, limit: int,
             lastUpdate: str, tags: str, news: dict) -> None:
    count: int = 0
    if not limit:
        limit: int = client.database.getLimit(chatId)
    print(lastUpdate)
    for new in news["entries"]:
        if count == limit:
            break
        if not lastUpdate:
            pass
        elif lastUpdate == new["published"]:
            break
        try:
            message: str = f"""**{new['title']}**
{tags}
__{new['published']} usando o serviço de noticias {news['feed']['title']}__

```{new['description']}```

🌐[Visitar o site]({new['link']})"""
            if len(message) > 4096:
                continue
            client.send_message(
                chat_id=chatId,
                text=message,
                parse_mode="markdown"
            )
            sleep(1)
            count += 1
        except Exception:
            pass
    client.database.setLastUpdate(
        chatId=chatId,
        urlId=urlId,
        last=news["entries"][0]["published"]
    )
