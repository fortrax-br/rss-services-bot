import sys
sys.path.extend(["bot"])
import unittest
import database
import random


class Tests(unittest.TestCase):
    dbFile = str(random.randint(1000, 9999))+".db"
    db = database.crub("sqlite:///" + dbFile)

    def test_01_addChat(self):
        r = self.db.addChat(123456)
        assert r is True

    def test_02_getUserId(self):
        r = self.db.getUserId(123456)
        assert r == 1

    def test_03_addUrl(self):
        r = self.db.addUrl("Google RSS service", "google.com")
        assert r is True

    def test_04_getUrlId(self):
        r1 = self.db.getUrlId("google.com")
        r2 = self.db.getUrlId("google.com")
        assert r1 == r2

    def test_05_addService(self):
        r = self.db.addService(123456, "google.com", "#google", 2)
        assert r is True

    def test_06_getUserServices(self):
        expected = [(1, "Google RSS service", "google.com", "#google", 2, None)]
        r = self.db.getUserServices(123456)
        assert r == expected

    def test_07_addTimer(self):
        r = self.db.addTimer(123456, "10:30")
        assert r is True

    def test_08_getTimers(self):
        expected = [(1, 123456, "10:30")]
        r = self.db.getTimers(123456)
        assert expected == r

    def test_09_getChatsByHours(self):
        expected = [(1, 123456, "10:30")]
        r = self.db.getChatsByHours("10:30")
        assert expected == r

    def test_10_createConfig(self):
        self.db.createConfig(123456)

    def test_11_getConfig(self):
        expected = (1, 123456, 5)
        r = self.db.getConfig(123456)
        assert r == expected

    def test_12_createSession(self):
        self.db.createSession(123456, 654321)

    def test_13_getSession(self):
        expected = (123456, 654321)
        r = self.db.getSession(123456)
        assert expected == r[:2]

    def test_14_setLastUpdate(self):
        self.db.setLastUpdate(123456, 1, "test")

    def test_15_getLastUpdate(self):
        expected = "test"
        r = self.db.getLastUpdate(123456, 1)
        assert expected == r

    def test_16_setDefaultLimit(self):
        self.db.setDefaultLimit(123456, 10)

    def test_17_getDefaultLimit(self):
        expected = 10
        r = self.db.getDefaultLimit(123456)
        assert expected == r

    def test_18_deleteService(self):
        self.db.deleteService(123456, 1)
        r = self.db.getUserServices(123456)
        assert not r

    def test_19_deleteSession(self):
        self.db.deleteSession(123456)
        r = self.db.getSession(123456)
        assert not r

    def test_20_deleteTimer(self):
        self.db.deleteTimer(123456, "10:30")
        r = self.db.getChatsByHours("10:30")
        assert not r

    def test_21_createDefaultStyle(self):
        self.db.createDefaultStyle(123456)
        expected = (123456, "**", "__", "```")
        r = self.db.getStyle(123456)
        assert expected == r

    def test_22_setStyle(self):
        self.db.setStyle(
            123456,
            title="__",
            hour_and_services="```",
            description="**"
        )
        expected = (123456, "__", "```", "**")
        r = self.db.getStyle(123456)
        assert r == expected


if __name__ == "__main__":
    unittest.main()