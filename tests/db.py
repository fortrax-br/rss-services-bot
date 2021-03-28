import sys
sys.path.extend(["bot"])
import unittest
import database_new


class Tests(unittest.TestCase):
    db = database_new.crub("sqlite:///test.db")

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
        expected = [(1, 1, 1, "#google", None, 2)]
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


if __name__ == "__main__":
    unittest.main()
