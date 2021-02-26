from xml.dom.minidom import parse as xmlparse

file = xmlparse(open("news.xml"))

for news in file.getElementsByTagName("item"):
    title = news.getElementsByTagName("title")[0].firstChild.data
    description = news.getElementsByTagName("description")[0].firstChild.data
    print(f"Titulo: \033[1m{title}\033[m\nDescrição:\n\033[4m{description}\033[m\n")
