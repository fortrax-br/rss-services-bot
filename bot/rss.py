from feedparser import parse


def getNews(url: str) -> dict:
    feed: dict = parse(url)
    return feed
