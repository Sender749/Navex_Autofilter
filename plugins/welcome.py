from pyrogram import Client, filters
from Script import script  # Import script.py where messages are stored

@Client.on_message(filters.new_chat_members & filters.group)
async def welcome_new_user(client, message):
    for new_member in message.new_chat_members:
        user_mention = new_member.mention  # Get new user's mention
        group_name = message.chat.title  # Get group name

        # Get welcome message from script.py
        welcome_text = script.WELCOME_TXT.format(user_mention=user_mention, group_name=group_name)

        # Send the welcome message
        await message.reply_text(welcome_text)
