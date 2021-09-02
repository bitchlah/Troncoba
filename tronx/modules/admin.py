import time
import asyncio
import html

from pyrogram import Client, filters
from pyrogram.types import Message, ChatPermissions, User

from pyrogram.errors import UserAdminInvalid
from pyrogram.methods.chats.get_chat_members import Filters as ChatMemberFilters

from tronx import (
	app, 
	CMD_HELP, 
	PREFIX,
	Config,
	)

from tronx.helpers import (
	get_arg, 
	get_args, 
	GetUserMentionable, 
	mention_html, 
	mention_markdown, 
	CheckAdmin, 
	CheckReplyAdmin, 
	RestrictFailed,
	gen,
	error, 
	send_edit,
	private,
	code,
	long,
)




CMD_HELP.update(
	{"admin" : (
		"admin", 
		{
		"ban" : "bans a user",
		"unban" : "unbans a user",
		"mute" : "restricts a user from talking in groups",
		"unmute" : "unrestricts a user from talking in groups",
		"promote" : "promote a member to admin",
		"demote" : "demote a admin to a member",
		"pin" : "pin a message in group",
		"unpin" : "unpin a pinned message in group",
		"unpin all" : "unpin all pinned messages in one command"
		}
		)
	}
)



@app.on_message(gen("ban"))
async def ban_hammer(_, m):
	# return if used in private
	await private(m)
	reply = m.reply_to_message
	# check that you're admin or not
	if await CheckAdmin(m) is True:
		if reply and (long(m) == 1 or long(m) > 1):
			user = reply.from_user
			await send_edit(m, "⏳ • Hold on...")
			await app.kick_chat_member(
				m.chat.id,
				user.id
				)
			await send_edit(m, f"Banned {mention_markdown(user.id, user.first_name)} in this chat ...")
			# not replies 
		elif not reply:
			if long(m) == 1:
				await send_edit(m, "Give me user id or username of that member you want to ban ...")
				return
			elif len(m.command) > 1:
				user = await app.get_users(m.command[1])
				await send_edit(m, "⏳ • Hold on...")
				done = await app.kick_chat_member(
					chat_id=m.chat.id,
					user_id=user.id,
					)
				if done:
					await send_edit(m, f"Banned {mention_markdown(user.id, user.first_name)} from the chat !")
			else:
				await send_edit(m, "Please try again later . . .")
		# used on admin or owner
		else:
			await send_edit(m, "I can't ban this user . . .")
	else:
		await send_edit(m, "Sorry, Your Are Not An Admin Here !")




@app.on_message(gen("unban"))
async def unban(_, m):
	await private(m)
	reply = m.reply_to_message
	if await CheckAdmin(m) is True:

		if reply and (long(m) == 1 or long(m) > 1):
			user = reply.from_user
			await send_edit(m, "⏳ • Hold on...")
			done = await app.unban_chat_member(
				chat_id=m.chat.id,
				user_id=user.id
				)
			if done:
				await send_edit(m, f"Unbanned {mention_markdown(user.id, user.first_name)} in the current chat.") 
			elif not done:
				await send_edit(m, "I'm not able to unban this user . . .")
				return

		elif not reply:
			if long(m) == 1:
				await send_edit(m, "Please give me some id or username . . .")
				return
			elif long(m) > 1:
				await send_edit(m, "⏳ • Hold on...")
				user = await app.get_users(m.command[1])
				done = await app.unban_chat_member(
					chat_id=m.chat.id, 
					user_id=user.id
					)
				if done:
					await send_edit(m, f"Unbanned {mention_markdown(user.id, user.first_name)} from this chat . . .")
				else:
					await send_edit(m, "I'm not able to unban this user . . .")

	else:
		await send_edit(m, "Sorry, You Are Not An Admin Here !")




# Mute Permissions
mute_permission = ChatPermissions(
	can_send_messages=False,
	can_send_media_messages=False,
	can_send_stickers=False,
	can_send_animations=False,
	can_send_games=True,
	can_use_inline_bots=False,
	can_add_web_page_previews=False,
	can_send_polls=False,
	can_change_info=False,
	can_invite_users=True,
	can_pin_messages=False,
)




@app.on_message(gen("mute"))
async def mute_hammer(_, m):
	await private(m)
	reply = m.reply_to_message
	if await CheckAdmin(m) is True:
		if reply and (long(m) == 1 or long(m) > 1):
			user = reply.from_user
			done = await app.restrict_chat_member(
				m.chat.id,
				user.id,
				permissions=mute_permission,
				)
			if done:
				await send_edit(m, f"{mention_markdown(user.id, user.first_name)} has been muted")
			else:
				await send_edit(m, "Sorry, I am unable to mite this user . . .")

		elif not reply:
			if long(m) == 1:
				await send_edit(m, "Please give me some id or username . . .")
				return

			elif long(m) > 1:
				await send_edit(m, "⏳ • Hold on...")
				user = await app.get_users(m.command[1])
				done = await app.restrict_chat_member(
					m.chat.id,
					user.id,
					permissions=mute_permission,
					)
				if done:
					await send_edit(m, f"{mention_markdown(user.id, user.first_name)} has been muted.")
				else:
					await send_edit(m, "Sorry, I can't mute this user . . .")
			else:
				await send_edit(m, "Please try again later . . .")

	else:
		await send_edit(m, "Sorry, You Are Not An Admin Here !")




# Unmute permissions
unmute_permissions = ChatPermissions(
	can_send_messages=True,
	can_send_media_messages=True,
	can_send_stickers=True,
	can_send_animations=True,
	can_send_games=True,
	can_use_inline_bots=True,
	can_add_web_page_previews=True,
	can_send_polls=True,
	can_change_info=False,
	can_invite_users=True,
	can_pin_messages=False,
)




@app.on_message(gen("unmute"))
async def unmute(_, m):
	await private(m)
	reply = m.reply_to_message
	if await CheckAdmin(m) is True:
		if reply and (long(m) == 1 or long(m) > 1):
			user = reply.from_user
			await send_edit(m, "⏳ • Hold on...")
			done = await app.restrict_chat_member(
				m.chat.id,
				user.id,
				permissions=unmute_permissions,
				)
			if done:
				await send_edit(m, f"{mention_markdown(user.id, user.first_name)} was unmuted !")
			else:
				await send_edit(m, "I can't unmute this user . . .")

		elif not reply:
			if long(m) == 1:
				await send_edit(m, "Please give me some id or username . . .")
				return
			elif long(m) > 1:
				await send_edit(m, "⏳ • Hold on...")
				user = await app.get_users(m.command[1])
				done = await app.restrict_chat_member(
					chat_id=m.chat.id,
					user_id=user.id,
					permissions=unmute_permissions,
					)
				if done:
					await send_edit(m, f"{mention_markdown(user.id, user.first_name)} was unmuted.")
				else:
					await send_edit(m, "I can't unmute this user . . .")
			else:
				await send_edit(m, "Please try again later . . .")
	else:
		await send(m, "Sorry, Your Are Not An Admin Here ! ")




@app.on_message(gen("kick"))
async def kick_user(_, m):
	await private(m)
	reply = m.reply_to_message
	if await CheckAdmin(m) is True:
		if reply and (long(m) == 1 or long(m) > 1):
			user = reply.from_user
			await send_edit(m, "⏳ • Hold on...")
			done = await app.kick_chat_member(
				chat_id=m.chat.id,
				user_id=user.id,
				)
			if done:
				await send_edit(m, f"Kicked {mention_markdown(user.id, user.first_name)} from the chat.")
			else:
				await send_edit(m, "I can't kick this user . . .")

		elif not reply:
			if long(m) == 1:
				await send_edit(m, "Give me some id or username . . .")
				return
			elif long(m) > 1:
				await send_edit(m, "⏳ • Hold on...")
				user = await app.get_users(m.command[1])
				done = await app.kick_chat_member(
					chat_id=m.chat.id,
					user_id=user.id,
					)
				if done:
					await send_edit(m, f"Kicked {mention_markdown(user.id, user.first_name} from this chat.")
				else:
					await send_edit(m, "I can't kick this user.")
			else:
				await send_edit(m, "Please try again later . . .")

	else:
		await send_edit(m, "Sorry, Your Are Not An Admin Here !")




@app.on_message(gen("pin"))
async def pin_message(_, m):
	try:
		reply = m.reply_to_message
		if reply:
			await send_edit(m, "⏳ • Hold on...")
			done = await app.pin_chat_message(
				m.chat.id,
				reply.message_id,
				)
			if done:
				await send_edit(m, "`Pinned message!`")
			else:
				await send_edit(m, "Failed to pin message")
		elif not reply:
			await send_edit(m, "`Reply to a message so that I can pin that message ...`")     
			time.sleep(2)
			await m.delete()
	except Exception as e:
		await error(m, e)




@app.on_message(gen("unpin"))
async def pin_message(_, m):
	try:
		reply = m.reply_to_message
		if reply and long(m) == 1:
			await send_edit(m, "⏳ • Hold on...")
			done = await app.unpin_chat_message(
				m.chat.id,
				m.reply_to_message.message_id
				)
			if done:
				await send_edit(m, "`Unpinned message !`")
			else:
				await send_edit(m, "Failed to unpin message . . .")
		elif (reply or not reply) and long(m) > 1:
			cmd = m.command[1]
			if cmd == "all":
				done = await app.unpin_all_chat_messages(m.chat.id)
				if done:
					await send_edit(m, "Unpinned all pinned messages . . .")
				else:
					await send_edit(m, "Failed to unpin all messages . . .")
			elif cmd != "all"
				await send_edit(m, "Reply to a pinned message to unpin or use 'all' after unpin command to unpin all pinned message . . .")
			else:
				await send_edit(m, "Failed to unpin messages . . .")
	except Exception as e:
		await error(m, e)




@app.on_message(gen("promote"))
async def promote(_, m):
	await private(m)
	reply = m.reply_to_message
	if await CheckAdmin(m) is True:
		if reply:
			if long(m) > 1:
				title = m.command[1]
				await app.set_administrator_title(m.chat.id, user.id, title)
			else:
				pass
			await send_edit(m, "⏳ • Hold on...")
			user = reply.from_user
			done = await app.promote_chat_member(
				m.chat.id, 
				user.id,
				can_pin_messages=True, 
				can_invite_users=True,
				)
			if done:
				await send_edit(m, f"{mention_markdown(user.id, user.first_name)} was promoted to admin !")
			else:
				await send_edit(m, "Failed to promote the user . . .")
		elif not reply:
			if long(m) == 1:
				await send_edit(m, "Please give me some id or username . . .")
				return
			elif long(m) > 1:
				user = await app.get_users(m.command[1])
				await send_edit(m, "⏳ • Hold on...")
				if long(m) > 2:
					title = m.command[2]
					await app.set_administrator_title(m.chat.id, user.id, title)
				else:
					pass
				done = await app.promote_chat_member(
					m.chat.id, 
					user.id,
					can_pin_messages=True, 
					can_invite_users=True,
					)
				if done:
					await send_edit(m, f"{mention_markdown(user.id, user.first_name)} was promoted to admin !")
				else:
					await send_edit(m, "Failed to promote the user . . .")
			else:
				await send_edit(m, "Failed to promote user . . .")
	else:
		await send_edit(m, "Sorry, you are not an admin here . . .")




@app.on_message(gen("demote"))
async def demote(client, m):
	await private(m)
	reply = m.reply_to_message
	if await CheckAdmin(m) is True:
		if reply:
			await send_edit(m, "⏳ • Hold on...")
			user = reply.from_user
			done = await app.promote_chat_member(
				m.chat.id,
				user.id,
				is_anonymous=False,
				can_change_info=False,
				can_delete_messages=False,
				can_edit_messages=False,
				can_invite_users=False,
				can_promote_members=False,
				can_restrict_members=False,
				can_pin_messages=False,
				can_post_messages=False,
				)
			if done:
				await send_edit(m, f"{mention_markdown(user.id, user.first_name)} now removed from admin status !")
			else:
				await send_edit(m, "Failed to promote the user . . .")
		elif not reply:
			if long(m) == 1:
				await send_edit(m, "Please give me some id or reply to that admin . . .")
				return
			elif long(m) > 1:
				user = m.command[1]
				done = await app.promote_chat_member(
					m.chat.id,
					user.id,
					is_anonymous=False,
					can_change_info=False,
					can_delete_messages=False,
					can_edit_messages=False,
					can_invite_users=False,
					can_promote_members=False,
					can_restrict_members=False,
					can_pin_messages=False,
					can_post_messages=False,
					)
				if done:
					await send_edit(m, f"{mention_markdown(user.id, user.first_name} is now removed from admin status !")
			else: 
				await send_edit(m, "Please try again later . . .")


