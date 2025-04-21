import os
import logging
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# ==== CẤU HÌNH ====
BOT_TOKEN = "7010265367:AAHT8PFy6R2KiiDKd4QTQ7c8iCegY_-dZk4"
CHAT_ID_B = 8000810390
CHAT_ID_C = 1707360759

# ==== LOGGING ====
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# ==== HÀM XỬ LÝ TIN NHẮN ====
async def relay_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sender_id = update.effective_chat.id
    receiver_id = None
    prefix = ""

    if sender_id == CHAT_ID_B:
        receiver_id = CHAT_ID_C
        prefix = "💬 B nói:"
    elif sender_id == CHAT_ID_C:
        receiver_id = CHAT_ID_B
        prefix = "💬 C nói:"
    else:
        await update.message.reply_text("❌ Bạn không có quyền sử dụng bot này.")
        return

    message = update.message

    if message.text:
        await context.bot.send_message(chat_id=receiver_id, text=f"{prefix}\n{message.text}")
    elif message.photo:
        await context.bot.send_photo(chat_id=receiver_id, photo=message.photo[-1].file_id, caption=prefix)
    elif message.video:
        await context.bot.send_video(chat_id=receiver_id, video=message.video.file_id, caption=prefix)
    elif message.voice:
        await context.bot.send_voice(chat_id=receiver_id, voice=message.voice.file_id, caption=prefix)
    elif message.document:
        await context.bot.send_document(chat_id=receiver_id, document=message.document.file_id, caption=prefix)
    else:
        await context.bot.send_message(chat_id=receiver_id, text=f"{prefix}\n(Đã nhận định dạng chưa hỗ trợ.)")

# ==== CHẠY BOT ====
if __name__ == "__main__":
    import pytz
    import asyncio
    from apscheduler.schedulers.asyncio import AsyncIOScheduler
    from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

    scheduler = AsyncIOScheduler(timezone=pytz.UTC)

    async def start_scheduler(app):
        scheduler.start()

    app = ApplicationBuilder().token(BOT_TOKEN).post_init(start_scheduler).build()
    app.add_handler(MessageHandler(filters.ALL, relay_message))

    print("🤖 Bot v20+ đang chạy...")
    app.run_polling()
