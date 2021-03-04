# RSS bot

Bot para recebimento de noticias atravez do telegram.

## Configuração

Primeiro configure o banco de dados executando o seguinte comando:

```bash
$ mysql -uUSER -pPASSWORD < setup.sql
```

E espere terminar, após fazer isso, é preciso configurar o login do bot, crie um arquivo `config.ini` com o seguinte conteúdo obtido no site https://my.telegram.org e no bot [@BotFather](https://t.me/BotFather):

```ini
[pyrogram]
api_id = API_ID
api_hash = API_HASH
bot_token = BOT_TOKEN
```

E para iniciar é só rodar `python3 bot`.