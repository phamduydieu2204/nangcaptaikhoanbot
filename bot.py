from telegram import Update, Bot
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext

# ==== THÔNG TIN CẤU HÌNH ====
BOT_TOKEN = "🔑_THAY_BẰNG_TOKEN_BOT_CỦA_BẠN"
CHAT_ID_B = 8000810390      # Thay bằng chat_id của tài khoản B
CHAT_ID_C = 1707360759      # Thay bằng chat_id của tài khoản C

# ==== HÀM CHUYỂN TIẾP ====
def relay_message(update: Update, context: CallbackContext):
    sender_id = update.effective_chat.id
    bot: Bot = context.bot
    receiver_id = None

    if sender_id == CHAT_ID_B:
        receiver_id = CHAT_ID_C
        prefix = "💬 B nói:"
    elif sender_id == CHAT_ID_C:
        receiver_id = CHAT_ID_B
        prefix = "💬 C nói:"
    else:
        update.message.reply_text("❌ Bạn không có quyền sử dụng bot này.")
        return

    # ===== XỬ LÝ TIN NHẮN TEXT =====
    if update.message.text:
        bot.send_message(chat_id=receiver_id, text=f"{prefix}\n{update.message.text}")

    # ===== ẢNH =====
    elif update.message.photo:
        bot.send_photo(chat_id=receiver_id,
                       photo=update.message.photo[-1].file_id,
                       caption=prefix)

    # ===== VIDEO =====
    elif update.message.video:
        bot.send_video(chat_id=receiver_id,
                       video=update.message.video.file_id,
                       caption=prefix)

    # ===== VOICE (tin nhắn thoại) =====
    elif update.message.voice:
        bot.send_voice(chat_id=receiver_id,
                       voice=update.message.voice.file_id,
                       caption=prefix)

    # ===== FILE HOẶC KHÁC =====
    elif update.message.document:
        bot.send_document(chat_id=receiver_id,
                          document=update.message.document.file_id,
                          caption=prefix)
    else:
        bot.send_message(chat_id=receiver_id,
                         text=f"{prefix}\n(Đã nhận một định dạng chưa hỗ trợ.)")

# ==== CHẠY BOT ====
def main():
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.all, relay_message))

    print("🤖 Bot chuyển tiếp đang chạy...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
