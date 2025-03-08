from pyrogram import Client, filters

@Client.on_message(filters.video)
async def get_video_file_id(client, message):
    video = message.video
    file_id = video.file_id
    await message.reply_text(f"🎥 **Video File ID:**\n`{file_id}`")
