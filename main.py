import telebot
from telebot import types

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
