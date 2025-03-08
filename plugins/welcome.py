from pyrogram import Client, filters
from script import WELCOME_MESSAGE  # Assuming you have a WELCOME_MESSAGE in script.py

# Tutorial video file_id
TUTORIAL_VIDEO_FILE_ID = "BAACAgUAAxkBAAIN3GfMYg3f98IOATHjOljUWUSK8D_MAAJ1FQACyBhRVjH6nRmO9C86HgQ"

# Flags to control whether the welcome message and video message are sent
SEND_WELCOME_MESSAGE = True  # Set to False to disable welcome message
SEND_TUTORIAL_VIDEO = True   # Set to False to disable tutorial video

@Client.on_message(filters.new_chat_members)
async def welcome_new_user(client, message):
    # Get the new user's details
    for user in message.new_chat_members:
        user_name = user.first_name

        # Send welcome message if the flag is True
        if SEND_WELCOME_MESSAGE:
            welcome_text = WELCOME_MESSAGE.format(user_name=user_name)
            await message.reply_text(welcome_text)

        # Send tutorial video if the flag is True
        if SEND_TUTORIAL_VIDEO:
            await message.reply_video(video=TUTORIAL_VIDEO_FILE_ID, caption="🎬 Here's a tutorial video on how to search for movies in the group. Enjoy!")
