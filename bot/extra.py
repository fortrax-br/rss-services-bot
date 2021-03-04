from re import findall

async def getChatId(client, message) -> int:
    marked = findall(r"\((.*)\)", message.text)
    if marked:
        message.text = marked[0]
    try:
        return int(message.text)
    except ValueError:
        pass
    if "t.me" in message.text:
        message.text = message.text.split("/")[-1]
    try:
        chat = await client.get_chat(message.text)
        return chat.id
    except:
        pass
    return message.chat.id
