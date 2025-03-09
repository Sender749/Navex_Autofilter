from pyrogram import filters
from info import BIN_CHANNEL  # Import bin channel ID
from Jisshu.bot import JisshuBot  # Import bot instance

# Tutorial video file_id
TUTORIAL_VIDEO_FILE_ID = "BAACAgUAAxkBAAIN3GfMYg3f98IOATHjOljUWUSK8D_MAAJ1FQACyBhRVjH6nRmO9C86HgQ"

# Flags to control message sending
SEND_WELCOME_MESSAGE = True  # Set False to disable welcome message
SEND_TUTORIAL_VIDEO = True   # Set False to disable tutorial video
SEND_JOIN_LOG = True  # Set False to disable logging join messages

@JisshuBot.on_message(filters.new_chat_members)
async def welcome_new_user(client, message):
    chat_id = message.chat.id  # Group ID

    for user in message.new_chat_members:
        user_name = user.first_name

        # Welcome text
        welcome_text = f"👋 **Welcome {user_name}!**\n\n" \
                       "🔍 You can search any movies in this group by sending their name (with correct spelling). " \
                       "Just type the movie name and check the results!\n\n" \
                       "📌 If you don't understand, watch this video."

        # Send welcome message if enabled
        if SEND_WELCOME_MESSAGE:
            await client.send_message(chat_id, welcome_text)

        # Send tutorial video if enabled
        if SEND_TUTORIAL_VIDEO:
            await client.send_video(chat_id, video=TUTORIAL_VIDEO_FILE_ID, 
                                    caption="🎬 Here's a tutorial video on how to search for movies in the group. Enjoy!")

        # Send join log to bin channel if enabled
        if SEND_JOIN_LOG:
            await client.send_message(BIN_CHANNEL, f"📝 **User joined:** {user_name}")
