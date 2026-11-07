import os
import time
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import telebot
from telebot import types

TOKEN = "9163206553:AAEjs1mCITIow9KnvmTjGzr6f0wNdHmlRvQ"
bot = telebot.TeleBot(TOKEN)

START_GOLD = 100_000_000
EAST, EUROPE, ANTIK = "Sharq", "Yevropa", "Antik"

def m(name, desc, type_, val):
    return {"name": name, "desc": desc, "type": type_, "val": val}

def e(name, group, cap, monarchs):
    return {"name": name, "group": group, "gold": START_GOLD, "capital": cap, "monarchs": monarchs}

EMPIRES = {
    "temuriylar": e("Temuriylar imperiyasi", EAST, "Samarqand", {
        "timur": m("Amir Timur", "Harbiy quvvat +25%", "power", 1.25),
        "ulugbek": m("Mirzo Ulug'bek", "Qo'shin narxi -15%", "cost", 0.85)
    }),
    "omaviylar": e("Omaviylar xalifaligi", EAST, "Damashq", {
        "muoviya": m("Muoviya I", "Diplomatiya -10%", "cost", 0.90),
        "abdulmalik": m("Abdulmalik", "Soliqlar +30%", "tax", 1.30)
    }),
    "abbosiylar": e("Abbosiylar xalifaligi", EAST, "Bagdod", {
        "horun": m("Horun ar-Rashid", "Xazina +30%", "gold", 1.30),
        "mamun": m("Al-Ma'mun", "Qo'shin narxi -10%", "cost", 0.90)
    }),
    "usmonlilar": e("Usmonlilar imperiyasi", EAST, "Istanbul", {
        "mehmed": m("Fotih Mehmed", "Qamal +30%", "power", 1.30),
        "sulaymon": m("Sulaymon Qonuniy", "Zabt narxi -20%", "cost", 0.80)
    }),
    "xorazmshohlar": e("Xorazmshohlar davlati", EAST, "Urganch", {
        "muhammad": m("Muhammad II", "Armiya +20%", "power", 1.20),
        "jaloliddin": m("Jaloliddin Manguberdi", "Qahramonlik +35%", "power", 1.35)
    }),
    "buxoro_amirligi": e("Buxoro amirligi", EAST, "Buxoro", {
        "shohmurod": m("Shohmurod", "Soliq +30%", "tax", 1.30),
        "olimxon": m("Said Olimxon", "Mudofaa +25%", "power", 1.25)
    }),
    "xiva_xonligi": e("Xiva xonligi", EAST, "Xiva", {
        "rahimxon2": m("Muhammad Rahimxon II", "Soliq +35%", "tax", 1.35),
        "junaid": m("Junaidxon", "Shijoat +30%", "power", 1.30)
    }),
    "qoqon_xonligi": e("Qo'qon xonligi", EAST, "Qo'qon", {
        "olimxon_q": m("Olimxon", "Armiya +30%", "power", 1.30),
        "madalixon": m("Madalixon", "Savdo +35%", "tax", 1.35)
    }),
    "britaniya": e("Britaniya imperiyasi", EUROPE, "London", {
        "viktoriya": m("Viktoriya", "Soliq +35%", "tax", 1.35),
        "cherchill": m("Uinston Cherchill", "Qat'iyat +25%", "power", 1.25)
    }),
    "rim": e("Rim imperiyasi", EUROPE, "Rim", {
        "sezar": m("Yuliy Sezar", "Legionlar +30%", "power", 1.30),
        "trayan": m("Trayan", "Zabt narxi -20%", "cost", 0.80)
    }),
    "fransiya": e("Fransiya imperiyasi", EUROPE, "Parij", {
        "lyudovik": m("Lyudovik XIV", "Soliq +35%", "tax", 1.35),
        "napoleon": m("Napoleon", "Strategiya +40%", "power", 1.40)
    }),
    "rossiya": e("Rossiya imperiyasi", EUROPE, "Sankt-Peterburg", {
        "pyotr": m("Buyuk Pyotr", "Sanoat +30%", "gold", 1.30),
        "yekaterina": m("Yekaterina II", "Kengaytirish -35%", "cost", 0.65)
    }),
    "sssr": e("SSSR", EUROPE, "Moskva", {
        "stalin": m("Iosif Stalin", "Qizil armiya +40%", "power", 1.40),
        "lenin": m("Vladimir Lenin", "Resurslar +25%", "gold", 1.25)
    }),
    "mongol": e("Mo'g'ullar imperiyasi", ANTIK, "Qoraqurum", {
        "chingiz": m("Chingizxon", "Tezkor yurish +45%", "power", 1.45),
        "qubilay": m("Qubilay xon", "Savdo +35%", "gold", 1.35)
    }),
    "qadimgi_xitoy": e("Sin imperiyasi", ANTIK, "Sian", {
        "sinshi": m("Sin Shi Huang", "Soliq +40%", "tax", 1.40),
        "xanvudi": m("Xan Vu-di", "Ipak yo'li +30%", "gold", 1.30)
    }),
    "makedoniya": e("Makedoniya imperiyasi", ANTIK, "Pella", {
        "aleksandr": m("Aleksandr Makedoniyali", "Saltanat +50%", "power", 1.50),
        "filipp2": m("Filipp II", "Falanga +25%", "power", 1.25)
    })
}

PROVINCES = {
    "anadolu": {"name": "Anadolu", "cost": 10_000_000, "power_required": 30},
    "xuroson": {"name": "Xuroson", "cost": 15_000_000, "power_required": 70},
    "mesopotamiya": {"name": "Mesopotamiya", "cost": 20_000_000, "power_required": 120},
    "sharqiy_yevropa": {"name": "Sharqiy Yevropa", "cost": 25_000_000, "power_required": 200},
    "hindiston": {"name": "Hindiston", "cost": 30_000_000, "power_required": 300}
}

TROOPS = {
    "piyoda": {"name": "Piyodalar", "cost": 1_000_000, "power": 10},
    "otliq": {"name": "Otliqlar", "cost": 3_000_000, "power": 35},
    "qamal": {"name": "Qamal qurollari", "cost": 7_000_000, "power": 90}
}

user_game_data = {}

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot ishlamoqda!")

def run_server():
    server = ThreadingHTTPServer(("0.0.0.0", int(os.environ.get("PORT", 10000))), HealthHandler)
    server.serve_forever()

@bot.message_handler(commands=["start"])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("🕌 Sharq", callback_data="cat_Sharq"),
        types.InlineKeyboardButton("🌍 Yevropa", callback_data="cat_Yevropa"),
        types.InlineKeyboardButton("⚔️ Antik", callback_data="cat_Antik")
    )
    bot.reply_to(message, "Sivilizatsiya o'yiniga xush kelibsiz! Kategoriyani tanlang:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    user_id = call.from_user.id

    if call.data.startswith("cat_"):
        cat_name = call.data.split("_", 1)[1]
        markup = types.InlineKeyboardMarkup(row_width=1)
        for key, val in EMPIRES.items():
            if val["group"] == cat_name:
                markup.add(types.InlineKeyboardButton(f"👑 {val['name']}", callback_data=f"select_{key}"))
        markup.add(types.InlineKeyboardButton("🔙 Orqaga", callback_data="back_to_cats"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"📂 **{cat_name}** imperiyalari:", reply_markup=markup, parse_mode="Markdown")

    elif call.data == "back_to_cats":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🕌 Sharq", callback_data="cat_Sharq"),
            types.InlineKeyboardButton("🌍 Yevropa", callback_data="cat_Yevropa"),
            types.InlineKeyboardButton("⚔️ Antik", callback_data="cat_Antik")
        )
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Kategoriyani tanlang:", reply_markup=markup)

    elif call.data.startswith("select_"):
        emp_key = call.data.split("_", 1)[1]
        emp = EMPIRES[emp_key]
        markup = types.InlineKeyboardMarkup(row_width=1)
        for m_key, m_val in emp["monarchs"].items():
            markup.add(types.InlineKeyboardButton(f"👑 {m_val['name']} ({m_val['desc']})", callback_data=f"monarch_{emp_key}_{m_key}"))
        markup.add(types.InlineKeyboardButton("🔙 Orqaga", callback_data=f"cat_{emp['group']}"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"✅ **{emp['name']}** uchun Hukmdorni tanlang:", reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("monarch_"):
        _, emp_key, monarch_key = call.data.split("_", 2)
        emp = EMPIRES[emp_key]
        monarch = emp["monarchs"][monarch_key]
        initial_gold = int(emp["gold"] * monarch["val"]) if monarch["type"] == "gold" else emp["gold"]

        user_game_data[user_id] = {
            "empire": emp_key, "monarch": monarch_key, "player_name": call.from_user.first_name,
            "gold": initial_gold, "conquered": [], "army": {"piyoda": 0, "otliq": 0, "qamal": 0},
            "total_power": 0, "last_tax_time": 0
        }

        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("📜 Profil", callback_data="profile"),
            types.InlineKeyboardButton("🗺 Xarita", callback_data="map"),
            types.InlineKeyboardButton("⚔️ Qorgon", callback_data="army_menu"),
            types.InlineKeyboardButton("💰 Soliq", callback_data="collect_tax"),
            types.InlineKeyboardButton("🏆 Reyting", callback_data="leaderboard")
        )
        bot.answer_callback_query(call.id, f"Hukmdor {monarch['name']} tanlandi!")
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"👑 **{emp['name']}**\nHukmdor: {monarch['name']}\n💰 Xazina: {initial_gold:,} oltin", reply_markup=markup, parse_mode="Markdown")

    elif call.data == "profile":
        data = user_game_data.get(user_id)
        if not data: return
        emp = EMPIRES[data["empire"]]
        monarch = emp["monarchs"][data["monarch"]]
        conq = ", ".join([PROVINCES[p]["name"] for p in data["conquered"]]) if data["conquered"] else "Yo'q"
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, f"📜 **Profil:**\n👑 Imperiya: {emp['name']}\n👑 Hukmdor: {monarch['name']}\n⚔️ Zabt etilgan: {conq}\n🛡 Kuch: {data['total_power']}\n💰 Xazina: {data['gold']:,} oltin", parse_mode="Markdown")

    elif call.data == "map":
        data = user_game_data.get(user_id)
        if not data: return
        emp = EMPIRES[data["empire"]]
        monarch = emp["monarchs"][data["monarch"]]
        markup = types.InlineKeyboardMarkup(row_width=1)
        for p_key, p_val in PROVINCES.items():
            if p_key not in data["conquered"]:
                cost = int(p_val["cost"] * (monarch["val"] if monarch["type"] == "cost" else 1.0))
                markup.add(types.InlineKeyboardButton(f"⚔️ {p_val['name']} ({cost:,} oltin | {p_val['power_required']} kuch)", callback_data=f"conquer_{p_key}"))
        markup.add(types.InlineKeyboardButton("🔙 Menyu", callback_data="back_to_menu"))
        bot.answer_callback_query(call.id)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"🗺 **Xarita:**\n💰 Xazina: {data['gold']:,}\n🛡 Kuch: {data['total_power']}", reply_markup=markup, parse_mode="Markdown")

    elif call.data == "army_menu":
        data = user_game_data.get(user_id)
        if not data: return
        emp = EMPIRES[data["empire"]]
        monarch = emp["monarchs"][data["monarch"]]
        markup = types.InlineKeyboardMarkup(row_width=1)
        for t_key, t_val in TROOPS.items():
            cost = int(t_val["cost"] * (monarch["val"] if monarch["type"] == "cost" else 1.0))
            markup.add(types.InlineKeyboardButton(f"➕ {t_val['name']} ({cost:,} oltin)", callback_data=f"recruit_{t_key}"))
        markup.add(types.InlineKeyboardButton("🔙 Menyu", callback_data="back_to_menu"))
        bot.answer_callback_query(call.id)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"⚔️ **Harbiy Qorgon:**\n💂‍♂️ Piyoda: {data['army']['piyoda']}\n🐎 Otliq: {data['army']['otliq']}\n💣 Qamal: {data['army']['qamal']}\n🛡 Kuch: {data['total_power']}\n💰 Xazina: {data['gold']:,}", reply_markup=markup, parse_mode="Markdown")

    elif call.data == "collect_tax":
        data = user_game_data.get(user_id)
        if not data: return
        curr = time.time()
        if curr - data.get("last_tax_time", 0) < 60:
            bot.answer_callback_query(call.id, f"Kuting: {int(60 - (curr - data['last_tax_time']))} sek", show_alert=True)
            return
        emp = EMPIRES[data["empire"]]
        monarch = emp["monarchs"][data["monarch"]]
        tax = 5_000_000 + (len(data["conquered"]) * 2_000_000)
        if monarch["type"] == "tax": tax = int(tax * monarch["val"])
        data["gold"] += tax
        data["last_tax_time"] = curr
        bot.answer_callback_query(call.id, f"+{tax:,} oltin olindi!")
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("📜 Profil", callback_data="profile"),
            types.InlineKeyboardButton("🗺 Xarita", callback_data="map"),
            types.InlineKeyboardButton("⚔️ Qorgon", callback_data="army_menu"),
            types.InlineKeyboardButton("💰 Soliq", callback_data="collect_tax"),
            types.InlineKeyboardButton("🏆 Reyting", callback_data="leaderboard")
        )
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"✅ **{emp['name']}**\n💰 Xazina: {data['gold']:,} oltin", reply_markup=markup, parse_mode="Markdown")

    elif call.data == "leaderboard":
        sorted_p = sorted(user_game_data.items(), key=lambda x: x[1].get("total_power", 0), reverse=True)
        txt = "🏆 **Top 10 Reyting:**\n\n"
        for i, (u, p) in enumerate(sorted_p[:10], 1):
            txt += f"{i}. **{p.get('player_name')}** | 🛡 {p['total_power']} kuch\n"
        markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔙 Menyu", callback_data="back_to_menu"))
        bot.answer_callback_query(call.id)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=txt, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("recruit_"):
        t_key = call.data.split("_", 1)[1]
        data = user_game_data.get(user_id)
        if not data: return
        monarch = EMPIRES[data["empire"]]["monarchs"][data["monarch"]]
        t_val = TROOPS[t_key]
        cost = int(t_val["cost"] * (monarch["val"] if monarch["type"] == "cost" else 1.0))
        pwr = int(t_val["power"] * (monarch["val"] if monarch["type"] == "power" else 1.0))

        if data["gold"] >= cost:
            data["gold"] -= cost
            data["army"][t_key] += 1
            data["total_power"] += pwr
            bot.answer_callback_query(call.id, f"+1 {t_val['name']} yollandi!")
        else:
            bot.
