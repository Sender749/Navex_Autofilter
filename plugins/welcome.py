from pyrogram import filters
from info import BIN_CHANNEL
from Jisshu.bot import JisshuBot

TUTORIAL_VIDEO_FILE_ID = "BAACAgUAAxkBAAIN3GfMYg3f98IOATHjOljUWUSK8D_MAAJ1FQACyBhRVjH6nRmO9C86HgQ"

SEND_WELCOME_MESSAGE = True
SEND_TUTORIAL_VIDEO = True
SEND_JOIN_LOG = True

print("Welcome plugin loaded!")  # Debug log

@JisshuBot.on_message(filters.new_chat_members)
async def welcome_new_user(client, message):
    chat_id = message.chat.id
    print(f"New chat members detected in chat ID: {chat_id}")  # Debug log

    for user in message.new_chat_members:
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
