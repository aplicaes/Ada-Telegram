import requests
import time
import os

# 🔑 Lee las credenciales desde las variables de entorno de Railway
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def get_ada_price():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": "cardano", "vs_currencies": "eur"}
    try:
        response = requests.get(url, params=params)
        data = response.json()
        return data["cardano"]["eur"]
    except Exception as e:
        print("Error obteniendo precio:", e)
        return None

def send_telegram_message(msg):
    url = "https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": msg}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("Error enviando mensaje:", e)

if __name__ == "__main__":
    while True:
        price = get_ada_price()
        if price:
            print(f"ADA = {price} €")
            if 0.70 <= price <= 0.72:
                send_telegram_message(f"🚀 ADA está en {price:.3f} € (¡Entre 0.70 y 0.72!)")
        time.sleep(30)  # cada 30 segundos

