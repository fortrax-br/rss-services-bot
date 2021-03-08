from time import sleep

import rss


stop: bool = False

def run(client, *args) -> None:
    global stop
    while not stop:
        print("Atualizando...")
        urls: list = client.database.getAllUrl()
        for id, url in urls:
            news: dict = rss.getNews(url)
            ok: bool = sendNews(client, id, news)
            if not ok:
                return
        print("Dormindo por 10 segundos...")
        sleep(10)


def sendNews(client, urlId: int, news: dict) -> bool:
    chats: list = client.database.getUrlChats(urlId)
    for chatId, dbId, tags in chats:
        limit: int = client.database.getLimit(chatId)
        count: int = 0
        lastUpdate: int = client.database.getLastUpdate(dbId, urlId)
        for new in news["entries"]:
            if not lastUpdate:
                pass
            elif lastUpdate[0][0] == new["published"] or count == limit:
                break
            try:
                message: str = f"**{new['title']}**\n{tags}\n"
                message += f"__{new['published']} pelo serviço {news['feed']['title']}__\n\n"
                message += f"```{new['description']}```\n\n"
                message += f"[Visitar o site]({new['link']})"
                if len(message) > 4096:
                    continue
                print(f"[{urlId}] Enviando {count}/{limit} para {chatId}...")
                client.send_message(
                    chat_id=chatId,
                    text=message,
                    parse_mode="markdown"
                )
                sleep(0.5)
                count += 1
            except KeyboardInterrupt:
                return False
            except Exception:
                pass
        client.database.setLastUpdate(
            userId=dbId,
            urlId=urlId,
            last=news["entries"][0]["published"]
        )
    return True
