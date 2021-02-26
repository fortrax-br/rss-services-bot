from feedparser import parse

def getNews(url: str) -> dict:
    feed = parse(url)
    return feed
