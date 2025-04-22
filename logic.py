from config import USER_NAMES, USER_ROLES, GROUP

async def forward_message(sender_id, msg, context, edited=False):
    role = USER_ROLES.get(sender_id)
    sender_name = USER_NAMES.get(sender_id, f"ID {sender_id}")
    prefix = "📩 Đã chỉnh sửa\n" if edited else ""
    header = f"{prefix}💬 {sender_name}:"

    # Lựa chọn người nhận
    if role == "client":
        targets = [uid for uid in GROUP if uid != sender_id]
    elif role == "staff":
        targets = [uid for uid in GROUP if uid != sender_id]
    elif role == "boss":
        text = msg.text or ""
        if text.startswith("#linh"):
            targets = [8000810390]
            msg_text = text.replace("#linh", "", 1).strip()
        elif text.startswith("#hau") or text.startswith("#hậu"):
            targets = [462516296]
            msg_text = text.replace("#hau", "", 1).replace("#hậu", "", 1).strip()
        else:
            targets = [uid for uid in GROUP if uid != sender_id]
            msg_text = text
    else:
        return

    for target in targets:
        try:
            if msg.text:
                text_to_send = msg_text if role == "boss" and 'msg_text' in locals() else msg.text
                await context.bot.send_message(chat_id=target, text=f"{header}\n{text_to_send}")
            elif msg.photo:
                await context.bot.send_photo(chat_id=target, photo=msg.photo[-1].file_id, caption=header)
            elif msg.video:
                await context.bot.send_video(chat_id=target, video=msg.video.file_id, caption=header)
            elif msg.voice:
                await context.bot.send_voice(chat_id=target, voice=msg.voice.file_id, caption=header)
            elif msg.document:
                await context.bot.send_document(chat_id=target, document=msg.document.file_id, caption=header)
            else:
                await context.bot.send_message(chat_id=target, text=f"{header}\n(Loại tin chưa hỗ trợ)")
        except Exception as e:
            print(f"Lỗi gửi đến {target}: {e}")