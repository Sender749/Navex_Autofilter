from pyrogram import Client, filters
from pyrogram.types import ChatMemberUpdated
from Script import script  # Import script.py where WELCOME_TXT is stored

@Client.on_chat_member_updated(filters.group)
async def welcome_user(client, chat_member: ChatMemberUpdated):
    if chat_member.new_chat_member and chat_member.new_chat_member.status in ["member"]:
        user_mention = chat_member.new_chat_member.user.mention  # Get user's mention
        group_name = chat_member.chat.title  # Get group name

        # Get welcome message from script.py
        welcome_text = script.WELCOME_TXT.format(user_mention=user_mention, group_name=group_name)

        # Send the welcome message
        await client.send_message(chat_member.chat.id, welcome_text)
