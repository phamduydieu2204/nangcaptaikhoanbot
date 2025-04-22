from telegram.ext import ApplicationBuilder
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import pytz
import logging
from handlers import register_handlers
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")

if __name__ == '__main__':
    logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

    scheduler = AsyncIOScheduler(timezone=pytz.UTC)
    async def start_scheduler(app):
        scheduler.start()

    app = ApplicationBuilder().token(BOT_TOKEN).post_init(start_scheduler).build()

    register_handlers(app)

    print("🤖 Bot phân tầng đang chạy...")
    app.run_polling()