from pyrogram import Client, filters

@Client.on_message(filters.media)
async def get_media_file_id(client, message):
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
