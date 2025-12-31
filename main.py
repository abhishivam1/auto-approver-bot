import asyncio
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

from pyrogram import Client, filters
from pyrogram.types import ChatJoinRequest, Message
import json
import os
import re

API_ID = 751980
API_HASH = "1481687e152a07f5f4881deccf2235dd"
BOT_TOKEN = "7550064879:AAExJAk5zB_7vsNdMjaC1H221jbCv5b7Omw"

OWNER_ID = 5253533929

ADMIN_FILE = "admins_bot_2.json"
USERS_FILE = "users_bot_2.json"

FORWARD_LINKS = [
    "https://t.me/msgforward69/2",
    "https://t.me/msgforward69/3",
    "https://t.me/msgforward69/4"
]

if not os.path.exists(ADMIN_FILE):
    with open(ADMIN_FILE, "w") as f:
        json.dump([], f)

if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump([], f)

with open(ADMIN_FILE, "r") as f:
    ADMINS = json.load(f)

with open(USERS_FILE, "r") as f:
    USERS = json.load(f)

if OWNER_ID not in ADMINS:
    ADMINS.append(OWNER_ID)
    with open(ADMIN_FILE, "w") as f:
        json.dump(ADMINS, f)

app = Client(
    "join_bot_2",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

def save_admins():
    with open(ADMIN_FILE, "w") as f:
        json.dump(ADMINS, f)

def save_users():
    with open(USERS_FILE, "w") as f:
        json.dump(USERS, f)

def parse_link(link):
    match = re.match(r"https?://t\.me/([^/]+)/(\d+)", link)
    if match:
        return match.group(1), int(match.group(2))
    return None, None

@app.on_message(filters.command("start") & filters.private)
async def start(client, message: Message):
    uid = message.from_user.id
    if uid not in USERS:
        USERS.append(uid)
        save_users()
    await message.reply("👋 Welcome to the bot!\nThis is made by @prohubc")

@app.on_message(filters.command("addadmin") & filters.private)
async def add_admin(client, message: Message):
    if message.from_user.id != OWNER_ID:
        return await message.reply("❌ Only owner can add admins.")
    if len(message.command) < 2:
        return await message.reply("Usage: /addadmin <user_id>")
    try:
        uid = int(message.command[1])
        if uid not in ADMINS:
            ADMINS.append(uid)
            save_admins()
            await message.reply(f"✅ User {uid} added as admin.")
        else:
            await message.reply("ℹ️ User is already an admin.")
    except ValueError:
        await message.reply("❌ Invalid user ID.")

@app.on_message(filters.command("adminlist") & filters.private)
async def list_admins(client, message: Message):
    if message.from_user.id not in ADMINS:
        return await message.reply("❌ Not authorized.")
    await message.reply("👤 Admins:\n" + "\n".join(map(str, ADMINS)))

@app.on_message(filters.command("users") & filters.private)
async def users_count(client, message: Message):
    if message.from_user.id not in ADMINS:
        return await message.reply("❌ Not authorized.")
    await message.reply(f"👥 Total users: {len(USERS)}")

@app.on_message(filters.command("broadcast") & filters.private & filters.reply)
async def broadcast(client, message: Message):
    if message.from_user.id not in ADMINS:
        return await message.reply("❌ Not authorized.")
    sent = 0
    failed = 0
    for uid in USERS:
        try:
            await message.reply_to_message.copy(chat_id=uid)
            await asyncio.sleep(0.2)
            sent += 1
        except:
            failed += 1
    await message.reply(f"📢 Broadcast finished\n\n✅ Sent: {sent}\n❌ Failed: {failed}")

@app.on_chat_join_request()
async def approve_and_copy_links(client: Client, join_request: ChatJoinRequest):
    try:
        await client.approve_chat_join_request(
            join_request.chat.id,
            join_request.from_user.id
        )
        await asyncio.sleep(1)
        for link in FORWARD_LINKS:
            channel, msg_id = parse_link(link)
            if channel and msg_id:
                await client.copy_message(
                    chat_id=join_request.from_user.id,
                    from_chat_id=channel,
                    message_id=msg_id
                )
                await asyncio.sleep(1)
    except Exception as e:
        print(e)

async def main():
    print("🤖 Bot is running...")
    await app.start()
    await asyncio.Event().wait()

if __name__ == "__main__":
    loop.run_until_complete(main())
