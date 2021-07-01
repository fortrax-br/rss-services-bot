from time import time
from typing import Union, List
from .types import (
    Service, Session, User, Url,
    Timer, Error, Config, Style
)
from sqlalchemy import (
    create_engine, text, MetaData, Table,
    Column, String, Integer, BigInteger,
    ForeignKey
)


class crub:
    def __init__(self, url: str):
        self.db = create_engine(url, echo=False)
        self.conn = self.db.connect()
        self.meta = MetaData(self.db)
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
        self.meta.create_all()

    def getUser(self, chatId: int) -> Union[User, Error]:
        query = self.users.select().where(self.users.c.chat_id == chatId)
        result: tuple = query.execute().fetchone()
        if result:
            return User(*result)
        return Error("Não foi possivél obter usuário")

    def addUser(self, chatId: int) -> bool:
        self.users.insert().values(chat_id=chatId).execute()
        return True

    def addUrl(self, title: str, url: str) -> bool:
        self.urls.insert().values(title=title, url=url).execute()
        return True

    def getUrl(self, url: str) -> Union[Url, Error]:
        command = self.urls.select().where(self.urls.c.url == url)
        result: tuple = command.execute().fetchone()
        if result:
            return Url(*result)
        return Error("Url inexistente")

    def getServices(self, chatId: int) -> List[Service]:
        command = text(
            f"SELECT urls.*, user_url.tags, user_url.max_news, user_url.lastupdate \
                FROM user_url, urls, users \
                WHERE user_url.url_id=urls.id \
                    AND user_url.user_id=users.id \
                    AND users.chat_id={chatId};"
        )
        result = self.conn.execute(command).fetchall()
        return list(map(lambda item: Service(*item), result))

    def addService(self, chatId: int, url: str,
                   tags: str, limit: int = 0) -> bool:
        url: int = self.getUrl(url)
        user: int = self.getUser(chatId)
        self.user_url.insert().values(
            user_id=user.id,
            url_id=url.id,
            tags=tags,
            max_news=limit
        ).execute()
        return True

    def getTimers(self, chatId) -> List[Timer]:
        command = self.timers.select().where(self.timers.c.chat_id == chatId)
        result = command.execute().fetchall()
        return list(map(lambda item: Timer(*item), result))

    def addTimer(self, chatId: int, hour: str) -> Union[bool, Error]:
        exists = any(filter(
            lambda time: time.timer == hour,
            self.getTimers(chatId)
        ))
        if exists:
            return Error("Este horário já existe!")
        self.timers.insert().values(chat_id=chatId, timer=hour).execute()
        return True

    def getUsersByHours(self, hour: str) -> List[Timer]:
        command = self.timers.select().where(self.timers.c.timer == hour)
        result = command.execute().fetchall()
        return list(map(lambda item: Timer(*item), result))

    def createConfig(self, chatId: int):
        self.config.insert().values(chat_id=chatId).execute()

    def getConfig(self, chatId: int) -> Union[Config, Error]:
        command = self.config.select().where(self.config.c.chat_id == chatId)
        config = command.execute().fetchone()
        if not config:
            return Error("A configuração não foi encontrada")
        return Config(*config)

    def createSession(self, chatId: int, controlId: int):
        self.sessions.insert().values(
            chat_id=chatId,
            control_id=controlId,
            started=int(time())
        ).execute()

    def getSession(self, chatId: int) -> Union[Session, Error]:
        command = self.sessions.select().where(
            self.sessions.c.chat_id == chatId
        )
        session = command.execute().fetchone()
        if not session:
            return Error("Nenhuma sessão econtrada")
        return Session(*session)

    def setLastUpdate(self, chatId: int, urlId: int, lastUpdate: str):
        user = self.getUser(chatId)
        self.user_url.update().values(
            lastupdate=lastUpdate
        ).where(
            self.user_url.c.user_id == user.id,
            self.user_url.c.url_id == urlId
        ).execute()

    def getService(self, chatId: int, urlId: int) -> Union[Service, Error]:
        command = self.user_url.select().select_from(
            self.user_url.join(
                self.users,
                self.users.c.chat_id == chatId,
                self.users.c.id == self.user_url.c.user_id,
                self.user_url.c.url_id == urlId
            )
        )
        service = command.execute().fetchone()
        if not service:
            return Error("Serviço não encontrado para este usuário")
        return Service(*service)

    def setDefaultLimit(self, chatId: int, limit: int):
        self.config.update().values(max_news=limit).where(
            self.config.c.chat_id == chatId
        ).execute()

    def deleteService(self, chatId: int, urlId: int):
        user = self.getUser(chatId)
        self.user_url.delete().where(
            self.user_url.c.url_id == urlId,
            self.user_url.c.user_id == user.id
        ).execute()

    def deleteSession(self, chatId: int):
        self.sessions.delete().where(
            self.sessions.c.chat_id == chatId
        ).execute()

    def deleteTimer(self, chatId: int, timer: str):
        self.timers.delete().where(
            self.timers.c.chat_id == chatId,
            self.timers.c.timer == timer
        ).execute()

    def createDefaultStyle(self, chatId: int):
        self.styles.insert().values(chat_id=chatId).execute()

    def setStyle(self, chatId: int, **kwargs) -> None:
        self.styles.update().values(**kwargs).where(
            self.styles.c.chat_id == chatId
        ).execute()

    def getStyle(self, chatId: int) -> Style:
        command = self.styles.select().where(self.styles.c.chat_id == chatId)
        style = command.execute().fetchone()
        return Style(*style)
