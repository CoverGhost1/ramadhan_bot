import requests
import time
import asyncio
from datetime import datetime, timedelta
import pytz
from telegram import Bot

TOKEN = "7660181456:AAHmmuC6VNRQ_u4tyJHqFJ0cBlXZebugTdA"
GROUP_ID = -1003123683403

LAT = -6.9175
LON = 106.9290

TIMEZONE = "Asia/Jakarta"

bot = Bot(token=TOKEN)

async def send(msg):
    try:
        await bot.send_message(chat_id=GROUP_ID, text=msg)
        print("Sent:", msg)
    except Exception as e:
        print("Error:", e)

def get_timings():
    url = f"https://api.aladhan.com/v1/timings?latitude={LAT}&longitude={LON}&method=11"
    data = requests.get(url).json()
    
    subuh = data["data"]["timings"]["Fajr"]
    maghrib = data["data"]["timings"]["Maghrib"]
    
    return subuh, maghrib


def run():

    tz = pytz.timezone(TIMEZONE)
    sent_today = set()

    while True:

        now = datetime.now(tz)
        current_time = now.strftime("%H:%M")
        today = now.strftime("%Y-%m-%d")

        subuh, maghrib = get_timings()

        subuh_dt = datetime.strptime(subuh, "%H:%M")
        maghrib_dt = datetime.strptime(maghrib, "%H:%M")

        times = {
            (subuh_dt - timedelta(minutes=30)).strftime("%H:%M"): "🌙 30 menit lagi masuk waktu Subuh",
            (subuh_dt - timedelta(minutes=10)).strftime("%H:%M"): "⚠️ 10 menit lagi masuk waktu Subuh",
            (subuh_dt - timedelta(minutes=5)).strftime("%H:%M"): "⏳ 5 menit lagi masuk waktu Subuh",
            subuh: "🕌 Subuh telah tiba. Selamat berpuasa 🤍",

            (maghrib_dt - timedelta(minutes=30)).strftime("%H:%M"): "🌇 30 menit lagi waktu berbuka",
            (maghrib_dt - timedelta(minutes=10)).strftime("%H:%M"): "⏳ 10 menit lagi waktu berbuka",
            (maghrib_dt - timedelta(minutes=5)).strftime("%H:%M"): "⏳ 5 menit lagi waktu berbuka",
            maghrib: "🕌 Adzan Maghrib telah tiba. Selamat berbuka 🤍"
        }

        key = f"{today}-{current_time}"

        if key not in sent_today and current_time in times:
            asyncio.run(send(times[current_time]))
            sent_today.add(key)

        time.sleep(20)

print("Bot running...")
asyncio.run(send("its from railway!"))
run()
