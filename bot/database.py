from mysql.connector import connect as myConnect


class mysql:
    connection = None
    cursor = None

    def __init__(self, **kwargs):
        self.mysqlConfig: dict = kwargs
        self.connect()

    # Conexão e execução de códigos no MySql
    def connect(self) -> None:
        self.connection = myConnect(**self.mysqlConfig)
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()
        self.execute(f"USE rssBot;")
        self.execute(f"SET FOREIGN_KEY_CHECKS = 0;")

    def execute(self, cmd: str) -> list:
        self.connection.ping()
        self.cursor.execute(cmd)
        try:
            result: list = self.cursor.fetchall()
        except Exception:
            result: list = []
        return result

    # Comandos
    def addChat(self, chat_id: int) -> bool:
        if self.getUserId(chat_id) != -1:
            return False
        command: str = f"INSERT INTO users VALUES (DEFAULT, '{chat_id}');"
        self.execute(command)
        return True

    def addService(self, chat_id: int, title: str, url: str, tags: list = []) -> bool:
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
        command: str = f"INSERT INTO user_url VALUES (DEFAULT, '{userId}', '{urlId}', "
        if tags:
            command += f"'{tagsStr}'"
        else:
            command += "DEFAULT"
        self.execute(command+");")

    def addUrl(self, title: str, url: str) -> bool:
        if self.getUrlId(url) != -1:
            return False
        command: str = f"INSERT INTO urls VALUES (DEFAULT, '{title}', '{url}');"
        self.execute(command)
        return True

    def createConfig(self, chatId: int) -> bool:
        if self.getConfig(chatId):
            return False
        command: str = f"INSERT INTO config(chat_id) VALUES ('{chatId}');"
        self.execute(command)
        return True

    def deleteService(self, userId: int, urlId: int) -> None:
        command: str = f"DELETE FROM user_url WHERE user_id = '{userId}' AND url_id = '{urlId}'"
        self.execute(command)

    def getAllChats(self) -> list:
        query: str = f"SELECT * FROM users;"
        result: list = self.execute(query)
        return result

    def getAllUrl(self) -> list:
        query: str = f"SELECT id, url FROM urls;"
        result: list = self.execute(query)
        return result

    def getChatTelegramId(self, id: int) -> int:
        query: str = f"SELECT chat_id FROM users WHERE id = {id};"
        result: list = self.execute(query)
        if result:
            return result[0][0]
        return -1

    def getUserId(self, chat_id: int) -> int:
        query: str = f"SELECT id FROM users WHERE chat_id = '{chat_id}';"
        result: list = self.execute(query)
        if result:
            return result[0][0]
        return -1

    def getConfig(self, chatId: int) -> list:
        query: str = f"SELECT max_news, timer FROM config WHERE chat_id = '{chatId}';"
        result: list = self.execute(query)
        return result

    def getLastUpdate(self, userId: int) -> list:
        query: str = f"SELECT last_update FROM config WHERE user_id = '{userId}';"
        result: list = self.execute(query)
        return query

    def getLimit(self, chatId: int) -> int:
        self.createConfig(chatId)
        query: str = f"SELECT max_news FROM config WHERE chat_id = '{chatId}';"
        result: list = self.execute(query)
        return result[0][0]

    def getTimer(self, userId: int) -> int:
        self.createConfig(userId)
        query: str = f"SELECT timer FROM config WHERE user_id='{userId}';"
        result: list = self.execute(query)
        return result[0][0]

    def getUrl(self, userId: int) -> list:
        query: str = f"SELECT urls.title, urls.url FROM user_url, users WHERE user_url.url_id=urls.id AND user_url.user_id={userId};"
        result: list = self.execute(query)
        return result

    def getUrlChats(self, urlId: int) -> list:
        query: str = f"SELECT user_id FROM user_url WHERE url_id='{urlId}';"
        result: list = self.execute(query)
        return result

    def getUrlId(self, url: str) -> int:
        query: str = f"SELECT id FROM urls WHERE url = '{url}';"
        result: list = self.execute(query)
        if result:
            return result[0][0]
        return -1

    def getUserUrls(self, userId: int) -> list:
        query: str = f"SELECT urls.* FROM urls, user_url WHERE user_url.user_id='{userId}' AND user_url.url_id=urls.id;"
        result: list = self.execute(query)
        return result

    def setLastUpdate(self, userId: int, last: str) -> None:
        self.createConfig(userId)
        command: str = f"UPDATE config SET last_update = '{last}' WHERE user_id = '{userId}';"
        self.execute(command)

    def setLimit(self, chatId: int, limit: int) -> None:
        self.createConfig(chatId)
        command: str = f"UPDATE config SET max_news = '{limit}' WHERE chat_id = '{chatId}';"
        self.execute(command)

    def setTimer(self, chat_id: int, timer: int) -> None:
        self.createConfig(userId)
        userId: int = self.getUserId(chat_id)
        command: str = f"UPDATE config SET timer = '{timer}' WHERE user_id='{userId}';"
        self.execute(command)
