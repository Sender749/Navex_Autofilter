from pyrogram import Client, filters

app = Client("my_bot")

# Dictionary to store user states
user_states = {}

@app.on_message(filters.command("file_id"))
async def request_file(client, message):
    # Set the user's state to expect a file
    user_states[message.from_user.id] = "awaiting_file"
    await message.reply_text("Send me a file.")

@app.on_message(filters.media & filters.private)
async def get_media_file_id(client, message):
    user_id = message.from_user.id

    # Check if the user is in the "awaiting_file" state
    if user_id in user_states and user_states[user_id] == "awaiting_file":
        # Reset the user's state
        user_states[user_id] = None

        # Check the type of media and extract the file ID accordingly
        file_id = None

        if message.video:
            file_id = message.video.file_id
            media_type = "Video"
        elif message.document:
            file_id = message.document.file_id
            media_type = "File"
        elif message.animation:
            file_id = message.animation.file_id
            media_type = "GIF"
        elif message.sticker:
            file_id = message.sticker.file_id
            media_type = "Sticker"
        else:
            media_type = "Unknown"

        if file_id:
            # Send the file ID back to the user
            await message.reply_text(f"🎬 **{media_type} File ID:**\n`{file_id}`")
        else:
            await message.reply_text("This media type doesn't have a file ID.")
    else:
        # If the user is not in the "awaiting_file" state, ignore the media
        pass

app.run()
