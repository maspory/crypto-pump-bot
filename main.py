
import os
import time
import requests
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext

TOKEN = os.getenv("BOT_TOKEN")
USER_ID = int(os.getenv("USER_ID"))

# متغیرهای قابل تغییر با دستورات تلگرام — مقادیر پیش‌فرض
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 5))
AVG_HOURS = int(os.getenv("AVG_HOURS", 2))
THRESHOLD = float(os.getenv("THRESHOLD", 2))

bot = Bot(token=TOKEN)

# تابع اصلی بررسی پامپ (جایگزین با تابع واقعی بررسی بازار می‌شود)
def check_market():
    print(f"Checking market: interval={CHECK_INTERVAL}, avg={AVG_HOURS}, threshold={THRESHOLD}")
    # شبیه‌سازی هشدار
    bot.send_message(chat_id=USER_ID, text=f"📈 پامپ شناسایی شد! Threshold={THRESHOLD}%")

def start(update: Update, context: CallbackContext):
    if update.effective_user.id != USER_ID:
        return
    update.message.reply_text("✅ ربات فعال است. از دستورات /set_... استفاده کنید.")

def set_interval(update: Update, context: CallbackContext):
    global CHECK_INTERVAL
    if update.effective_user.id != USER_ID:
        return
    try:
        CHECK_INTERVAL = int(context.args[0])
        update.message.reply_text(f"⏱ بازه چک تنظیم شد به {CHECK_INTERVAL} دقیقه.")
    except:
        update.message.reply_text("❌ فرمت اشتباه است. مثال: /set_interval 5")

def set_avg(update: Update, context: CallbackContext):
    global AVG_HOURS
    if update.effective_user.id != USER_ID:
        return
    try:
        AVG_HOURS = int(context.args[0])
        update.message.reply_text(f"🕒 میانگین ساعتی تنظیم شد به {AVG_HOURS} ساعت.")
    except:
        update.message.reply_text("❌ فرمت اشتباه است. مثال: /set_avg 2")

def set_threshold(update: Update, context: CallbackContext):
    global THRESHOLD
    if update.effective_user.id != USER_ID:
        return
    try:
        THRESHOLD = float(context.args[0])
        update.message.reply_text(f"📊 آستانه پامپ تنظیم شد به {THRESHOLD}%")
    except:
        update.message.reply_text("❌ فرمت اشتباه است. مثال: /set_threshold 2.5")

def main():
    updater = Updater(token=TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("set_interval", set_interval))
    dp.add_handler(CommandHandler("set_avg", set_avg))
    dp.add_handler(CommandHandler("set_threshold", set_threshold))

    updater.start_polling()

    # حلقه بررسی پامپ هر چند دقیقه یکبار
    while True:
        check_market()
        time.sleep(CHECK_INTERVAL * 60)

if __name__ == '__main__':
    main()
