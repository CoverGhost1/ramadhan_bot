import requests
import time
from datetime import datetime, timedelta
import pytz
from telegram import Bot

# =========================
# CONFIG
# =========================

TOKEN = "7660181456:AAHmmuC6VNRQ_u4tyJHqFJ0cBlXZebugTdA"
GROUP_ID = -1003123683403

# Koordinat Sukabumi (akurasi bagus untuk Jawa Barat selatan)
LAT = -6.9175
LON = 106.9290

TIMEZONE = "Asia/Jakarta"

bot = Bot(token=TOKEN)

# =========================
# AMBIL JADWAL SHOLAT
# =========================

def get_timings():
    url = f"https://api.aladhan.com/v1/timings?latitude={LAT}&longitude={LON}&method=11"
    data = requests.get(url).json()
    
    subuh = data["data"]["timings"]["Fajr"]
    maghrib = data["data"]["timings"]["Maghrib"]
    
    return subuh, maghrib


# =========================
# FORMAT MESSAGE
# =========================

def send(msg):
    try:
        bot.send_message(GROUP_ID, msg)
        print("Sent:", msg)
    except:
        print("Failed send")


# =========================
# MAIN LOOP
# =========================

def run():

    tz = pytz.timezone(TIMEZONE)
    
    sent_today = set()

    while True:

        now = datetime.now(tz)
        current_time = now.strftime("%H:%M")
        today = now.strftime("%Y-%m-%d")

        subuh, maghrib = get_timings()

        # convert
        subuh_dt = datetime.strptime(subuh, "%H:%M")
        maghrib_dt = datetime.strptime(maghrib, "%H:%M")

        # countdown times
        subuh_30 = (subuh_dt - timedelta(minutes=30)).strftime("%H:%M")
        subuh_10 = (subuh_dt - timedelta(minutes=10)).strftime("%H:%M")
        subuh_5 = (subuh_dt - timedelta(minutes=5)).strftime("%H:%M")

        maghrib_30 = (maghrib_dt - timedelta(minutes=30)).strftime("%H:%M")
        maghrib_10 = (maghrib_dt - timedelta(minutes=10)).strftime("%H:%M")
        maghrib_5 = (maghrib_dt - timedelta(minutes=5)).strftime("%H:%M")

        key = f"{today}-{current_time}"

        if key not in sent_today:

            # SUBUH countdown
            if current_time == subuh_30:
                send("🌙 30 menit lagi masuk waktu Subuh\nWaktu sahur masih tersedia")

            elif current_time == subuh_10:
                send("⚠️ 10 menit lagi masuk waktu Subuh\nSegera selesaikan sahur")

            elif current_time == subuh_5:
                send("⏳ 5 menit lagi masuk waktu Subuh\nPersiapkan niat puasamu")

            elif current_time == subuh:
                send("🕌 Subuh telah tiba\nSelamat menjalankan ibadah puasa 🤍")


            # MAGHRIB countdown
            elif current_time == maghrib_30:
                send("🌇 30 menit lagi waktu berbuka\nTetap semangat 🤍")

            elif current_time == maghrib_10:
                send("⏳ 10 menit lagi waktu berbuka\nSiapkan makanan terbaikmu")

            elif current_time == maghrib_5:
                send("⏳ 5 menit lagi waktu berbuka\nWaktu yang dinanti hampir tiba")

            elif current_time == maghrib:
                send("🕌 Adzan Maghrib telah tiba\nSelamat berbuka puasa 🤍")

            sent_today.add(key)

        time.sleep(20)


# =========================

print("Bot running...")
run()
