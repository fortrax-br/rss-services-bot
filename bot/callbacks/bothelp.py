from pyrogram.types import InlineKeyboardMarkup
from ..extra import back
from pyrogram import Client
from pyrogram.types import CallbackQuery


async def botHelp(client: Client, callback: CallbackQuery):
    msg = callback.message
    await client.edit_message_text(
        message_id=msg.message_id,
        chat_id=msg.chat.id,
        text="""Eu tenho os seguintes comandos:

Obs: Tudo entre os `[]` é opcional.

`/add [(N)] url <tags>`
  - N é a quantidade de noticias para ser enviada, url deve ser o link direto do serviço e tags são as que devem aparecer junto com as noticias;

`/limit [N]`
  - N é a quantidade padrão de noticias por serviço, se o comando for executado sem esse argumento ele devolve o limite atual;

`/session @username`
  - @username deve ser substituido pelo nome de usuário do canal/grupo a ser controlado;

`/delsession`
  - Apaga a sessão atual se existir;

`/addtime 8:30`
  - Adiciona uma hora de envio, 8:30 deve ser substituido por esse horário, mas tem uma observação: O horário deve ser em UTC.""",
        parse_mode="markdown",
        reply_markup=InlineKeyboardMarkup([back("menu")])
    )
