""" broadcast plugin """

from pyrogram.types import Message
from pyrogram.enums import ChatType
from pyrogram.errors import (
    PeerIdInvalid,
    ChatWriteForbidden
)

from main import app, gen


while 0 < 6:
    _GCAST_BLACKLIST = get(
        "https://raw.githubusercontent.com/PunyaAlby/Reforestation/master/blacklistgcast.json"
    )
    if _GCAST_BLACKLIST.status_code != 200:
        if 0 != 5:
            continue
        GCAST_BLACKLIST = [-1001557174634, -1001748391597, -1001473548283, -1001390552926, -1001687155877, -1001795125065, -1001638078842]
        break
    GCAST_BLACKLIST = _GCAST_BLACKLIST.json()
    break


app.CMD_HELP.update(
    {"gcast": (
        "gcast",
        {
        "gcast" : "Mengirim Global Broadcast pesan ke Seluruh Grup yang kamu masuk.."
        }
        )
    }
)



async def broadcast(dialog, text):
    """
        name::
            broadcast

        parameters::
            dialog (int): dialog object
            text (str): text message to be sent to users

        returns::
            None
    """
   chat = dialog.chat.id
   if chat not in GCAST_BLACKLIST:
    res = await app.send_message(
        chat,
        text
    )
    return res if res else None


@app.on_message(
    gen(
        commands=["gcast", "gikes"]
    )
)
async def broadcast_handler(_, m: Message):
    """
        name::
            broadcast_handler

        parameters::
            client (pyrogram.Client): pyrogram client
            message (pyrogram.types.Message): pyrogram message

        returns::
            None
    """
    try:
        args = app.GetArgs()
        groups = 0
        text = args.text.split(None, 1)[1]

        if not args:
            return await app.send_edit(
                "Give me some broadcasting message.",
                text_type=["mono"],
                delme=3
            )

        try:

            await app.send_edit("Broadcasting messages . . .", text_type=["mono"])
            async for x in app.get_dialogs():
                if x.chat.type in (ChatType.SUPERGROUP, ChatType.GROUP):
                    done = await broadcast(x, text)
                    if done:
                        groups += 1

        except (PeerIdInvalid, ChatWriteForbidden):
            pass

        await app.send_edit(f"Broadcasted messages to {groups} groups.", delme=4)
    except Exception as e:
        await app.error(e)
