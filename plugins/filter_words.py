from pyrogram import Client, filters
from Jisshu.bot import JisshuBot
from info import DATABASE_URI, DATABASE_NAME, ADMINS
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

# Database connection
client = AsyncIOMotorClient(DATABASE_URI)
db = client[DATABASE_NAME]
collection = db["filter_words"]

async def get_filter_words():
    doc = await collection.find_one({"_id": "filter_words"})
    return set(doc["words"]) if doc else {
        'bhai', 'bhje do', 'send', 'please', 'hai', 'hai kya', 'kya', 
        'do', 'de do', 'chahiye', 'dijiye', 'dedo', 'punjabi',
        'gurnal', 'bhular', 'movie', 'series', 'anime', 'link',
        'download', 'de', 'dear', 'bro', 'hi', 'hello', 'pls', 'plz'
    }

async def set_filter_words(words):
    await collection.update_one(
        {"_id": "filter_words"},
        {"$set": {"words": words}},
        upsert=True
    )

@JisshuBot.on_message(filters.command("filterword") & filters.user("ADMINS"))
async def show_filter_words(client, message):
    words = await get_filter_words()
    formatted_words = "\n".join(sorted(words))
    await message.reply_text(f"📝 Current filter words:\n\n{formatted_words}")

@JisshuBot.on_message(filters.command("set_filterword") & filters.user("ADMIN_USER_ID"))
async def update_filter_words(client, message):
    if len(message.command) < 2:
        await message.reply_text("❌ Please provide words separated by commas.\nExample: /set_filterword please,bhai,do")
        return
    
    words = [word.strip().lower() for word in message.command[1].split(",")]
    await set_filter_words(words)
    await message.reply_text(f"✅ Filter words updated successfully!\n\nNew words: {', '.join(words)}")
