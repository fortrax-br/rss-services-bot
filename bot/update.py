import rss
from extra import getUTC
from time import sleep, strftime, time
from threading import Thread
from bs4 import BeautifulSoup


news: dict = {}


def run(client, *args) -> None:
    lastUpdate: int = None
    while True:
        minutes: int = int(strftime("%M"))
        if (minutes % 5) == 0 and lastUpdate != minutes:
            lastUpdate = minutes
            Thread(target=update, args=(client,)).start()
        sleep(10)


def update(client) -> None:
    global news
    utc = getUTC()
    chats: list = client.database.getChatsByHours(utc)
    for chatId in chats:
        urls: list = client.database.getUserUrls(chatId[0])
        for id, url, limit, lastUpdate, tags in urls:
            if url in news:
                if (time()-news[url][1]) > 10:
                    news[url] = [rss.getNews(url), time()]
            else:
                news[url] = [rss.getNews(url), time()]
            Thread(
                target=sendNews,
                args=(client, id, chatId[0], limit, lastUpdate, tags, news[url][0],)
            ).start()


def sendNews(client, urlId: int, chatId: int, limit: int,
             lastUpdate: str, tags: str, news: dict) -> None:
    count: int = 0
    if not limit:
        limit: int = client.database.getLimit(chatId)
    for new in news["entries"]:
        if count == limit:
            break
        if not lastUpdate:
            pass
        elif lastUpdate == new["published"]:
            break
        try:
            description = BeautifulSoup(new["description"], "html.parser").text
            message: str = f"""**{new['title']}**
{tags}
__{new['published']} usando o serviço de noticias {news['feed']['title']}__

```{description}```

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
