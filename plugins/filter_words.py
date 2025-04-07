from pyrogram import filters
from Jisshu.bot import JisshuBot
from database.ia_filterdb import get_filter_words, set_filter_words
from info import ADMINS

@JisshuBot.on_message(filters.command("filterword") & filters.user(ADMINS))
async def show_filter_words(client, message):
    words = await get_filter_words()
    formatted_words = "\n".join([f"• {word}" for word in sorted(words)])
    count = len(words)
    await message.reply_text(
        f"📝 Current filter words ({count}):\n\n"
        f"{formatted_words}\n\n"
        "To add/update: /set_filterword word1, word2, \"multi word phrase\""
    )

@JisshuBot.on_message(filters.command("set_filterword") & filters.user(ADMINS))
async def update_filter_words(client, message):
    if len(message.command) < 2:
        current_words = await get_filter_words()
        example = "/set_filterword send, kr do, movie, series hai bhai, pls"
        await message.reply_text(
            "❌ Please provide words/phrases separated by commas.\n"
            f"Example: {example}\n\n"
            f"Current count: {len(current_words)} words"
        )
        return
    
    # Split by commas and clean the words
    words = [word.strip().lower() 
             for word in message.text.split(maxsplit=1)[1].split(",") 
             if word.strip()]
    
    if not words:
        await message.reply_text("❌ No valid words provided!")
        return
    
    # Merge with existing words
    existing = await get_filter_words()
    updated = existing.union(words)
    await set_filter_words(updated)
    
    # Show results
    added = len(updated) - len(existing)
    await message.reply_text(
        f"✅ Updated filter words:\n"
        f"- Total words: {len(updated)}\n"
        f"- Newly added: {added}\n"
        f"- Use /filterword to view all"
    )
