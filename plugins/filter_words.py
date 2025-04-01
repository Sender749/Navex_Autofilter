from pyrogram import filters
from Jisshu.bot import JisshuBot
from database.ia_filterdb import get_filter_words, set_filter_words
from info import ADMINS

@JisshuBot.on_message(filters.command("filterword") & filters.user(ADMINS))
async def show_filter_words(client, message):
    words = await get_filter_words()
    formatted_words = ", ".join(sorted(words))
    await message.reply_text(
        f"📝 Current filter words ({len(words)}):\n\n"
        f"{formatted_words}\n\n"
        "Use /set_filterword to update the list"
    )

@JisshuBot.on_message(filters.command("set_filterword") & filters.user(ADMINS))
async def update_filter_words(client, message):
    if len(message.command) < 2:
        await message.reply_text(
            "❌ Please provide words separated by commas.\n"
            "Example: /set_filterword please,bhai,do\n\n"
            "Current words:\n"
            f"{', '.join(sorted(await get_filter_words()))}"
        )
        return

    words_input = " ".join(message.command[1:])
    words = [word.strip().lower() for word in message.command[1].split(",") if word.strip()]
    await set_filter_words(words)

    updated_words = ", ".join(sorted(words))
    await message.reply_text(
        f"✅ Filter words updated successfully! ({len(words)} words)\n\n"
        f"New list: {', '.join(sorted(words))}"
    )
