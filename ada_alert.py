import os
import time
import requests
import schedule

# 🔑 Lee las credenciales desde las variables de entorno
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def get_ada_price():
    """Obtiene el precio de ADA en euros desde CoinGecko"""
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": "cardano", "vs_currencies": "eur"}
    try:
        response = requests.get(url, params=params)
        data = response.json()
        return data["cardano"]["eur"]
    except Exception as e:
        print("❌ Error obteniendo precio:", e)
        return None

def send_telegram_message(msg):
    """Envía un mensaje a tu chat de Telegram"""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": msg}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("❌ Error enviando mensaje:", e)

def check_price():
    """Consulta el precio y envía alerta si está en rango"""
    price = get_ada_price()
    if price:
        print(f"ADA = {price:.3f} €")
        if 0.70 <= price <= 0.72:
            send_telegram_message(f"🚀 ADA está en {price:.3f} € (¡Entre 0.70 y 0.72!)")

# 📌 Programar la tarea cada 1 minuto
schedule.every(1).minutes.do(check_price)

print("✅ Bot ADA iniciado... (comprobando cada minuto)")

while True:
    schedule.run_pending()
    time.sleep(1)
