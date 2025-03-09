from pyrogram import filters
from pyrogram.types import ChatMemberUpdated
from info import BIN_CHANNEL
from Jisshu.bot import JisshuBot

TUTORIAL_VIDEO_FILE_ID = "BAACAgUAAxkBAAIN3GfMYg3f98IOATHjOljUWUSK8D_MAAJ1FQACyBhRVjH6nRmO9C86HgQ"

SEND_WELCOME_MESSAGE = True
SEND_TUTORIAL_VIDEO = True
SEND_JOIN_LOG = True

print("Welcome plugin loaded!")  # Debug log

@JisshuBot.on_chat_member_updated()
async def welcome_new_user(client, chat_member: ChatMemberUpdated):
    # Check if the user is a new member
    if chat_member.new_chat_member and chat_member.new_chat_member.status == "member":
        chat_id = chat_member.chat.id
        user = chat_member.new_chat_member.user
        user_name = user.first_name

        print(f"New user joined: {user_name}")  # Debug log

        welcome_text = f"👋 **Welcome {user_name}!**\n\n" \
                       "🔍 You can search any movies in this group by sending their name (with correct spelling). " \
                       "Just type the movie name and check the results!\n\n" \
                       "📌 If you don't understand, watch this video."

        if SEND_WELCOME_MESSAGE:
            await client.send_message(chat_id, welcome_text)
            print(f"Welcome message sent to {user_name}")  # Debug log

        if SEND_TUTORIAL_VIDEO:
            await client.send_video(chat_id, video=TUTORIAL_VIDEO_FILE_ID, 
                                   caption="🎬 Here's a tutorial video on how to search for movies in the group. Enjoy!")
            print(f"Tutorial video sent to {user_name}")  # Debug log

        if SEND_JOIN_LOG:
            await client.send_message(BIN_CHANNEL, f"📝 **User joined:** {user_name}")
            print(f"Join log sent to bin channel for {user_name}")  # Debug log
