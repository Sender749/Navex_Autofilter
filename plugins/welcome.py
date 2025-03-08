from pyrogram import Client, filters
from script import WELCOME_MESSAGE  # Assuming you have a WELCOME_MESSAGE in script.py

# Tutorial video file_id
TUTORIAL_VIDEO_FILE_ID = "BAACAgUAAxkBAAIN3GfMYg3f98IOATHjOljUWUSK8D_MAAJ1FQACyBhRVjH6nRmO9C86HgQ"

@Client.on_message(filters.new_chat_members)
async def welcome_new_user(client, message):
    # Get the new user's details
    for user in message.new_chat_members:
        user_name = user.first_name

        # Format the welcome message
        welcome_text = WELCOME_MESSAGE.format(user_name=user_name)

        # Send the welcome message
        await message.reply_text(welcome_text)

        # Send the tutorial video
        await message.reply_video(video=TUTORIAL_VIDEO_FILE_ID, caption="🎬 Here's a tutorial video on how to search for movies in the group. Enjoy!")
