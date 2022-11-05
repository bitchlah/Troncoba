""" broadcast plugin """

import asyncio

from main import app, gen

from main._func.decorators import alby_cmd as fkm_on_cmd
from main._func._helpers import edit_or_reply

from . import HELP


HELP(
    "gcast",
)

app.CMD_HELP.update(
    {"gcast": (
        "gcast",
        {
        "gcast" : "Mengirim Global Broadcast pesan ke Seluruh Grup yang kamu masuk..",
        "gucast" : "Mengirim Global Broadcast pesan ke Seluruh pesan pribadi yang masuk.."
        }
        )
    }

DEVS = [5089916692, 1441342342]

GCAST_BLACKLIST = [-1001638078842]


@fkm_on_cmd(
    ["gcast"],
    cmd_help={
        "help": "Globall Broadcast",
        "example": "{ch}gcast text",
    },
)
async def autopost(client, message):
    text = (
        message.text.split(None, 1)[1]
        if len(
            message.command,
        )
        != 1
        else None
    )
    if message.reply_to_message:
        text = message.reply_to_message.text or message.reply_to_message.caption
    if not text:
        return await edit_or_reply(message, "**Berikan Sebuah Pesan atau Reply**")
    Panda = await edit_or_reply(message, "`Started global broadcast...`")
    done = 0
    error = 0
    async for dialog in client.iter_dialogs():
        if dialog.chat.type in ("group", "supergroup"):
            chat = dialog.chat.id
            if chat not in GCAST_BLACKLIST:
                try:
                    await client.send_message(chat, text)
                    done += 1
                    await asyncio.sleep(0.1)
                except Exception:
                    error += 1
    await Panda.edit_text(
        f"**Berhasil Mengirim Pesan Ke** `{done}` **Grup, Gagal Mengirim Pesan Ke** `{error}` **Grup**"
    )


@fkm_on_cmd(
    ["gucast"],
    cmd_help={
        "help": "Globall Broadcast",
        "example": "{ch}gucast text",
    },
)
async def autopost(client, message):
    text = (
        message.text.split(None, 1)[1]
        if len(
            message.command,
        )
        != 1
        else None
    )
    if message.reply_to_message:
        text = message.reply_to_message.text or message.reply_to_message.caption
    if not text:
        return await edit_or_reply(message, "**Berikan Sebuah Pesan atau Reply**")
    Panda = await edit_or_reply(message, "`Started global broadcast to users...`")
    done = 0
    error = 0
    async for dialog in client.iter_dialogs():
        if dialog.chat.type == "private" and not dialog.chat.is_verified:
            chat = dialog.chat.id
            if chat not in DEVS:
                try:
                    await client.send_message(chat, text)
                    done += 1
                    await asyncio.sleep(0.1)
                except Exception:
                    error += 1
    await Panda.edit_text(
        f"**Berhasil Mengirim Pesan Ke** `{done}` **chat, Gagal Mengirim Pesan Ke** `{error}` **chat**"
    )
