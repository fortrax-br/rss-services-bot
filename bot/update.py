from time import sleep
import rss

news: dict = {}
limit = 20

def run(app, *args):
    while True:
        print("Atualizando...")
        urls = app.database.getAllUrl()
        for url in urls:
            url = url[0]
            news[url] = rss.getNews(url)
            if len(news[url]) > limit:
                news[url] = news[url][:limit]
            sendNews(app, url, news[url])
        sleep(60)

def sendNews(app, url: str, news: dict):
    chats: list = app.database.getAllChats(url)
    for id, chat_id in chats:
        lastUpdate: int = app.database.getLastUpdate(id)
        count = 0
        for new in news["entries"]:
            print(lastUpdate[0][0], new["published"], lastUpdate[0][0]==new["published"])
            if not lastUpdate:
                pass
            elif lastUpdate[0][0] == new["published"] or count == limit:
                break
            try:
                app.send_message(
                    chat_id=chat_id,
                    text=f"**{new['title']}**\n__{new['published']}__\n\n```{new['description']}```\n\n[Clique e saiba mais.]({new['link']})",
                    parse_mode="markdown"
                )
                sleep(0.5)
                count += 1
            except KeyboardInterrupt:
                return
            except:
                pass
        app.database.setLastUpdate(id, news["entries"][0]["published"])
