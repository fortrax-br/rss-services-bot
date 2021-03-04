import bot.database, json
conf = json.load(open("bot.json"))
db = bot.database.mysql(**conf["mysql"])
print(db.getAllChats())
print(db.getAllUrl())
db.addService(-12345678, "UOL", "https://uol.com")
print(db.getUserUrls(1))
db.deleteService(1, 2)
