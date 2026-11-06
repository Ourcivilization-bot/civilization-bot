import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import telebot
from telebot import types

# Render port talab qilgani uchun kichik fon serveri
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    server.serve_forever()

# Serverni alohida oqimda (thread) ishga tushiramiz
threading.Thread(target=run_server, daemon=True).start()

TOKEN = "9163206553:AAEjs1mCITIow9KnvmTjGzr6f0wNdHmlRvQ"

bot = telebot.TeleBot(TOKEN)

EMPIRES = {
    "Temuriylar imperiyasi": {
        "specialization": "Harbiy / Ilm-fan",
        "gold": 100_000_000,
        "capital": "Samarqand",
        "cities": ["Samarqand", "Buxoro", "Hirot"]
    },
    "Omaviylar xalifaligi": {
        "specialization": "Diplomatiya / Kengayish",
        "gold": 100_000_000,
        "capital": "Damashq",
        "cities": ["Damashq", "Kufa", "Basra"]
    },
    "Ayyubiylar sulolasi": {
        "specialization": "Harbiy / Himoya",
        "gold": 100_000_000,
        "capital": "Qohira",
        "cities": ["Qohira", "Aleppo", "Damashq"]
    },
    "Britaniya imperiyasi": {
        "specialization": "Iqtisodiy / Savdo",
        "gold": 100_000_000,
        "capital": "London",
        "cities": ["London", "Liverpul", "Edinburg"]
    }
}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_profile = types.InlineKeyboardButton("📜 Profil", callback_data="profile")
    btn_map = types.InlineKeyboardButton("🗺 Xarita", callback_data="map")
    markup.add(btn_profile, btn_map)
    bot.reply_to(message, "Salom! Sivilizatsiya o'yiniga xush kelibsiz. Imperiyangizni tanlang:", reply_markup=markup)

if __name__ == '__main__':
    print("Bot ishga tushdi...")
    bot.infinity_polling(skip_pending=True)
