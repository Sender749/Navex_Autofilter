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
        current_words = ", ".join(sorted(await get_filter_words()))
        await message.reply_text(
            "❌ Please provide words separated by commas.\n"
            "Example: /set_filterword bhai ha kya,plz\n\n"
            f"Current words: {current_words}"
        )
        return
    
    # Get the entire command text after /set_filterword
    command_text = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else ""
    
    # Split by commas but preserve multi-word phrases
    words = []
    current_phrase = []
    in_quotes = False
    
    for char in command_text:
        if char == '"':
            in_quotes = not in_quotes
        elif char == ',' and not in_quotes:
            if current_phrase:  # Only add if we have content
                words.append(''.join(current_phrase).strip())
                current_phrase = []
        else:
            current_phrase.append(char)
    
    # Add the last phrase if exists
    if current_phrase:
        words.append(''.join(current_phrase).strip())
    
    # Clean up the words - remove empty entries and strip whitespace
    words = [word.strip().lower() for word in words if word.strip()]
    
    if not words:
        await message.reply_text("❌ No valid words provided!")
        return
    
    await set_filter_words(words)
    
    # Show updated list in comma-separated format
    updated_words = ", ".join(sorted(words))
    await message.reply_text(
        f"✅ Filter words updated successfully! ({len(words)} words)\n\n"
        f"New list: {updated_words}"
    )
