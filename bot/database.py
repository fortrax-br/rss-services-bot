from sqlalchemy import (create_engine, MetaData, Table, text,
                        Column, String, Integer, BigInteger,
                        ForeignKey)
from time import time


class crub:
    def __init__(self, url: str):
        self.db = create_engine(url, echo=False)
        self.conn = self.db.connect()
        self.meta = MetaData()
        self.users = Table(
            "users",
            self.meta,
            Column("id", Integer, autoincrement=True, primary_key=True),
            Column("chat_id", BigInteger, unique=True)
        )
        self.urls = Table(
            "urls",
            self.meta,
            Column("id", Integer, autoincrement=True, primary_key=True),
            Column("title", String(1024)),
            Column("url", String(1024), unique=True)
        )
        self.user_url = Table(
            "user_url",
            self.meta,
            Column("id", Integer, autoincrement=True, primary_key=True),
            Column("user_id", ForeignKey("users.id")),
            Column("url_id", ForeignKey("urls.id")),
            Column("tags", String(1024)),
            Column("lastupdate", String(512)),
            Column("max_news", Integer)
        )
        self.timers = Table(
            "timers",
            self.meta,
            Column("id", Integer, autoincrement=True, primary_key=True),
            Column("chat_id", BigInteger()),
            Column("timer", String(5))
        )
        self.config = Table(
            "config",
            self.meta,
            Column("id", Integer, autoincrement=True, primary_key=True),
            Column("chat_id", BigInteger, unique=True),
            Column("max_news", Integer, server_default="5")
        )
        self.sessions = Table(
            "sessions",
            self.meta,
            Column("chat_id", BigInteger, unique=True),
            Column("control_id", BigInteger),
            Column("started", BigInteger)
        )
        self.styles = Table(
            "styles",
            self.meta,
            Column("chat_id", BigInteger, unique=True),
            Column("title", String(5), server_default="**"),
            Column("hour_and_services", String(5), server_default="__"),
            Column("description", String(5), server_default="```")
        )
        self.meta.create_all(self.db)

    def getUserId(self, chatId: int) -> int:
        query = self.users.select().where(self.users.c.chat_id == chatId)
        result: tuple = self.conn.execute(query).fetchone()
        if result:
            return result[0]
        return -1

    def addChat(self, chatId: int) -> bool:
        command = self.users.insert().values(chat_id=chatId)
        self.conn.execute(command)
        return True

    def addUrl(self, title: str, url: str) -> bool:
        command = self.urls.insert().values(title=title, url=url)
        self.conn.execute(command)
        return True

    def getUrlId(self, url: str) -> int:
        command = self.urls.select().where(self.urls.c.url == url)
        result: tuple = self.conn.execute(command).fetchone()
        if result:
            return result[0]
        return -1

    def getUserServices(self, chatId: int) -> list:
        command = text(f"SELECT urls.*, user_url.tags, user_url.max_news, lastupdate \
                        FROM user_url, urls, users \
                        WHERE user_url.url_id=urls.id \
                          AND user_url.user_id=users.id \
                          AND users.chat_id={chatId};")
        result = self.conn.execute(command)
        return result.fetchall()

    def addService(self, chatId: int, url: str,
                   tags: str, limit: int = 0) -> bool:
        urlId: int = self.getUrlId(url)
        userId: int = self.getUserId(chatId)
        command = self.user_url.insert().values(
            user_id=userId,
            url_id=urlId,
            tags=tags,
            max_news=limit
        )
        self.conn.execute(command)
        return True

    def getTimers(self, chatId) -> list:
        command = self.timers.select().where(self.timers.c.chat_id == chatId)
        result = self.conn.execute(command).fetchall()
        return result

    def addTimer(self, chatId: int, hour: str) -> bool:
        exists = [True for timer in self.getTimers(chatId) if timer[1] == hour]
        if exists:
            return False
        command = self.timers.insert().values(chat_id=chatId, timer=hour)
        self.conn.execute(command)
        return True

    def getChatsByHours(self, hour: str) -> list:
        command = self.timers.select().where(self.timers.c.timer == hour)
        result = self.conn.execute(command).fetchall()
        return result

    def createConfig(self, chatId: int) -> None:
        command = self.config.insert().values(chat_id=chatId)
        self.conn.execute(command)

    def getConfig(self, chatId: int) -> tuple:
        command = self.config.select().where(self.config.c.chat_id == chatId)
        result = self.conn.execute(command).fetchone()
        if result:
            return result
        return ()

    def createSession(self, chatId: int, controlId: int) -> None:
        command = self.sessions.insert().values(
            chat_id=chatId,
            control_id=controlId,
            started=int(time())
        )
        self.conn.execute(command)

    def getSession(self, chatId: int) -> tuple:
        command = self.sessions.select().where(
            self.sessions.c.chat_id == chatId
        )
        result = self.conn.execute(command).fetchone()
        return result

    def setLastUpdate(self, chatId: int, urlId: int, lastUpdate: str) -> None:
        userId = self.getUserId(chatId)
        command = self.user_url.update().values(
            lastupdate=lastUpdate
        ).where(
            self.user_url.c.user_id == userId,
            self.user_url.c.url_id == urlId
        )
        self.conn.execute(command)

    def getLastUpdate(self, chatId: int, urlId: int) -> str:
        command = self.user_url.select().select_from(
            self.user_url.join(
                self.users,
                self.users.c.chat_id == chatId,
                self.users.c.id == self.user_url.c.user_id,
                self.user_url.c.url_id == urlId
            )
        )
        result = self.conn.execute(command).fetchone()
        if result:
            return result[4]
        return ""

    def setDefaultLimit(self, chatId: int, limit: int) -> None:
        command = self.config.update().values(
            max_news=limit
        ).where(self.config.c.chat_id == chatId)
        self.conn.execute(command)

    def getDefaultLimit(self, chatId: int) -> int:
        config = self.getConfig(chatId)
        return config[2]

    def deleteService(self, chatId: int, urlId: int) -> None:
        userId = self.getUserId(chatId)
        command = self.user_url.delete().where(
            self.user_url.c.url_id == urlId,
            self.user_url.c.user_id == userId
        )
        self.conn.execute(command)

    def deleteSession(self, chatId: int) -> None:
        command = self.sessions.delete().where(
            self.sessions.c.chat_id == chatId
        )
        self.conn.execute(command)

    def deleteTimer(self, chatId: int, timer: str) -> None:
        command = self.timers.delete().where(self.timers.c.timer == timer)
        self.conn.execute(command)

    def createDefaultStyle(self, chatId: int) -> None:
        command = self.styles.insert().values(chat_id=chatId)
        self.conn.execute(command)

    def setStyle(self, chatId: int, **kwargs) -> None:
        command = self.styles.update().values(**kwargs).where(
            self.styles.c.chat_id == chatId
        )
        self.conn.execute(command)

    def getStyle(self, chatId: int) -> tuple:
        command = self.styles.select().where(
            self.styles.c.chat_id == chatId
        )
        result = self.conn.execute(command).fetchone()
        return result
