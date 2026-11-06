import os
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import telebot
from telebot import types

# Render port talab qilgani uchun fon serveri
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    server.serve_forever()

threading.Thread(target=run_server, daemon=True).start()

TOKEN = "9163206553:AAEjs1mCITIow9KnvmTjGzr6f0wNdHmlRvQ"
bot = telebot.TeleBot(TOKEN)

# O'yin ma'lumotlari va foydalanuvchilar tanlovi
EMPIRES = {
    "temuriylar": {
        "name": "Temuriylar imperiyasi",
        "specialization": "Harbiy / Ilm-fan",
        "gold": 100_000_000,
        "capital": "Samarqand",
        "cities": ["Samarqand", "Buxoro", "Hirot"]
    },
    "omaviylar": {
        "name": "Omaviylar xalifaligi",
        "specialization": "Diplomatiya / Kengayish",
        "gold": 100_000_000,
        "capital": "Damashq",
        "cities": ["Damashq", "Kufa", "Basra"]
    },
    "ayyubiylar": {
        "name": "Ayyubiylar sulolasi",
        "specialization": "Harbiy / Himoya",
        "gold": 100_000_000,
        "capital": "Qohira",
        "cities": ["Qohira", "Aleppo", "Damashq"]
    },
    "britaniya": {
        "name": "Britaniya imperiyasi",
        "specialization": "Iqtisodiy / Savdo",
        "gold": 100_000_000,
        "capital": "London",
        "cities": ["London", "Liverpul", "Edinburg"]
    }
}

user_empires = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    for key, val in EMPIRES.items():
        markup.add(types.InlineKeyboardButton(f"👑 {val['name']}", callback_data=f"select_{key}"))
    
    bot.reply_to(message, "Salom! Sivilizatsiya o'yiniga xush kelibsiz.\nO'yinni boshlash uchun o'z imperiyangizni tanlang:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    user_id = call.from_user.id
    
    if call.data.startswith("select_"):
        emp_key = call.data.split("_")[1]
        user_empires[user_id] = emp_key
        emp = EMPIRES[emp_key]
        
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("📜 Profil", callback_data="profile"),
            types.InlineKeyboardButton("🗺 Xarita", callback_data="map")
        )
        
        bot.answer_callback_query(call.id, f"Tabriklayman! Siz {emp['name']}ni tanladingiz.")
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f"✅ **Sizning tanlovingiz:** {emp['name']}\n\n"
                 f"🏛 **Poytaxt:** {emp['capital']}\n"
                 f"⚔️ **Ixtisoslashuv:** {emp['specialization']}\n"
                 f"💰 **Xazina:** {emp['gold']:,} oltin\n\n"
                 f"Quyidagi menyudan foydalaning:",
            reply_markup=markup,
            parse_mode="Markdown"
        )
        
    elif call.data == "profile":
        emp_key = user_empires.get(user_id)
        if not emp_key:
            bot.answer_callback_query(call.id, "Siz hali imperiya tanlamagansiz! /start ni bosing.", show_alert=True)
            return
        
        emp = EMPIRES[emp_key]
        bot.answer_callback_query(call.id)
        bot.send_message(
            call.message.chat.id,
            f"📜 **Sizning Imperiyangiz Profili:**\n\n"
            f"👑 Nomi: {emp['name']}\n"
            f"🏛 Poytaxt: {emp['capital']}\n"
            f"🏙 Shaharlar: {', '.join(emp['cities'])}\n"
            f"💰 Xazina: {emp['gold']:,} oltin",
            parse_mode="Markdown"
        )
        
    elif call.data == "map":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "🗺 **Global Xarita:**\n\nHozircha xarita bo'sh, tez orada bu yerda hududlarni zabt etish qo'shiladi!", parse_mode="Markdown")

if __name__ == '__main__':
    print("Bot ishga tushdi...")
    while True:
        try:
            bot.remove_webhook()
            bot.infinity_polling(skip_pending=True)
        except Exception as e:
            print(f"Xatolik yuz berdi: {e}")
            time.sleep(5)
