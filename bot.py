import os
import logging
from telegram import Update, Message, constants
from telegram.ext import (
    ApplicationBuilder, ContextTypes, MessageHandler,
    filters, CallbackQueryHandler, CommandHandler, 
    EditedMessageHandler
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import pytz

# ==== CẤU HÌNH ====
BOT_TOKEN = os.environ.get("BOT_TOKEN")
ID_LINH = int(os.environ.get("CHAT_ID_LINH"))       # 8000810390
ID_DIYEU = int(os.environ.get("CHAT_ID_DIYEU"))     # 1707360759
ID_HAU = int(os.environ.get("CHAT_ID_HAU"))         # 462516296

ID_TO_NAME = {
    ID_LINH: "Thùy Linh",
    ID_DIYEU: "Phạm Duy Diệu",
    ID_HAU: "Mr Hậu"
}

message_map = {}  # (from_id, original_msg_id) => {to_id: forwarded_msg_id}

# ==== HÀM Gửi tin nhắn đi ====
async def forward_message(sender_id: int, msg: Message, context: ContextTypes.DEFAULT_TYPE, edited=False):
    sender_name = ID_TO_NAME.get(sender_id, "Người lạ")
    targets = [ID_LINH, ID_DIYEU, ID_HAU]
    targets.remove(sender_id)  # không gửi lại cho người gửi

    for target_id in targets:
        try:
            # Xử lý reply mapping
            reply_to = None
            if msg.reply_to_message:
                original_id = msg.reply_to_message.message_id
                reply_to = message_map.get((msg.reply_to_message.chat_id, original_id), {}).get(target_id)

            text_prefix = f"{'✉️ Đã chỉnh sửa\n' if edited else ''}💬 {sender_name}:"

            if msg.text:
                sent = await context.bot.send_message(
                    chat_id=target_id,
                    text=f"{text_prefix}\n{msg.text}",
                    reply_to_message_id=reply_to if reply_to else None
                )
            elif msg.photo:
                sent = await context.bot.send_photo(
                    chat_id=target_id,
                    photo=msg.photo[-1].file_id,
                    caption=text_prefix,
                    reply_to_message_id=reply_to if reply_to else None
                )
            elif msg.document:
                sent = await context.bot.send_document(
                    chat_id=target_id,
                    document=msg.document.file_id,
                    caption=text_prefix,
                    reply_to_message_id=reply_to if reply_to else None
                )
            elif msg.video:
                sent = await context.bot.send_video(
                    chat_id=target_id,
                    video=msg.video.file_id,
                    caption=text_prefix,
                    reply_to_message_id=reply_to if reply_to else None
                )
            elif msg.voice:
                sent = await context.bot.send_voice(
                    chat_id=target_id,
                    voice=msg.voice.file_id,
                    caption=text_prefix,
                    reply_to_message_id=reply_to if reply_to else None
                )
            else:
                sent = await context.bot.send_message(
                    chat_id=target_id,
                    text=f"{text_prefix}\n(Loại tin chưa hỗ trợ)",
                    reply_to_message_id=reply_to if reply_to else None
                )

            # Lưu mapping reply
            message_map.setdefault((msg.chat_id, msg.message_id), {})[target_id] = sent.message_id

        except Exception as e:
            print(f"Lỗi khi chuyển tin nhắn cho {target_id}: {e}")


# ==== HANDLER ====
async def handle_new_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    sender_id = msg.chat_id
    if sender_id not in ID_TO_NAME:
        await msg.reply_text("❌ Bạn không có quyền sử dụng bot")
        return
    await forward_message(sender_id, msg, context)

async def handle_edited_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.edited_message
    sender_id = msg.chat_id
    if sender_id not in ID_TO_NAME:
        return
    await forward_message(sender_id, msg, context, edited=True)

# ==== CHẠY BOT ====
if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

    scheduler = AsyncIOScheduler(timezone=pytz.UTC)

    async def start_scheduler(app):
        scheduler.start()

    app = ApplicationBuilder().token(BOT_TOKEN).post_init(start_scheduler).build()

    app.add_handler(MessageHandler(filters.TEXT | filters.PHOTO | filters.VIDEO | filters.VOICE | filters.Document.ALL, handle_new_message))
    app.add_handler(EditedMessageHandler(handle_edited_message))

    print("🤖 Bot 3-người trung gian đang chạy...")
    app.run_polling()
