import os
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import telebot
from telebot import types

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

EMPIRES = {
    "temuriylar": {
        "name": "Temuriylar imperiyasi",
        "group": "Sharq va Islom olami",
        "specialization": "Harbiy / Ilm-fan",
        "gold": 100_000_000,
        "capital": "Samarqand",
        "cities": ["Samarqand", "Buxoro", "Hirot"]
    },
    "omaviylar": {
        "name": "Omaviylar xalifaligi",
        "group": "Sharq va Islom olami",
        "specialization": "Diplomatiya / Kengayish",
        "gold": 100_000_000,
        "capital": "Damashq",
        "cities": ["Damashq", "Kufa", "Basra"]
    },
    "abbosiylar": {
        "name": "Abbosiylar xalifaligi",
        "group": "Sharq va Islom olami",
        "specialization": "Ilm-fan / Madaniyat",
        "gold": 100_000_000,
        "capital": "Bagdod",
        "cities": ["Bagdod", "Qohira", "Basra"]
    },
    "usmonlilar": {
        "name": "Usmonlilar imperiyasi",
        "group": "Sharq va Islom olami",
        "specialization": "Harbiy / Dengiz floti",
        "gold": 100_000_000,
        "capital": "Istanbul",
        "cities": ["Istanbul", "Edirne", "Bursa"]
    },
    "ayyubiylar": {
        "name": "Ayyubiylar sulolasi",
        "group": "Sharq va Islom olami",
        "specialization": "Harbiy / Himoya",
        "gold": 100_000_000,
        "capital": "Qohira",
        "cities": ["Qohira", "Aleppo", "Damashq"]
    },
    "xorazmshohlar": {
        "name": "Xorazmshohlar davlati",
        "group": "Sharq va Islom olami",
        "specialization": "Savdo / Kengayish",
        "gold": 100_000_000,
        "capital": "Kunya-Urganch",
        "cities": ["Urganch", "Gurlan", "Marv", "Samarqand"]
    },
    "gaznaviylar": {
        "name": "Gaznaviylar davlati",
        "group": "Sharq va Islom olami",
        "specialization": "Harbiy / Bosqinchilik",
        "gold": 100_000_000,
        "capital": "Gazna",
        "cities": ["Gazna", "Lahor", "Balx"]
    },
    "safaviylar": {
        "name": "Safaviylar imperiyasi",
        "group": "Sharq va Islom olami",
        "specialization": "Madaniyat / Savdo",
        "gold": 100_000_000,
        "capital": "Isfahon",
        "cities": ["Isfahon", "Tebriz", "Sheroz"]
    },
    "boburiylar": {
        "name": "Boburiylar imperiyasi",
        "group": "Sharq va Islom olami",
        "specialization": "Arxitektura / Boylik",
        "gold": 100_000_000,
        "capital": "Dehli",
        "cities": ["Dehli", "Agra", "Lahor"]
    },
    "oltin_orda": {
        "name": "Oltin Orda",
        "group": "Sharq va Islom olami",
        "specialization": "Kochmanchi qudrati / Soliq",
        "gold": 100_000_000,
        "capital": "Saroy-Bot",
        "cities": ["Saroy-Bot", "Qozon", "Astraxan"]
    },
    "britaniya": {
        "name": "Britaniya imperiyasi",
        "group": "Yevropa va Jahon",
        "specialization": "Iqtisodiy / Savdo",
        "gold": 100_000_000,
        "capital": "London",
        "cities": ["London", "Liverpul", "Edinburg"]
    },
    "rim": {
        "name": "Rim imperiyasi",
        "group": "Yevropa va Jahon",
        "specialization": "Infratuzilma / Legionlar",
        "gold": 100_000_000,
        "capital": "Rim",
        "cities": ["Rim", "Milano", "Afina"]
    },
    "fransiya": {
        "name": "Fransiya imperiyasi",
        "group": "Yevropa va Jahon",
        "specialization": "Diplomatiya / Madaniyat",
        "gold": 100_000_000,
        "capital": "Parij",
        "cities": ["Parij", "Marsel", "Lion"]
    },
    "rossiya": {
        "name": "Rossiya imperiyasi",
        "group": "Yevropa va Jahon",
        "specialization": "Hudud / Resurslar",
        "gold": 100_000_000,
        "capital": "Sankt-Peterburg",
        "cities": ["Moskva", "Sankt-Peterburg", "Kiyev"]
    },
    "ispan": {
        "name": "Ispaniya imperiyasi",
        "group": "Yevropa va Jahon",
        "specialization": "Dengiz sayohati / Oltin",
        "gold": 100_000_000,
        "capital": "Madrid",
        "cities": ["Madrid", "Barselona", "Seviliya"]
    },
    "germaniya": {
        "name": "Germaniya imperiyasi",
        "group": "Yevropa va Jahon",
        "specialization": "Sanoat / Ilm-fan",
        "gold": 100_000_000,
        "capital": "Berlin",
        "cities": ["Berlin", "Myunxen", "Gamburg"]
    },
    "avstriya_vengriya": {
        "name": "Avstriya-Vengriya",
        "group": "Yevropa va Jahon",
        "specialization": "Kopmillatli / Birlik",
        "gold": 100_000_000,
        "capital": "Vena",
        "cities": ["Vena", "Budapesht", "Praga"]
    },
    "shved": {
        "name": "Shved imperiyasi",
        "group": "Yevropa va Jahon",
        "specialization": "Harbiy taktika / Temir",
        "gold": 100_000_000,
        "capital": "Stokgolm",
        "cities": ["Stokgolm", "Gteborg", "Malmo"]
    },
    "vizantiya": {
        "name": "Vizantiya imperiyasi",
        "group": "Yevropa va Jahon",
        "specialization": "Diplomatiya / Diniy markaz",
        "gold": 100_000_000,
        "capital": "Konstantinopol",
        "cities": ["Konstantinopol", "Saloniki", "Trabzon"]
    },
    "gon_sivar": {
        "name": "Muqaddas Rim imperiyasi",
        "group": "Yevropa va Jahon",
        "specialization": "Diniy tasir / Birlik",
        "gold": 100_000_000,
        "capital": "Aaxen",
        "cities": ["Aaxen", "Frankfurt", "Vyana"]
    },
    "mongol": {
        "name": "Mogullar imperiyasi",
        "group": "Antik va Osiyo",
        "specialization": "Tezkor yurish / Qoshin",
        "gold": 100_000_000,
        "capital": "Qoraqurum",
        "cities": ["Qoraqurum", "Pekin", "Tabriz"]
    },
    "xunnu": {
        "name": "Buyuk Xunnu imperiyasi",
        "group": "Antik va Osiyo",
        "specialization": "Otliq qoshin / Erkinlik",
        "gold": 100_000_000,
        "capital": "Utuken",
        "cities": ["Utuken", "Orxon", "Gobi"]
    },
    "qadimgi_xitoy": {
        "name": "Sin imperiyasi (Xitoy)",
        "group": "Antik va Osiyo",
        "specialization": "Aholi / Devor qurilishi",
        "gold": 100_000_000,
        "capital": "Sian",
        "cities": ["Sian", "Pekin", "Shanxay"]
    },
    "fors_ahamoniylar": {
        "name": "Ahamoniylar imperiyasi (Fors)",
        "group": "Antik va Osiyo",
        "specialization": "Logistika / Shoh yoli",
        "gold": 100_000_000,
        "capital": "Persepol",
        "cities": ["Persepol", "Susa", "Bobil"]
    },
    "qadimgi_misr": {
        "name": "Qadimgi Misr",
        "group": "Antik va Osiyo",
        "specialization": "Obidalar / Nil daryosi",
        "gold": 100_000_000,
        "capital": "Memfis",
        "cities": ["Memfis", "Tiva", "Aleksandriya"]
    },
    "makedoniya": {
        "name": "Makedoniya imperiyasi",
        "group": "Antik va Osiyo",
        "specialization": "Aleksandr taktikasi / Tezkor",
        "gold": 100_000_000,
        "capital": "Pella",
        "cities": ["Pella", "Bobil", "Aleksandriya"]
    },
    "karfagen": {
        "name": "Karfagen imperiyasi",
        "group": "Antik va Osiyo",
        "specialization": "Savdo / Dengiz floti",
        "gold": 100_000_000,
        "capital": "Karfagen",
        "cities": ["Karfagen", "Utika", "Gades"]
    },
    "yaponiya": {
        "name": "Tokugava shogunati (Yaponiya)",
        "group": "Antik va Osiyo",
        "specialization": "Samuraylar / Intizom",
        "gold": 100_000_000,
        "capital": "Edo",
        "cities": ["Edo", "Kioto", "Osaka"]
    },
    "turk_xoqonligi": {
        "name": "Buyuk Turk xoqonligi",
        "group": "Antik va Osiyo",
        "specialization": "Chegarasiz dasht / Ittifoq",
        "gold": 100_000_000,
        "capital": "Suyob",
        "cities": ["Suyob", "Otuken", "Beshbaliq"]
    }
}

PROVINCES = {
    "anadolu": {"name": "Anadolu yarimoroli", "cost": 10_000_000, "power_required": 30},
    "xuroson": {"name": "Xuroson hududi", "cost": 15_000_000, "power_required": 70},
    "mesopotamiya": {"name": "Mesopotamiya", "cost": 20_000_000, "power_required": 120},
    "sharqiy_yevropa": {"name": "Sharqiy Yevropa", "cost": 25_000_000, "power_required": 200},
    "hindiston": {"name": "Hindiston vodiysi", "cost": 30_000_000, "power_required": 300}
}

TROOPS = {
    "piyoda": {"name": "Piyoda askarlar", "cost": 1_000_000, "power": 10},
    "otliq": {"name": "Saralangan otliqlar", "cost": 3_000_000, "power": 35},
    "qamal": {"name": "Qamal qurollari", "cost": 7_000_000, "power": 90}
}

user_game_data = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("🕌 Sharq va Islom olami", callback_data="cat_Sharq va Islom olami"),
        types.InlineKeyboardButton("🌍 Yevropa va Jahon", callback_data="cat_Yevropa va Jahon"),
        types.InlineKeyboardButton("⚔️ Antik va Osiyo", callback_data="cat_Antik va Osiyo")
    )
    bot.reply_to(message, "Salom! Sivilizatsiya o'yiniga xush kelibsiz.\nQuyidagi kategoriyalardan birini tanlang:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    user_id = call.from_user.id
    
    if call.data.startswith("cat_"):
        cat_name = call.data.split("_", 1)[1]
        markup = types.InlineKeyboardMarkup(row_width=1)
        for key, val in EMPIRES.items():
            if val["group"] == cat_name:
                markup.add(types.InlineKeyboardButton(f"👑 {val['name']}", callback_data=f"select_{key}"))
        markup.add(types.InlineKeyboardButton("🔙 Kategoriyalarga qaytish", callback_data="back_to_cats"))
        
        bot.edit_message_text(
            chat_id=call.message.chat.id, message_id=call.message.message_id,
            text=f"📂 **{cat_name}** kategoriyasidagi imperiyalar:", reply_markup=markup, parse_mode="Markdown"
        )
        
    elif call.data == "back_to_cats":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🕌 Sharq va Islom olami", callback_data="cat_Sharq va Islom olami"),
            types.InlineKeyboardButton("🌍 Yevropa va Jahon", callback_data="cat_Yevropa va Jahon"),
            types.InlineKeyboardButton("⚔️ Antik va Osiyo", callback_data="cat_Antik va Osiyo")
        )
        bot.edit_message_text(
            chat_id=call.message.chat.id, message_id=call.message.message_id,
            text="Salom! Sivilizatsiya o'yiniga xush kelibsiz.\nQuyidagi kategoriyalardan birini tanlang:", reply_markup=markup, parse_mode="Markdown"
        )
        
    elif call.data.startswith("select_"):
        emp_key = call.data.split("_", 1)[1]
        emp = EMPIRES[emp_key]
        user_game_data[user_id] = {
            "empire": emp_key, "gold": emp["gold"], "conquered": [],
            "army": {"piyoda": 0, "otliq": 0, "qamal": 0}, "total_power": 0,
            "last_tax_time": 0
        }
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("📜 Profil", callback_data="profile"),
            types.InlineKeyboardButton("🗺 Xarita", callback_data="map"),
            types.InlineKeyboardButton("⚔️ Harbiy Qorgon", callback_data="army_menu"),
            types.InlineKeyboardButton("💰 Soliq yig'ish", callback_data="collect_tax")
        )
        bot.answer_callback_query(call.id, f"Tabriklayman! Siz {emp['name']}ni tanladingiz.")
        bot.edit_message_text(
            chat_id=call.message.chat.id, message_id=call.message.message_id,
            text=f"✅ **Sizning tanlovingiz:** {emp['name']}\n📂 **Guruh:** {emp['group']}\n\n🏛 **Poytaxt:** {emp['capital']}\n⚔️ **Ixtisoslashuv:** {emp['specialization']}\n💰 **Xazina:** {emp['gold']:,} oltin\n\nQuyidagi menyudan foydalaning:",
            reply_markup=markup, parse_mode="Markdown"
        )
        
    elif call.data == "profile":
        data = user_game_data.get(user_id)
        if not data:
            bot.answer_callback_query(call.id, "Siz hali imperiya tanlamagansiz! /start ni bosing.", show_alert=True)
            return
        emp = EMPIRES[data["empire"]]
        conquered_str = ", ".join([PROVINCES[p]["name"] for p in data["conquered"]]) if data["conquered"] else "Hozircha yo'q"
        bot.answer_callback_query(call.id)
        bot.send_message(
            call.message.chat.id,
            f"📜 **Sizning Imperiyangiz Profili:**\n\n👑 Nomi: {emp['name']}\n📂 Guruh: {emp['group']}\n🏛 Poytaxt: {emp['capital']}\n🏙 Shaharlar: {', '.join(emp['cities'])}\n⚔️ Zabt etilgan hududlar: {conquered_str}\n🛡 Umumiy harbiy quvvat: {data['total_power']} kuch\n💰 Xazina: {data['gold']:,} oltin",
            parse_mode="Markdown"
        )
        
    elif call.data == "map":
        data = user_game_data.get(user_id)
        if not data:
            bot.answer_callback_query(call.id, "Siz hali imperiya tanlamagansiz! /start ni bosing.", show_alert=True)
            return
        markup = types.InlineKeyboardMarkup(row_width=1)
        for p_key, p_val in PROVINCES.items():
            if p_key not in data["conquered"]:
                btn_text = f"⚔️ {p_val['name']} ({p_val['cost']:,} oltin)"
                markup.add(types.InlineKeyboardButton(btn_text, callback_data=f"conquer_{p_key}"))
        markup.add(types.InlineKeyboardButton("🔙 Asosiy menyu", callback_data="back_to_menu"))
        bot.answer_callback_query(call.id)
        bot.edit_message_text(
            chat_id=call.message.chat.id, message_id=call.message.message_id,
            text=f"🗺 **Global Xarita va Jang maydoni:**\n\n💰 Xazinangiz: **{data['gold']:,} oltin**\n🛡 Armiyangiz kuchi: **{data['total_power']} kuch**\n\nHududni zabt etish uchun yetarli kuch va oltin kerak:",
            reply_markup=markup, parse_mode="Markdown"
        )
        
    elif call.data == "army_menu":
        data = user_game_data.get(user_id)
        if not data:
            bot.answer_callback_query(call.id, "Siz hali imperiya tanlamagansiz!", show_alert=True)
            return
        markup = types.InlineKeyboardMarkup(row_width=1)
        for t_key, t_val in TROOPS.items():
            btn_text = f"➕ Yollash: {t_val['name']} ({t_val['cost']:,} oltin)"
            markup.add(types.InlineKeyboardButton(btn_text, callback_data=f"recruit_{t_key}"))
        markup.add(types.InlineKeyboardButton("🔙 Asosiy menyu", callback_data="back_to_menu"))
        bot.answer_callback_query(call.id)
        bot.edit_message_text(
            chat_id=call.message.chat.id, message_id=call.message.message_id,
            text=f"⚔️ **Harbiy Qorgon (Qo'shin yollash):**\n\n💂‍♂️ Piyodalar: {data['army']['piyoda']} ta\n🐎 Otliqlar: {data['army']['otliq']} ta\n💣 Qamal qurollari: {data['army']['qamal']} ta\n🛡 Jami quvvat: {data['total_power']} kuch\n💰 Xazina: {data['gold']:,} oltin\n\nQo'shin turini tanlang:",
            reply_markup=markup, parse_mode="Markdown"
        )
        
    elif call.data == "collect_tax":
        data = user_game_data.get(user_id)
        if not data:
            bot.answer_callback_query(call.id, "Siz hali imperiya tanlamagansiz!", show_alert=True)
            return
        
        current_time = time.time()
        if current_time - data.get("last_tax_time", 0) < 60:
            remaining = int(60 - (current_time - data["last_tax_time"]))
            bot.answer_callback_query(call.id, f"Soliqni yana {remaining} sekunddan keyin yig'ishingiz mumkin!", show_alert=True)
            return
        
        tax_amount = 5_000_000 + (len(data["conquered"]) * 2_000_000)
        data["gold"] += tax_amount
        data["last_tax_time"] = current_time
        
        bot.answer_callback_query(call.id, f"Muvaffaqiyatli! Xazinaga +{tax_amount:,} oltin qo'shildi!")
        
        emp = EMPIRES[data["empire"]]
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("📜 Profil", callback_data="profile"),
            types.InlineKeyboardButton("🗺 Xarita", callback_data="map"),
            types.InlineKeyboardButton("⚔️ Harbiy Qorgon", callback_data="army_menu"),
            types.InlineKeyboardButton("💰 Soliq yig'ish", callback_data="collect_tax")
        )
        bot.edit_message_text(
            chat_id=call.message.chat.id, message_id=call.message.message_id,
            text=f"✅ **Sizning imperiyangiz:** {emp['name']}\n🏛 **Poytaxt:** {emp['capital']}\n💰 **Xazina:** {data['gold']:,} oltin (+{tax_amount:,} soliq olindi)\n🛡 **Armiya kuchi:** {data['total_power']} kuch\n\nQuyidagi menyudan foydalaning:",
            reply_markup=markup, parse_mode="Markdown"
        )
        
    elif call.data.startswith("recruit_"):
        t_key = call.data.split("_", 1)[1]
        data = user_game_data.get(user_id)
        if not data:
            bot.answer_callback_query(call.id, "Siz hali imperiya tanlamagansiz!", show_alert=True)
            return
        troop = TROOPS[t_key]
        if data["gold"] >= troop["cost"]:
            data["gold"] -= troop["cost"]
            data["army"][t_key] += 1
            data["total_power"] += troop["power"]
            bot.answer_callback_query(call.id, f"Muvaffaqiyatli yollandi: {troop['name']}!")
        else:
            bot.answer_callback_query(call.id, "Xazinangizda yetarli oltin yo'q!", show_alert=True)
            return
        markup = types.InlineKeyboardMarkup(row_width=1)
        for tk, tv in TROOPS.items():
            btn_text = f"➕ Yollash: {tv['name']} ({tv['cost']:,} oltin)"
            markup.add(types.InlineKeyboardButton(btn_text, callback_data=f"recruit_{tk}"))
        markup.add(types.InlineKeyboardButton("🔙 Asosiy menyu", callback_data="back_to_menu"))
        bot.edit_message_text(
            chat_id=call.message.chat.id, message_id=call.message.message_id,
            text=f"⚔️ **Harbiy Qorgon (Qo'shin yollash):**\n\n💂‍♂️ Piyodalar: {data['army']['piyoda']} ta\n🐎 Otliqlar: {data['army']['otliq']} ta\n💣 Qamal qurollari: {data['army']['qamal']} ta\n🛡 Jami quvvat: {data['total_power']} kuch\n💰 Xazina: {data['gold']:,} oltin\n\nQo'shin turini tanlang:",
            reply_markup=markup, parse_mode="Markdown"
        )
        
    elif call.data.startswith("conquer_"):
        p_key = call.data.split("_", 1)[1]
        data = user_game_data.get(user_id)
        if not data:
            bot.answer_callback_query(call.id, "Siz hali imperiya tanlamagansiz!", show_alert=True)
            return
        province = PROVINCES[p_key]
        if data["gold"] < province["cost"]:
            bot.answer_callback_query(call.id, "Xazinangizda yetarli oltin yo'q!", show_alert=True)
            return
        if data["total_power"] < province["power_required"]:
            bot.answer_callback_query(call.id, f"Armiyangiz kuchi yetmadi! Kerakli kuch: {province['power_required']}", show_alert=True)
            return
        data["gold"] -= province["cost"]
        data["conquered"].append(p_key)
        bot.answer_callback_query(call.id, f"G'alaba! {province['name']} muvaffaqiyatli zabt etildi!")
        markup = types.InlineKeyboardMarkup(row_width=1)
        for pk, pv in PROVINCES.items():
            if pk not in data["conquered"]:
                btn_text = f"⚔️ {pv['name']} ({pv['cost']:,} oltin)"
                markup.add(types.InlineKeyboardButton(btn_text, callback_data=f"conquer_{pk}"))
        markup.add(types.InlineKeyboardButton("🔙 Asosiy menyu", callback_data="back_to_menu"))
        bot.edit_message_text(
            chat_id=call.message.chat.id, message_id=call.message.message_id,
            text=f"🗺 **Global Xarita va Jang maydoni:**\n\n🎉 **Oxirgi g'alaba:** {province['name']} zabt etildi!\n💰 Qolgan xazina: **{data['gold']:,} oltin**\n🛡 Armiya kuchi: **{data['total_power']} kuch**\n\nBoshqa hududlarni ham tanlashingiz mumkin:",
            reply_markup=markup, parse_mode="Markdown"
        )
        
    elif call.data == "back_to_menu":
        data = user_game_data.get(user_id)
        if not data:
            return
        emp = EMPIRES[data["empire"]]
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("📜 Profil", callback_data="profile"),
            types.InlineKeyboardButton("🗺 Xarita", callback_data="map"),
            types.InlineKeyboardButton("⚔️ Harbiy Qorgon", callback_data="army_menu"),
            types.InlineKeyboardButton("💰 Soliq yig'ish", callback_data="collect_tax")
        )
        bot.edit_message_text(
            chat_id=call.message.chat.id, message_id=call.message.message_id,
            text=f"✅ **Sizning imperiyangiz:** {emp['name']}\n🏛 **Poytaxt:** {emp['capital']}\n💰 **Xazina:** {data['gold']:,} oltin\n🛡 **Armiya kuchi:** {data['total_power']} kuch\n\nQuyidagi menyudan foydalaning:",
            reply_markup=markup, parse_mode="Markdown"
        )

if __name__ == '__main__':
    print("Bot ishga tushdi...")
    while True:
        try:
            bot.remove_webhook()
            bot.infinity_polling(skip_pending=True, timeout=60, long_polling_timeout=60)
        except Exception as e:
            print(f"Xatolik yuz berdi: {e}")
            time.sleep(5)
