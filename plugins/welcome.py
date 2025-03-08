from pyrogram import Client, filters
from Script import script  
from info import BIN_CHANNEL  # Import bin channel ID

@Client.on_message(filters.group & filters.new_chat_members)
async def welcome(client, message):
    for new_member in message.new_chat_members:
        user_mention = new_member.mention  
        user_id = new_member.id  
        username = f"@{new_member.username}" if new_member.username else "No Username"
        group_name = message.chat.title  
        inviter = message.from_user  # Who added the user (if available)

        # Determine how the user joined
        if inviter:
            if inviter.is_bot:
                join_method = "Joined via Bot Message"
            else:
                join_method = f"Invited by {inviter.mention}"
        elif message.sender_chat:
            join_method = "Joined via Group Link"
        else:
            join_method = "Joined via Search"

        # Welcome message in group
        welcome_text = script.WELCOME_TXT.format(user_mention=user_mention, group_name=group_name)
        await message.reply_text(welcome_text)

        # Log message to bin channel
        bin_message = (
            f"🆕 **New User Joined!**\n\n"
            f"👤 **Name:** {user_mention}\n"
            f"🆔 **User ID:** `{user_id}`\n"
            f"🔗 **Username:** {username}\n"
            f"🏠 **Group:** {group_name}\n"
            f"🛠 **Join Method:** {join_method}"
        )

        await client.send_message(BIN_CHANNEL, bin_message)
