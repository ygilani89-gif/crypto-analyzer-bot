import os
import requests
import time
from telegram import Bot
from telegram.error import TelegramError
import asyncio

# تنظیمات
BOT_TOKEN = "8833513223:AAFRlYKnILXTD5bA3xDWoPiks1d3D4OCTss"
CHAT_ID = "@crypto_analyzer_mohsen_bot"  # اسم کانالت
API_URL = "https://api.coingecko.com/api/v3"

bot = Bot(token=BOT_TOKEN)

# لیست ارزهایی که می‌خوایم تحلیل کنیم
CRYPTOCURRENCIES = {
    "bitcoin": "Bitcoin 🪙",
    "ethereum": "Ethereum 💎"
}

def get_crypto_data():
    """قیمت ارزها رو دریافت کن"""
    try:
        ids = ",".join(CRYPTOCURRENCIES.keys())
        url = f"{API_URL}/simple/price?ids={ids}&vs_currencies=usd&include_24hr_change=true"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ خطا در دریافت اطلاعات: {e}")
        return None

def analyze_crypto(data):
    """تحلیل قیمت‌ها"""
    if not data:
        return None
    
    message = "📊 *تحلیل بازار ارزهای دیجیتال* 📊\n"
    message += f"⏰ ساعت: {time.strftime('%H:%M:%S')}\n"
    message += "=" * 40 + "\n\n"
    
    for crypto_id, crypto_name in CRYPTOCURRENCIES.items():
        if crypto_id in data:
            price = data[crypto_id].get("usd", 0)
            change = data[crypto_id].get("usd_24h_change", 0)
            
            # تعیین سیگنال
            if change > 5:
                signal = "🟢 خریدار (قوی)"
            elif change > 0:
                signal = "🟡 خریدار (ضعیف)"
            elif change > -5:
                signal = "🔴 فروشنده (ضعیف)"
            else:
                signal = "🔴 فروشنده (قوی)"
            
            message += f"{crypto_name}\n"
            message += f"💵 قیمت: ${price:,.2f}\n"
            message += f"📈 تغییر 24 ساعت: {change:+.2f}%\n"
            message += f"🎯 سیگنال: {signal}\n"
            message += "-" * 40 + "\n\n"
    
    return message

async def send_analysis():
    """ارسال تحلیل به کانال"""
    while True:
        try:
            data = get_crypto_data()
            message = analyze_crypto(data)
            
            if message:
                # ارسال به کانال
                try:
                    await bot.send_message(
                        chat_id=CHAT_ID,
                        text=message,
                        parse_mode='Markdown'
                    )
                    print("✅ تحلیل ارسال شد!")
                except TelegramError as e:
                    print(f"❌ خطا در ارسال: {e}")
            
            # منتظر 1 ساعت
            print("⏳ منتظر ساعت بعد...")
            await asyncio.sleep(3600)
            
        except Exception as e:
            print(f"❌ خطا: {e}")
            await asyncio.sleep(60)

if __name__ == "__main__":
    print("🚀 ربات شروع شد...")
    asyncio.run(send_analysis())
