import os
import time
import requests
from telegram import Bot, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Updater

BOT_TOKEN = os.getenv("BOT_TOKEN")
USER_ID = int(os.getenv("USER_ID"))
THRESHOLD = float(os.getenv("THRESHOLD", 2.5))
AVG_HOURS = int(os.getenv("AVG_HOURS", 3))
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 5))

bot = Bot(token=BOT_TOKEN)

menu_keyboard = ReplyKeyboardMarkup(
    [['🔄 شروع پایش', '⛔ توقف پایش'],
     ['🕒 میانگین ساعتی', '📈 آستانه پامپ'],
     ['⏱️ فاصله بررسی']],
    resize_keyboard=True
)

def start(update, context):
    if update.effective_user.id != USER_ID:
        return
    update.message.reply_text('ربات پامپ‌گیر فعال شد! 🚀', reply_markup=menu_keyboard)

def unknown(update, context):
    if update.effective_user.id != USER_ID:
        return
    update.message.reply_text("دستور نامعتبره. لطفاً از منو استفاده کن.")

def start_alerts(update, context):
    if update.effective_user.id != USER_ID:
        return
    update.message.reply_text("🔄 پایش پامپ‌ها شروع شد (شبیه‌سازی)...")

def stop_alerts(update, context):
    if update.effective_user.id != USER_ID:
        return
    update.message.reply_text("⛔ پایش متوقف شد.")

def set_threshold(update, context):
    pass  # این قسمت می‌تونه گسترش پیدا کنه برای تنظیم مقدار آستانه

updater = Updater(BOT_TOKEN, use_context=True)
dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("startalerts", start_alerts))
dp.add_handler(CommandHandler("stopalerts", stop_alerts))
dp.add_handler(CommandHandler("setthreshold", set_threshold))
dp.add_handler(CommandHandler(None, unknown))

updater.start_polling()
updater.idle()