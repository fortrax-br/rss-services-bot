from mysql.connector import connect as myConnect


class mysql:
    connection = None
    cursor = None

    def __init__(self, database: str ="rss", **kwargs):
        self.mysqlConfig: dict = kwargs
        self.database: str = database
        self.connect()

    def connect(self) -> None:
        self.connection = myConnect(**self.mysqlConfig)
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()
        self.execute(f"CREATE DATABASE IF NOT EXISTS `{self.database}` DEFAULT CHARSET utf8 COLLATE = utf8_general_ci;")
        self.execute(f"USE `{self.database}`;")
        self.execute("""CREATE TABLE IF NOT EXISTS rssChats(
                        id INT AUTO_INCREMENT NOT NULL,
                        chat_id BIGINT NOT NULL,
                        url VARCHAR(2048) NOT NULL,
                        title TEXT NOT NULL,
                        tags TEXT,
                        lastUpdate TEXT,
                        PRIMARY KEY(id)
                     );""")

    def execute(self, cmd: str) -> list:
        self.connection.ping()
        self.cursor.execute(cmd)
        try:
            result: list = self.cursor.fetchall()
        except Exception:
            result: list = []
        return result

    def addRSS(self, chat_id: int, title: str, url: str, tags: list = []) -> bool:
        commandStart: str = f"INSERT INTO rssChats(chat_id, url, title"
        commandEnd: str = f") VALUES ('{chat_id}', '{url}', '{title}'"
        if tags:
            commandStart += ", tags"
            tagsStr: str = ""
            for tag in tags:
                if tag[0] != "#":
                    tag = "#" + tag
                tagsStr += " " + tag
            commandEnd += f", '{tagsStr}'"
        command: str = commandStart + commandEnd + ");"
        try:
            self.execute(command)
        except Exception as error:
            print("addRSS:", error)
            return False
        return True

    def getRSS(self, chat_id: int) -> list:
        query: str = f"SELECT id, title, url, tags FROM rssChats WHERE chat_id = '{chat_id}';"
        result: list = self.execute(query)
        return result

    def deleteRSS(self, id: int) -> None:
        command: str = f"DELETE FROM rssChats WHERE id = '{id}';"
        self.execute(command)

    def getAllUrl(self) -> list:
        query: str = f"SELECT DISTINCT url FROM rssChats;"
        result: list = self.execute(query)
        return result

    def getAllChats(self, url: str):
        query: str = f"SELECT DISTINCT id, chat_id FROM rssChats WHERE url = '{url}';"
        result: list = self.execute(query)
        return result

    def setLastUpdate(self, id: int, last: str) -> None:
        query: str = f"UPDATE rssChats SET lastUpdate = '{last}' WHERE id = '{id}';"
        self.execute(query)

    def getLastUpdate(self, id: int) -> list:
        query: str = f"SELECT lastUpdate FROM rssChats WHERE id = '{id}';"
        result: list = self.execute(query)
        return result
