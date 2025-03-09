from pyrogram import Client, filters

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

        # Define the welcome message
        welcome_text = f"👋 **Welcome {user_name}!**\n\n" \
                       "🔍 You can search any movies in this group by send there name (with correct spelling). " \
                       "Just type the movie name and check the results!\n\n" \
                       "📌 If you don't understand, watch this video."

        # Send welcome message if the flag is True
        if SEND_WELCOME_MESSAGE:
            await message.reply_text(welcome_text)

        # Send tutorial video if the flag is True
        if SEND_TUTORIAL_VIDEO:
            await message.reply_video(video=TUTORIAL_VIDEO_FILE_ID, 
                                      caption="🎬 Here's a tutorial video on how to search for movies in the group. Enjoy!")
