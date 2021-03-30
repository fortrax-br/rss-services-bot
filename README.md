# RSS bot

Bot para recebimento de noticias atravez do telegram de forma totalmente controlável.

## Configuração

Primeiro crie o seu banco de dados postgresql;

Depois instale as bibliotecas que é preciso usando o seguinte comando:

```bash
$ sudo pip3 install -r requirements.txt
```

E por último é preciso configurar o login do bot na conta dele e o login do banco de dados, você vai precisar de algumas coisas que podem ser obtido no site [My Telegram](https://my.telegram.org) e no bot [@BotFather](https://t.me/BotFather) para criar algumas variáveis de ambiente, veja como configurar elas no linux:

```bash
$ export TELEGRAM_API_ID=123456 # O id do seu app no site My Telegram;
$ export TELEGRAM_API_HASH="asdfghjklpoiuytrewqzxcvbnm" # A hash encontrada no mesmo site do id;
$ export BOT_TOKEN="123456:asdfghjkloiuyrec" # E o mais importante, o token do seu bot obtido no Bot Father.
$ export DATABASE_URL="postgresql+psycopg2://user:password@host:port/database"
```

Após ter feito isso você já vai poder usar o bot tranquilamente rodando o comando `python3 bot` nessa pasta.
