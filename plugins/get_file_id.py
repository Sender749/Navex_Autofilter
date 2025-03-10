from pyrogram import Client, filters

# Assuming JisshuBot is the main bot client
from Jisshu.bot import JisshuBot

@JisshuBot.on_message(filters.command("file_id") & filters.reply)
async def get_replied_file_id(client, message):
    replied_message = message.reply_to_message

    if not replied_message or not replied_message.media:
        await message.reply_text("❌ Please reply to a media file to get its file_id.")
        return

    # Identify the media type and extract file_id
    file_id = None
    media_type = "Unknown"

    if replied_message.video:
        file_id = replied_message.video.file_id
        media_type = "Video"
    elif replied_message.document:
        file_id = replied_message.document.file_id
        media_type = "File"
    elif replied_message.animation:
        file_id = replied_message.animation.file_id
        media_type = "GIF"
    elif replied_message.sticker:
        file_id = replied_message.sticker.file_id
        media_type = "Sticker"

    if file_id:
        await message.reply_text(f"🎬 **{media_type} File ID:**\n`{file_id}`")
    else:
        await message.reply_text("❌ This media type doesn't have a valid file_id.")
