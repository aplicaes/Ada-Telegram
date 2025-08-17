import requests, time, os, schedule

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def get_ada_price():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": "cardano", "vs_currencies": "eur"}
    return requests.get(url, params=params).json()["cardano"]["eur"]

def send_telegram_message(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def job():
    price = get_ada_price()
    print(f"ADA = {price} €")
    if 0.70 <= price <= 0.72:
        send_telegram_message(f"🚀 ADA está en {price:.3f} € (¡Entre 0.70 y 0.84!)")

# Ejecutar cada minuto
schedule.every(30).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(30)
