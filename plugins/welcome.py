print("Welcome plugin loaded!")  # Debug log

@JisshuBot.on_chat_member_updated()
async def welcome_new_user(client, chat_member: ChatMemberUpdated):
    print(f"Chat member updated event detected!")  # Debug log
    print(f"Chat ID: {chat_member.chat.id}, User: {chat_member.new_chat_member.user.first_name if chat_member.new_chat_member else 'None'}")  # Debug log

    if chat_member.new_chat_member and chat_member.new_chat_member.status == "member":
        user_name = chat_member.new_chat_member.user.first_name
        print(f"New user joined: {user_name}")  # Debug log
        await client.send_message(chat_member.chat.id, f"👋 Welcome {user_name}!")
