import os
os.system("pip3 install tgcrypto pyrogram")

from pyrogram import Client
import asyncio

# guide them 

intro = """
@Tronuserbot Corporation
Get the following values by logging to,

https://my.telegram.org

Required:
  
  1. APP_ID
  2. API_HASH
  3. PHONE NUMBER (WITH COUNTRY CODE)
  
"""


print(intro)


API_ID = input("\nEnter your API_ID: ")

while not API_ID.isdigit():
  print("\n\nPlease enter a digit.\n\n")
  API_ID = input("Enter your API_ID (1234567): ")



# hexadecimal number
API_HASH = input("\nEnter API HASH: ")



# create a new pyrogram session
with Client(":memory:", api_id=int(API_ID), api_hash=API_HASH, hide_password=True) as app:
  app.send_message("me", f"This Is Your Tron Userbot • [ `SESSION` ]\n\n```{app.export_session_string()}```\n\n⚠️• Don't share this with anyone !!\n\nCreate Again • [ Press Here](https://replit.com/@beastzx18/Tron-Userbot-Session)", disable_web_page_preview=True,) 
  print("Your String Session Is Successfully Saved In Telegram Saved Messages !! Don't Share It With Anyone!! Anyone having your session can use your telegram account !")
  
