import requests
import time
import telebot
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
USER_ID = int(os.getenv("USER_ID"))
bot = telebot.TeleBot(BOT_TOKEN)

BASE_URL = "https://api.binance.com"

user_settings = {}

def get_price_data(symbol, interval, limit=12):
    url = f"{BASE_URL}/api/v3/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    try:
        response = requests.get(url, params=params)
        data = response.json()
        closes = [float(candle[4]) for candle in data]
        return closes
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return []

def check_pumps(interval, threshold):
    url = f"{BASE_URL}/api/v3/ticker/price"
    prices = requests.get(url).json()
    for pair in prices:
        symbol = pair['symbol']
        if not symbol.endswith("USDT"):
            continue
        price_now = float(pair['price'])
        closes = get_price_data(symbol, interval)
        if not closes:
            continue
        avg_price = sum(closes[:-1]) / len(closes[:-1])
        change = (price_now - avg_price) / avg_price * 100
        if change >= threshold:
            bot.send_message(USER_ID, f"📈 پامپ {change:.2f}% در {symbol} مشاهده شد.")

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "👋 تایم‌فریم نمودار را وارد کن (مثلاً 2h یا 3h):")

@bot.message_handler(func=lambda m: m.chat.id == USER_ID and 'h' in m.text.lower())
def get_interval(message):
    user_settings['interval'] = message.text.lower()
    bot.send_message(message.chat.id, "🔢 حالا درصد رشد مورد نظر برای هشدار را بنویس (مثلاً 1 برای 1٪):")

@bot.message_handler(func=lambda m: m.chat.id == USER_ID and m.text.isdigit())
def get_threshold(message):
    user_settings['threshold'] = float(message.text)
    bot.send_message(message.chat.id, "✅ تنظیمات ذخیره شد. پایش شروع شد.")
    while True:
        check_pumps(user_settings['interval'], user_settings['threshold'])
        time.sleep(300)  # every 5 minutes

bot.polling()
