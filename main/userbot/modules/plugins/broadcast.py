""" broadcast plugin """

from pyrogram.types import Message
from pyrogram.enums import ChatType
from pyrogram.errors import PeerIdInvalid, UserNotParticipant

from main import app, gen




app.CMD_HELP.update(
    {"broadcast" : (
        "broadcast",
        {
        "broadcast" : "Broadcast messages in user chats, group chats."
        }
        )
    }
)

app.CMD_HELP.update(
    {"gcast" : (
        "gcast",
        {
        "gcast" : "Broadcast messages in group chats."
        }
        )
    }
)

BLACKLIST = [
    -1001638078842,  # RUANGDISKUSIKAMI
    -1001473548283,  # SharingUserbot
    -1001433238829,  # TedeSupport
]

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
    res = await app.send_message(
        dialog.chat.id,
        text
    )
    return res if res else None


@app.on_message(
    gen(
        commands=["broadcast", "bdc"]
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
        users = 0
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
                chat_id = x.id
                if x.chat.type in (ChatType.SUPERGROUP, ChatType.GROUP) and chat_id not in BLACKLIST:
                       done = await broadcast(x, text)
                       if done:
                           groups += 1

           except (PeerIdInvalid, UserNotParticipant):
               pass

        await app.send_edit(f"Broadcasted messages to {users} users & {groups} groups.", delme=4)
    except Exception as e:
        await app.error(e)
