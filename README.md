# RSS bot

Bot para recebimento de noticias atravez do telegram de forma totalmente controlável.

## Configuração

Primeiro configure o banco de dados executando o seguinte comando:

!! Atenção !! Esté comando apaga o banco de dados rssBot para que ele seja recriado do zero
```bash
$ mysql -uUSER -pPASSWORD < setup.sql
```

Depois instale as bibliotecas que é preciso usando o seguinte comando:

```bash
$ sudo pip3 install -r requirements.txt
```

E espere terminar, após fazer isso, é preciso configurar o login do bot, crie um arquivo `config.ini` com o seguinte conteúdo obtido no site https://my.telegram.org e no bot [@BotFather](https://t.me/BotFather):

```ini
[pyrogram]
api_id = API_ID
api_hash = API_HASH
bot_token = BOT_TOKEN
```

Logo após isso é preciso criar um arquivo `bot.json` para a configuração do banco de dados da seguinte forma:

```json
{
    "mysql": {
        "user": "Nome de usuário do banco de dados",
        "password": "A senha dele",
        "host": "Onde ele está",
        "port": "(opcional) a porte de conexão sem usar aspas"
    }
}
```

Após ter feito isso você já vai poder usar o bot tranquilamente rodando o comando `python3 bot` nessa pasta.