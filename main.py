import telebot
from telebot import types

TOKEN = "import telebot
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
"

bot = telebot.TeleBot(TOKEN)

EMPIRES = {
    "Temuriylar imperiyasi": {
        "specialization": "Harbiy / Ilm-fan",
        "gold": 100_000_000,
        "capital": "Samarqand",
        "cities": ["Samarqand", "Buxoro", "Hirot", "Shahrisabz", "Toshkent", "Marv", "Nishapur"]
    },
    "Omaviylar xalifaligi": {
        "specialization": "Diplomatiya / Kengayish",
        "gold": 100_000_000,
        "capital": "Damashq",
        "cities": ["Damashq", "Kufa", "Basra", "Quddus", "Fustot", "Qayravon", "Qurtuba"]
    },
    "Ayyubiylar sulolasi": {
        "specialization": "Harbiy / Himoya",
        "gold": 100_000_000,
        "capital": "Qohira",
        "cities": ["Qohira", "Aleppo", "Damashq", "Hims", "Quddus", "Hama", "Baalbek"]
    },
    "Britaniya imperiyasi": {
        "specialization": "Iqtisodiy / Savdo",
        "gold": 100_000_000,
        "capital": "London",
        "cities": ["London", "Liverpul", "Edinburg", "Dublin", "Sidney", "Dehli", "Kape-Taun"]
    }
}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_profile = types.InlineKeyboardButton("🏰 Mening Imperiyam", callback_data="my_empire")
    btn_map = types.InlineKeyboardButton("🗺️ Xarita", callback_data="map")
    btn_diplomacy = types.InlineKeyboardButton("🤝 Diplomatiya", callback_data="diplomacy")
    btn_upgrade = types.InlineKeyboardButton("⚙️ Rivojlantirish", callback_data="upgrade")
    
    markup.add(btn_profile, btn_map, btn_diplomacy, btn_upgrade)
    
    welcome_text = (
        "⚔️ **Sivilizatsiya Strategiyasiga xush kelibsiz!**\n\n"
        "Bu yerda siz buyuk imperiyaga boshchilik qilasiz, 7 ta shahringizni himoya qilasiz, "
        "tilla tangalaringizni ko'paytirasiz va dunyoni zabt etasiz.\n\n"
        "Quyidagi menyudan kerakli bo'limni tanlang:"
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "my_empire":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "🏰 Siz hali davlat tanlamadingiz. Tez orada davlat tanlash ro'yxati chiqadi!")
    elif call.data == "map":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "🗺️ Dunyo xaritasi yuklanmoqda... (Hozircha hududiy tarmoqlar tuzilmoqda)")
    elif call.data == "diplomacy":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "🤝 Alyanslar va vassallik tizimi tez kunda ishga tushadi.")
    elif call.data == "upgrade":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "⚙️ Shahar devorlari va garnizonni yaxshilash bo'limi.")

print("Bot muvaffaqiyatli ishga tushdi...")
bot.infinity_polling()
