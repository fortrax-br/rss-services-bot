# RSS bot

Bot para recebimento de noticias atravez do telegram de forma totalmente controlável.

## Configuração

Primeiro configure o banco de dados executando o seguinte comando:

!! Atenção !! Esté comando apaga o banco de dados rssBot para que ele seja recriado do zero
```bash
$ mysql -uUSER -pPASSWORD -hURL_SERVIDOR < setup.sql
```

Depois instale as bibliotecas que é preciso usando o seguinte comando:

```bash
$ sudo pip3 install -r requirements.txt
```

E por último é preciso configurar o login do bot na conta dele e o login do banco de dados(MySQL), você vai precisar de algumas coisas que podem ser obtido no site [My Telegram](https://my.telegram.org) e no bot [@BotFather](https://t.me/BotFather) para criar algumas variáveis de ambiente, veja como configurar elas no linux:


```bash
$ export MYSQL_USER=jorgin # Qualquer usuário que tenha as permissões básicas de leitura, atualização e remoção de dados;
$ export MYSQL_PASSWORD=jorgin123 # A senha do usuário usado;
$ export MYSQL_HOST=localhost # O endereço do seu servidor, se não for informado ele usa o localhost;
$ export MYSQL_PORT=3306 # A porta de conexão, se não for informada ele usa a 3306;
$ export TELEGRAM_API_ID=123456 # O id do seu app no site My Telegram;
$ export TELEGRAM_API_HASH="asdfghjklpoiuytrewqzxcvbnm" # A hash encontrada no mesmo site do id;
$ export BOT_TOKEN="123456:asdfghjkloiuyrec" # E o mais importante, o token do seu bot obtido no Bot Father.
```

Após ter feito isso você já vai poder usar o bot tranquilamente rodando o comando `python3 bot` nessa pasta.
