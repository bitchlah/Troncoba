import os
import re

from typing import (
	Union, 
	List, 
	Dict, 
	Pattern
)

from pyrogram.filters import create
from pyrogram import filters, Client
from pyrogram.types import (
	Message, 
	CallbackQuery, 
	InlineQuery, 
	InlineKeyboardMarkup, 
	ReplyKeyboardMarkup, 
	Update
)

from tronx.modules import SUDO_USERS
from tronx import USER_ID

from tronx import (
	PREFIX
)




if bool(SUDO_USERS) is False or SUDO_USERS is None:
	USERS = [USER_ID]
else:
	USERS = [USER_ID] + SUDO_USERS





# custom regex filter
def regex(
	pattern: Union[str, Pattern], 
	flags: int = 0
	):

	async def func(flt, _, update: Update):
		if ( update.from_user 
			and update.from_user.id in SUDO_USERS
			and not update.forward_date
			#and not message.chat.type == "channel"
			):
			if isinstance(update, Message):
				value = update.text or update.caption
			elif isinstance(update, CallbackQuery):
				value = update.data
			elif isinstance(update, InlineQuery):
				value = update.query
			else:
				raise ValueError(f"Regex filter doesn't work with {type(update)}")

			if value:
				update.matches = list(flt.p.finditer(value)) or None

			return bool(update.matches)
		else:
			return

	return create(
		func,
		"custom_regex",
		p=pattern if isinstance(pattern, Pattern) else re.compile(pattern, flags)
	)




# multiple prefixes
def myprefix():
	if len(PREFIX.split()) > 1:
		prelist = PREFIX.split()
	else:
		prelist = PREFIX
	return prelist




# custom command filter
def gen(commands: Union[str, List[str]], prefixes: Union[str, List[str]] = myprefix(), case_sensitive: bool = True):
	# modified func of pyrogram.filters.command
	command_re = re.compile(r"([\"'])(.*?)(?<!\\)\1|(\S+)")
	async def func(flt, client: Client, message: Message):
		# Username shared among all commands; used for mention commands, e.g.: /start@username
		global username

		username = ""
		# works only for you 
		if ( message.from_user 
			and message.from_user.id in USERS
			and not message.forward_date
			#and not message.chat.type == "channel"
			):

			text = message.text or message.caption
			message.command = None

			if not text:
				return False

			for prefix in flt.prefixes:
				if not text.startswith(prefix):
					continue

				without_prefix = text[len(prefix):]

				username = None

				for cmd in flt.commands:
					if not re.match(rf"^(?:{cmd}(?:@?{username})?)(?:\s|$)", without_prefix,
						flags=re.IGNORECASE if not flt.case_sensitive else 0):
						continue

					without_command = re.sub(rf"{cmd}(?:@?{username})?\s?", "", without_prefix, count=1)

					message.command = [cmd] + [
						re.sub(r"\\([\"'])", r"\1", m.group(2) or m.group(3) or "")
						for m in command_re.finditer(without_command)
					]
					return True
			return False
		else:
			return


	commands = commands if isinstance(commands, list) else [commands]
	commands = {c if case_sensitive else c.lower() for c in commands}

	prefixes = [] if prefixes is None else prefixes
	prefixes = prefixes if isinstance(prefixes, list) else [prefixes]
	prefixes = set(prefixes) if prefixes else {""}

	return create(
		func,
		"Commandfilter",
		commands=commands,
		prefixes=prefixes,
		case_sensitive=case_sensitive
	)
