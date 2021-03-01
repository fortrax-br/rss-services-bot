from mysql.connector import connect as myConnect


class mysql:
    connection = None
    cursor = None

    def __init__(self, **kwargs):
        self.mysqlConfig: dict = kwargs
        self.connect()

    def connect(self) -> None:
        self.connection = myConnect(**self.mysqlConfig)
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()
        self.execute(f"USE rssBot;")

    def execute(self, cmd: str) -> list:
        self.connection.ping()
        self.cursor.execute(cmd)
        try:
            result: list = self.cursor.fetchall()
        except Exception:
            result: list = []
        return result

    def addService(self, chat_id: int, title: str, url: str, tags: list = []) -> bool:
        self.addURL(title, url)
        urlId: int = self.findURL(url)
        userId: int = self.getID(chat_id)
        if userId == -1:
            self.addChat(chat_id)
            userId: int = self.getID(chat_id)
        tagsStr: str = ""
        for tag in tags:
            if tag == "#":
                continue
            elif tag[0] != "#":
                tag = "#" + tag
            tagsStr += " " + tag
        command: str = f"INSERT INTO user_url VALUES (DEFAULT, '{userId}', '{urlId}');"
        self.execute(command)

    def addURL(self, title: str, url: str) -> bool:
        if self.findURL(url) != -1:
            return False
        command: str = f"INSERT INTO urls VALUES (DEFAULT, '{title}', '{url}');"
        self.execute(command)
        return True

    def addChat(self, chat_id: int) -> bool:
        if self.getID(chat_id) != -1:
            return False
        command: str = f"INSERT INTO users VALUES (DEFAULT, '{chat_id}');"
        self.execute(command)
        return True

    def getID(self, chat_id: int) -> int:
        query: str = f"SELECT id FROM users WHERE chat_id = '{chat_id}';"
        result: list = self.execute(query)
        if result:
            return result[0][0]
        return -1

    def getChat(self, id: int) -> int:
        query: str = f"SELECT chat_id FROM users WHERE id = {id};"
        result: list = self.execute(query)
        if result:
            return result[0][0]
        return -1

    def findURL(self, url: str) -> int:
        query: str = f"SELECT id FROM urls WHERE url = '{url}';"
        result: list = self.execute(query)
        if result:
            return result[0][0]
        return -1

    def getURL(self, id: int) -> list:
        query: str = f"SELECT urls.title, urls.url FROM user_url, users WHERE user_url.url_id=urls.id AND user_url.user_id={id};"
        result: list = self.execute(query)
        return result

    def deleteRSS(self, userId: int, urlId: int) -> None:
        command: str = f"DELETE FROM user_url WHERE user_id = '{userId}' AND url_id = '{urlId}'"
        self.execute(command)

    def getAllUrl(self) -> list:
        query: str = f"SELECT url FROM urls;"
        result: list = self.execute(query)
        return result

    def getAllChats(self, urlId: int) -> list:
        query: str = f"SELECT user_id FROM user_url WHERE url_id='{urlId}';"
        result: list = self.execute(query)
        return result

    def getConfig(self, userId: int) -> list:
        query: str = f"SELECT max_news, timer WHERE user_id = '{userId}';"
        result: list = self.execute(query)
        return result

    def createConfig(self, userId: int) -> bool:
        if getConfig(userId):
            return False
        command: str = f"INSERT INTO config(user_id) VALUES ('{userId}');"
        self.execute(command)
        return True

    def setLastUpdate(self, userId: int, last: str) -> None:
        self.createConfig(userId)
        command: str = f"UPDATE config SET last_update = '{last}' WHERE user_id = '{userId}';"
        self.execute(command)

    def getLastUpdate(self, userId: int) -> list:
        query: str = f"SELECT last_update FROM config WHERE user_id = '{userId}';"
        result: list = self.execute(query)
        return query

    def setLimit(self, userId: int, limit: int) -> None:
        createConfig(userId)
        command: str = f"UPDATE config SET max_news = '{limit}' WHERE user_id = '{userId}';"
        self.execute(command)

    def getLimit(self, userId: int) -> list:
        self.createConfig(userId)
        query: str = f"SELECT max_news FROM config WHERE user_id = '{userId}';"
        result: str = self.execute(query)
        return result