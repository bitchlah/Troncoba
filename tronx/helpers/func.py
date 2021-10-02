import pytz, datetime, time, os
from asyncio import sleep

from pyrogram import Client
from pyrogram.types import Message

from tronx import (
	app,
	log,
	PREFIX,
	CMD_HELP,
)

from config import Config

from .user import mymention




# date
def showdate():
	today = pytz.timezone(
		Config.TIME_ZONE
		)
	get_date = datetime.datetime.now(today)
	mydate = get_date.strftime("%d %b %Y")
	return mydate


# time
def showtime():
	today = pytz.timezone(
		Config.TIME_ZONE
		)
	get_time = datetime.datetime.now(today)
	mytime = get_time.strftime("%r")
	return mytime


# send or edit msg
async def send_edit(
	m: Message, 
	text, 
	parse_mode="markdown", 
	disable_web_page_preview=False,
	delme : int = 0,
	prefix = PREFIX,
	mono = False,
	bold = False
	):
	if mono:
		try:
			await m.edit(f"`{text}`")
		except:
			await app.send_message(
				m.chat.id,
				f"`{text}`"
				)
	elif bold:
		try:
			await m.edit(text)
		except:
			await app.send_message(
				m.chat.id,
				text
				)
	else:
		try:
			await m.edit(text)
		except:
			await app.send_message(
				m.chat.id,
				text
				)
	try:
		if delme != 0:
			time.sleep(delme)
			await m.delete()
		else:
			pass
	except Exception as e:
		await error(m, e)


# send msg
async def sendmsg(m: Message, text):
	try:
		await app.send_message(
			m.chat.id,
			text
			)
	except Exception as e:
		await error(m, e)
	return


# show error
async def error(m: Message, e):
	teks = f"Traceback Report:\n\n"
	teks += f"Date: {showdate()}\nTime: {showtime()}\n\n"
	teks += f"This can be a error in tronuserbot, if you want you can forward this to @tronuserbot.\n\n" 
	teks += f"Command: {m.text}\n\n"
	teks += f"Error:\n\n"
	teks += f"{e}"
	try:
		await app.send_message(
			Config.LOG_CHAT,
			teks
			)
	except:
		print(teks)
	log.error("Please check your log chat for traceback error !")
	return 


# delete msg
async def delete(m: Message, sec: int = 0):
	if not sec > 600: # 10 min
		await sleep(sec)
		await m.delete()
	else:
		log.error("maximum sleep of 10 ( 600 sec ) minutes")
	return




async def data(plug):
	try:
		for x, y in zip(
			CMD_HELP.get(plug)[1].keys(), 
			CMD_HELP.get(plug)[1].values()
			):
			plugin_data.append(
				f"CMD: `{PREFIX}{x}`\nINFO: `{y}`\n\n"
				)
		return True
	except Exception as e:
		print(e)
		return False




async def private(m : Message, arg=True):
	if m.chat.type == "private":
		await send_edit(
			m, 
			"Please use these commands in groups . . ."
			)
		await delete(m, 3)
		if arg:
			return
		else:
			pass
	else:
		pass




async def code(my_codes):
	try:
		my_codes
	except Exception as e:
		await error(m, e)




def long(m: Message):
	text = len(m.command)
	if text:
		return text
	else:
		return 0




# file creator
async def create_file(m: Message, app: Client, filename, text):
	try:
		name = filename
		content = text
		file = open(name, "w+")
		file.write(content)
		file.close()
		await app.send_document(
			m.chat.id,
			name,
			caption = f"**Uploaded By:** {mymention()}"
			)
		os.remove(name)
		await m.delete()
	except Exception as e:
		await error(m, e)
	return




def rem_dual(one, two):
	data = list(set(one) - set(two))
	return data