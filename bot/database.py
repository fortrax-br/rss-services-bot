from time import time
from mysql.connector import connect as mySQL
from os import environ


class mysql:
    connection = None
    cursor = None

    def __init__(self, **kwargs):
        self.mysqlConfig: dict = kwargs
        self.connect()

    def connect(self) -> None:
        self.connection = mySQL(**self.mysqlConfig)
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()
        self.database = environ.get("MYSQL_DATABASE", "rssBot")
        self.execute("USE " + self.database + ";")
        self.execute("SET FOREIGN_KEY_CHECKS = 0;")

    def execute(self, cmd: str, err: bool = False) -> list:
        try:
            self.connection.ping()
            self.cursor.execute(cmd)
        except Exception as error:
            if not err:
                self.connect()
                self.execute(cmd, err=True)
            else:
                raise error
        try:
            result: list = self.cursor.fetchall()
            self.connection.commit()
        except Exception:
            result: list = []
        return result

    def addChat(self, chat_id: int) -> bool:
        if self.getUserId(chat_id) != -1:
            return False
        command: str = f"INSERT INTO users VALUES (DEFAULT, '{chat_id}');"
        self.execute(command)
        return True

    def addService(self, chat_id: int, title: str, url: str,
                   tags: list = [], limit: int = 0) -> bool:
        self.addUrl(title, url)
        urlId: int = self.getUrlId(url)
        self.addChat(chat_id)
        userId: int = self.getUserId(chat_id)
        if (urlId, url,) in self.getUserUrls(userId):
            return
        tagsStr: str = ""
        for tag in tags:
            if tag == "#":
                continue
            elif tag[0] != "#":
                tag = "#" + tag
            tagsStr += " " + tag
        command: str = f"INSERT INTO user_url(user_id, url_id, tags, max_news) \
            VALUES ('{userId}', '{urlId}', "
        if tags:
            command += f"'{tagsStr.strip()}'"
        else:
            command += "DEFAULT"
        if limit:
            command += f", '{limit}'"
        else:
            command += ", DEFAULT"
        self.execute(command+");")

    def addTimer(self, chatId: int, hour: str) -> bool:
        if (hour, ) in self.getTimers(chatId):
            return False
        command: str = f"INSERT INTO timers VALUES ( \
            DEFAULT, '{chatId}', '{hour}');"
        self.execute(command)
        return True

    def addUrl(self, title: str, url: str) -> bool:
        if self.getUrlId(url) != -1:
            return False
        command: str = f"INSERT INTO urls VALUES ( \
            DEFAULT, '{title}', '{url}');"""
        self.execute(command)
        return True

    def createConfig(self, chatId: int) -> bool:
        if self.getConfig(chatId):
            return False
        command: str = f"INSERT INTO config(chat_id) VALUES ('{chatId}');"
        self.execute(command)
        return True

    def createSession(self, chatId: int, controlId: int) -> bool:
        session, _ = self.getSession(chatId)
        if session != -1:
            return False
        command: str = f"INSERT INTO sessions VALUES ( \
            '{chatId}', '{controlId}', '{int(time())}');"
        self.execute(command)
        return True

    def deleteService(self, chatId: int, urlId: int) -> None:
        userId: int = self.getUserId(chatId)
        command: str = f"DELETE FROM user_url \
        WHERE \
            user_id = '{userId}' AND url_id = '{urlId}';"
        self.execute(command)

    def deleteSession(self, chatId: int) -> None:
        command: str = f"DELETE FROM sessions WHERE chat_id='{chatId}';"
        self.execute(command)

    def deleteTimer(self, chatId: int, timer: str) -> None:
        command: str = f"DELETE FROM timers WHERE chat_id='{chatId}' \
            AND timer='{timer}';"
        self.execute(command)

    def getTimers(self, chatId: int) -> list:
        query: str = f"SELECT timer FROM timers WHERE chat_id='{chatId}';"
        result: list = self.execute(query)
        return result

    def getChatsByHours(self, hour: str) -> list:
        query: str = f"SELECT chat_id FROM timers WHERE timer='{hour}';"
        result: list = self.execute(query)
        return result

    def getUserId(self, chat_id: int) -> int:
        query: str = f"SELECT id FROM users WHERE chat_id = '{chat_id}';"
        result: list = self.execute(query)
        if result:
            return result[0][0]
        return -1

    def getConfig(self, chatId: int) -> tuple:
        query: str = f"SELECT max_news FROM config \
            WHERE chat_id = '{chatId}';"
        result: list = self.execute(query)
        if result:
            return result[0]
        else:
            return ()

    def getLastUpdate(self, userId: int, urlId: int) -> list:
        query: str = f"SELECT last_update FROM user_url WHERE \
            user_id = '{userId}' AND \
            url_id = '{urlId}';"
        result: list = self.execute(query)
        return result

    def getLimit(self, chatId: int) -> int:
        self.createConfig(chatId)
        query: str = f"SELECT max_news FROM config WHERE chat_id = '{chatId}';"
        result: list = self.execute(query)
        if result:
            return result[0][0]
        return 5

    def getSession(self, chatId: int) -> [int, int]:
        query: str = f"SELECT control_id, started FROM sessions WHERE \
            chat_id='{chatId}';"
        result: list = self.execute(query)
        if result:
            return result[0]
        return -1, 0

    def getUrlId(self, url: str) -> int:
        query: str = f"SELECT id FROM urls WHERE url = '{url}';"
        result: list = self.execute(query)
        if result:
            return result[0][0]
        return -1

    def getUserUrls(self, chatId: int) -> list:
        userId: int = self.getUserId(chatId)
        query: str = f"SELECT urls.id, urls.url, user_url.max_news, user_url.last_update, \
            user_url.tags FROM urls, user_url WHERE \
            user_url.user_id='{userId}' AND \
            user_url.url_id=urls.id;"
        result: list = self.execute(query)
        return result

    def getUserUrlsSimple(self, chatId: int) -> list:
        userId: int = self.getUserId(chatId)
        query: str = f"SELECT urls.id, urls.title, urls.url, user_url.max_news, \
            user_url.tags FROM urls, user_url WHERE \
            user_url.user_id='{userId}' AND \
            user_url.url_id=urls.id;"
        result: list = self.execute(query)
        return result

    def setLastUpdate(self, chatId: int, urlId: int, last: str) -> None:
        self.createConfig(chatId)
        userId: int = self.getUserId(chatId)
        command: str = f"UPDATE user_url SET last_update = '{last}' WHERE \
            user_id = '{userId}' AND \
            url_id = '{urlId}';"
        self.execute(command)

    def setLimit(self, chatId: int, limit: int) -> None:
        self.createConfig(chatId)
        command: str = f"UPDATE config SET max_news = '{limit}' WHERE \
            chat_id = '{chatId}';"
        self.execute(command)
