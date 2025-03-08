# plugins/welcome.py

from telegram import Update
from telegram.ext import CallbackContext
from script import WELCOME_MESSAGE, WELCOME_VIDEO_PATH

async def send_welcome_message(update: Update, context: CallbackContext):
    # Get the new user's details
    user = update.message.new_chat_members[0]
    user_name = user.first_name

    # Format the welcome message with the user's name
    welcome_text = WELCOME_MESSAGE.format(user_name=user_name)

    # Send the welcome message
    await update.message.reply_text(welcome_text)

    # Send the playable video
    if WELCOME_VIDEO_PATH:
        with open(WELCOME_VIDEO_PATH, 'rb') as video_file:
            await update.message.reply_video(video=video_file, caption="Check out this intro video!")
