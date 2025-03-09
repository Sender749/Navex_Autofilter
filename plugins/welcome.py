from Jisshu.bot import JisshuBot  # Import the bot instance
from pyrogram import filters
from pyrogram.types import ChatMemberUpdated
from info import BIN_CHANNEL

TUTORIAL_VIDEO_FILE_ID = "BAACAgUAAxkBAAIN3GfMYg3f98IOATHjOljUWUSK8D_MAAJ1FQACyBhRVjH6nRmO9C86HgQ"

SEND_WELCOME_MESSAGE = True
SEND_TUTORIAL_VIDEO = True
SEND_JOIN_LOG = True

print("Welcome plugin loaded!")  # Debug log

@JisshuBot.on_chat_member_updated()
async def welcome_new_user(client, chat_member: ChatMemberUpdated):
    print(f"Chat member updated event detected!")  # Debug log
    print(f"Chat ID: {chat_member.chat.id}, User: {chat_member.new_chat_member.user.first_name if chat_member.new_chat_member else 'None'}")  # Debug log

    if chat_member.new_chat_member and chat_member.new_chat_member.status == "member":
        user_name = chat_member.new_chat_member.user.first_name
        print(f"New user joined: {user_name}")  # Debug log
        await client.send_message(chat_member.chat.id, f"👋 Welcome {user_name}!")
