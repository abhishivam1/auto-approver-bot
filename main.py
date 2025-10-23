from pyrogram import Client, filters
from pyrogram.types import ChatJoinRequest, Message
import json
import os
import asyncio
import re

API_ID = 751980
API_HASH = "1481687e152a07f5f4881deccf2235dd"
BOT_TOKEN = "7550064879:AAExJAk5zB_7vsNdMjaC1H221jbCv5b7Omw"
ADMIN_FILE = "admins_bot_2.json"

FORWARD_LINKS = [
    "https://t.me/msgforward69/2",
    "https://t.me/msgforward69/3",
    "https://t.me/msgforward69/4"
]

if not os.path.exists(ADMIN_FILE):
    with open(ADMIN_FILE, "w") as f:
        json.dump([], f)

with open(ADMIN_FILE) as f:
    ADMINS = json.load(f)

app = Client("join_bot_2", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def save_admins():
    with open(ADMIN_FILE, "w") as f:
        json.dump(ADMINS, f)

def parse_link(link):
    match = re.match(r"https?://t\.me/([^/]+)/(\d+)", link)
    if match:
        return match.group(1), int(match.group(2))
    return None, None

@app.on_message(filters.command("addadmin") & filters.private)
async def add_admin(client, message: Message):
    if message.from_user.id not in ADMINS:
        await message.reply("❌ You are not authorized to add admins.")
        return
    if len(message.command) < 2:
        await message.reply("Usage: /addadmin <user_id>")
        return
    try:
        new_admin = int(message.command[1])
        if new_admin not in ADMINS:
            ADMINS.append(new_admin)
            save_admins()
            await message.reply(f"✅ User {new_admin} added as admin.")
        else:
            await message.reply("User is already an admin.")
    except ValueError:
        await message.reply("❌ Invalid user ID.")

@app.on_message(filters.command("adminlist") & filters.private)
async def list_admins(client, message: Message):
    if message.from_user.id not in ADMINS:
        return await message.reply("❌ You are not authorized.")
    await message.reply(f"👤 Admins:\n" + "\n".join([str(a) for a in ADMINS]))

@app.on_chat_join_request()
async def approve_and_copy_links(client: Client, join_request: ChatJoinRequest):
    user_id = join_request.from_user.id
    chat_id = join_request.chat.id
    try:
        await client.approve_chat_join_request(chat_id, user_id)
        await asyncio.sleep(1)
        for link in FORWARD_LINKS:
            channel, msg_id = parse_link(link)
            if channel and msg_id:
                await client.copy_message(
                    chat_id=user_id,
                    from_chat_id=channel,
                    message_id=msg_id
                )
                await asyncio.sleep(1)
    except Exception as e:
        print(f"Error: {e}")

@app.on_message(filters.command("start") & filters.private)
async def start(client, message: Message):
    await message.reply("👋 Welcome to the bot!\nThis is made by @prohubc")

if __name__ == "__main__":
    print("🤖 Bot is running...")
    app.run()
