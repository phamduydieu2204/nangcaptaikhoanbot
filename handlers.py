from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
from config import GROUP
from logic import forward_message

def register_handlers(app):
    async def handle_new(update: Update, context: ContextTypes.DEFAULT_TYPE):
        msg = update.message
        sender_id = msg.chat_id
        if sender_id not in GROUP:
            await msg.reply_text("❌ Bạn không có quyền truy cập.")
            return
        await forward_message(sender_id, msg, context)

    async def handle_edited(update: Update, context: ContextTypes.DEFAULT_TYPE):
        msg = update.edited_message
        sender_id = msg.chat_id
        if sender_id not in GROUP:
            return
        await forward_message(sender_id, msg, context, edited=True)

    app.add_handler(MessageHandler(filters.ALL, handle_new))
    app.add_handler(MessageHandler(filters.ALL & filters.UpdateType.EDITED_MESSAGE, handle_edited))