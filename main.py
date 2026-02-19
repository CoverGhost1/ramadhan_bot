import requests
import asyncio
import pytz
from datetime import datetime, timedelta
from telegram import Bot

TOKEN = "7660181456:AAHmmuC6VNRQ_u4tyJHqFJ0cBlXZebugTdA"
GROUP_ID = -1003123683403

LAT = -6.820080
LON = 107.173859

TIMEZONE = "Asia/Jakarta"

bot = Bot(token=TOKEN)

# =====================
# SEND MESSAGE
# =====================

async def send(msg):
    try:
        await bot.send_message(chat_id=GROUP_ID, text=msg)
        print("Sent:", msg)
    except Exception as e:
        print("Error:", e)


# =====================
# GET PRAYER TIMES
# =====================

def get_timings():
    url = f"https://api.aladhan.com/v1/timings?latitude={LAT}&longitude={LON}&method=11"
    data = requests.get(url).json()
    
    return (
        data["data"]["timings"]["Fajr"],
        data["data"]["timings"]["Maghrib"]
    )


# =====================
# MAIN LOOP
# =====================

async def main():

    tz = pytz.timezone(TIMEZONE)
    sent_today = set()

    print("Bot running...")
    await send("✅ Bot aktif dari Railway!")

    while True:

        now = datetime.now(tz)
        current = now.strftime("%H:%M")
        today = now.strftime("%Y-%m-%d")

        subuh, maghrib = get_timings()

        subuh_dt = datetime.strptime(subuh, "%H:%M")
        maghrib_dt = datetime.strptime(maghrib, "%H:%M")

        schedule = {
            (subuh_dt - timedelta(minutes=30)).strftime("%H:%M"):
                "🌙 30 menit lagi masuk waktu Subuh",

            (subuh_dt - timedelta(minutes=10)).strftime("%H:%M"):
                "⚠️ 10 menit lagi masuk waktu Subuh",

            (subuh_dt - timedelta(minutes=5)).strftime("%H:%M"):
                "⏳ 5 menit lagi masuk waktu Subuh",

            subuh:
                "🕌 Subuh telah tiba. Selamat berpuasa 🤍",

            (maghrib_dt - timedelta(minutes=30)).strftime("%H:%M"):
                "🌇 30 menit lagi waktu berbuka",

            (maghrib_dt - timedelta(minutes=10)).strftime("%H:%M"):
                "⏳ 10 menit lagi waktu berbuka",

            (maghrib_dt - timedelta(minutes=5)).strftime("%H:%M"):
                "⏳ 5 menit lagi waktu berbuka",

            maghrib:
                "🕌 Adzan Maghrib telah tiba. Selamat berbuka 🤍"
        }

        key = f"{today}-{current}"

        if key not in sent_today and current in schedule:
            await send(schedule[current])
            sent_today.add(key)

        await asyncio.sleep(30)


# =====================

asyncio.run(main())
