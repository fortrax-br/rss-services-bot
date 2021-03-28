import database

db = database.crub("sqlite:///test.db")

c=db.user_url.select().select_from(
    db.user_url.join(
        db.users,
        db.users.c.chat_id == 123456,
        db.user_url.c.user_id == db.users.c.id,
    ),
)
print(c)
