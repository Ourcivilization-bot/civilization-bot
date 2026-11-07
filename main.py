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
        "shohrux": m("Shohrux Mirzo", "Soliq +20%", "tax", 1.20),
        "ulugbek": m("Mirzo Ulug'bek", "Qo'shin narxi -15%", "cost", 0.85),
        "husayn": m("Husayn Boyqaro", "Xazina +20%", "gold", 1.20)
    }),
    "omaviylar": e("Omaviylar xalifaligi", EAST, "Damashq", {
        "muoviya": m("Muoviya I", "Diplomatiya -10%", "cost", 0.90),
        "abdulmalik": m("Abdulmalik", "Soliqlar +30%", "tax", 1.30),
        "valid": m("Valid I", "Zabt kuchi -10%", "power", 1.10),
        "umar2": m("Umar II", "Adolat va xazina", "gold", 1.20)
    }),
    "abbosiylar": e("Abbosiylar xalifaligi", EAST, "Bagdod", {
        "horun": m("Horun ar-Rashid", "Xazina +30%", "gold", 1.30),
        "mamun": m("Al-Ma'mun", "Qo'shin narxi -10%", "cost", 0.90),
        "mansur": m("Al-Mansur", "Soliq +20%", "tax", 1.20),
        "mutasim": m("Al-Mu'tasim", "Armiya +15%", "power", 1.15)
    }),
    "usmonlilar": e("Usmonlilar imperiyasi", EAST, "Istanbul", {
        "osman": m("Osman I", "Asoschilik", "gold", 1.15),
        "mehmed": m("Fotih Mehmed", "Qamal +30%", "power", 1.30),
        "sulaymon": m("Sulaymon Qonuniy", "Zabt narxi -20%", "cost", 0.80),
        "boyazid": m("Yildirim Boyazid", "Hujum +25%", "power", 1.25)
    }),
    "ayyubiylar": e("Ayyubiylar sulolasi", EAST, "Qohira", {
        "salohiddin": m("Salohiddin Ayyubi", "Harbiy quvvat +25%", "power", 1.25),
        "adil": m("Al-Adil", "Soliq +20%", "tax", 1.20),
        "komil": m("Al-Komil", "Hudud narxi -15%", "cost", 0.85),
        "nosir": m("An-Nosir Yusuf", "Otliqlar +20%", "power", 1.20)
    }),
    "xorazmshohlar": e("Xorazmshohlar davlati", EAST, "Urganch", {
        "anushtegin": m("Anushtegin", "Soliq +10%", "tax", 1.10),
        "otsiz": m("Otsiz", "Hudud narxi -15%", "cost", 0.85),
        "muhammad": m("Muhammad II", "Armiya +20%", "power", 1.20),
        "jaloliddin": m("Jaloliddin Manguberdi", "Qahramonlik +35%", "power", 1.35)
    }),
    "gaznaviylar": e("Gaznaviylar davlati", EAST, "Gazna", {
        "sabuqtigin": m("Sabuqtigin", "Xazina +15%", "gold", 1.15),
        "mahmud": m("Mahmud G'aznaviy", "Oltin +30%", "tax", 1.30),
        "masud": m("Mas'ud I", "Otliqlar +20%", "power", 1.20),
        "ibrohim": m("Ibrohim", "Barqarorlik", "tax", 1.15)
    }),
    "safaviylar": e("Safaviylar imperiyasi", EAST, "Isfahon", {
        "ismoil": m("Shoh Ismoil I", "Shijoat +25%", "power", 1.25),
        "abbos": m("Shoh Abbos", "Savdo va soliq +30%", "tax", 1.30),
        "tahmosib": m("Tahmasp I", "Himoya", "power", 1.15),
        "husayn_s": m("Sulton Husayn", "Madaniyat", "gold", 1.20)
    }),
    "boburiylar": e("Boburiylar imperiyasi", EAST, "Dehli", {
        "bobur": m("Zahriddin Bobur", "Taktika +25%", "power", 1.25),
        "akbar": m("Akbarshoh", "Soliq +30%", "tax", 1.30),
        "jahon": m("Shoh Jahon", "Xazina +25%", "gold", 1.25),
        "avrangzeb": m("Avrangzeb", "Hudud narxi -20%", "cost", 0.80)
    }),
    "oltin_orda": e("Oltin Orda", EAST, "Saroy-Bot", {
        "botu": m("Botuxon", "Soliq yig'ish +35%", "tax", 1.35),
        "beraka": m("Berakaxon", "Savdo +20%", "gold", 1.20),
        "uzbek": m("O'zbekxon", "Barqarorlik", "tax", 1.20),
        "toxtamish": m("To'xtamishxon", "Tezkor hujum", "power", 1.20)
    }),
    "shayboniylar": e("Shayboniylar sulolasi", EAST, "Samarqand", {
        "abulxayr": m("Abulxayrxon", "Dasht qudrati", "power", 1.25),
        "shayboniy": m("Muhammad Shayboniy", "Birlashish +35%", "power", 1.35),
        "ubaydulla": m("Ubaydullaxon", "Soliq +30%", "tax", 1.30),
        "abdulla2": m("Abdullaxon II", "Kengaytirish -20%", "cost", 0.80)
    }),
    "buxoro_amirligi": e("Buxoro amirligi", EAST, "Buxoro", {
        "rahimxon_b": m("Muhammad Rahimxon", "Amirlik asosi", "power", 1.25),
        "shohmurod": m("Shohmurod", "Soliq +30%", "tax", 1.30),
        "haydar": m("Amir Haydar", "Ilm-fan", "gold", 1.20),
        "olimxon": m("Said Olimxon", "Mudofaa +25%", "power", 1.25)
    }),
    "xiva_xonligi": e("Xiva xonligi", EAST, "Xiva", {
        "olloquli": m("Olloqulixon", "Ichan qal'a", "gold", 1.30),
        "rahimxon2": m("Muhammad Rahimxon II", "Soliq +35%", "tax", 1.35),
        "isfandiyor": m("Isfandiyorxon", "Islohotlar", "tax", 1.20),
        "junaid": m("Junaidxon", "Shijoat +30%", "power", 1.30)
    }),
    "qoqon_xonligi": e("Qo'qon xonligi", EAST, "Qo'qon", {
        "norbotabiy": m("Norbo'tabiy", "Xazina", "gold", 1.25),
        "olimxon_q": m("Olimxon", "Armiya +30%", "power", 1.30),
        "madalixon": m("Madalixon", "Savdo +35%", "tax", 1.35),
        "xudoyorxon": m("Xudoyorxon", "Saroy", "gold", 1.25)
    }),
    "salibchilar": e("Salibchilar", EAST, "Quddus", {
        "gotfrid": m("Gotfrid", "Asoschilik", "power", 1.25),
        "baldvin4": m("Baldvin IV", "Mudofaa +30%", "power", 1.30),
        "richard": m("Richard Sheryurak", "Quvvat +40%", "power", 1.40),
        "reno": m("Reno", "Shijoat", "tax", 1.20)
    }),
    "saljuqiylar": e("Saljuqiylar imperiyasi", EAST, "Isfahon", {
        "togʻrulbek": m("Togʻrulbek", "Asoschilik va shijoat", "power", 1.25),
        "alp_arslon": m("Alp Arslon", "Harbiy quvvat +40%", "power", 1.40),
        "malikshoh": m("Malikshoh I", "Oltin davr va soliq", "tax", 1.35),
        "sultan_sanjar": m("Sulton Sanjar", "Kengayish va barqarorlik", "gold", 1.30)
    }),
    "britaniya": e("Britaniya imperiyasi", EUROPE, "London", {
        "elizaveta": m("Yelizaveta I", "Flot va savdo", "gold", 1.30),
        "viktoriya": m("Viktoriya", "Soliq +35%", "tax", 1.35),
        "cherchill": m("Uinston Cherchill", "Qat'iyat +25%", "power", 1.25),
        "genrix8": m("Genrix VIII", "Siyosat", "cost", 0.90)
    }),
    "rim": e("Rim imperiyasi", EUROPE, "Rim", {
        "sezar": m("Yuliy Sezar", "Legionlar +30%", "power", 1.30),
        "august": m("August", "Infratuzilma", "tax", 1.25),
        "trayan": m("Trayan", "Zabt narxi -20%", "cost", 0.80),
        "konstantin_r": m("Konstantin", "Barqarorlik", "gold", 1.20)
    }),
    "fransiya": e("Fransiya imperiyasi", EUROPE, "Parij", {
        "karl_buyuk": m("Karl Buyuk", "Qudrat", "power", 1.25),
        "lyudovik": m("Lyudovik XIV", "Soliq +35%", "tax", 1.35),
        "napoleon": m("Napoleon", "Strategiya +40%", "power", 1.40),
        "jovanni": m("Janna d'Ark", "Ruh", "power", 1.20)
    }),
    "rossiya": e("Rossiya imperiyasi", EUROPE, "Sankt-Peterburg", {
        "pyotr": m("Buyuk Pyotr", "Sanoat +30%", "gold", 1.30),
        "yekaterina": m("Yekaterina II", "Kengaytirish -35%", "cost", 0.65),
        "ivan": m("Ivan Grozniy", "Tazyiq", "power", 1.25),
        "alex2": m("Aleksandr II", "O'sish", "tax", 1.20)
    }),
    "ispan": e("Ispaniya imperiyasi", EUROPE, "Madrid", {
        "izabella": m("Izabella", "Ekspeditsiya", "gold", 1.30),
        "karl5": m("Karl V", "Soliq", "tax", 1.25),
        "filipp2": m("Filipp II", "Flot", "power", 1.25),
        "elcid": m("El Cid", "Jangovar ruh", "power", 1.20)
    }),
    "natsist_germaniya": e("Natsistlar Germaniyasi", EUROPE, "Berlin", {
        "gitler": m("Adolf Gitler", "Blitskrig +40%", "power", 1.40),
        "gebbels": m("Jozef Gebbels", "Targ'ibot", "gold", 1.25),
        "goring": m("Herman Goring", "Arzon qo'shin", "cost", 0.80),
        "gimmler": m("Genrix Gimmler", "Tartib", "tax", 1.30)
    }),
    "aqsh": e("AQSh", EUROPE, "Vashington", {
        "washington": m("Jorj Vashington", "Ozodlik va quvvat", "power", 1.30),
        "lincoln": m("Avraam Linkoln", "Birlik va barqarorlik", "tax", 1.30),
        "roosevelt": m("Teodor Ruzvelt", "Iqtisodiy qudrat", "gold", 1.35),
        "kennedy": m("Jon Kennedi", "Innovatsiya va ta'sir", "cost", 0.80)
    }),
    "sssr": e("SSSR", EUROPE, "Moskva", {
        "lenin": m("Vladimir Lenin", "Resurslar +25%", "gold", 1.25),
        "stalin": m("Iosif Stalin", "Qizil armiya +40%", "power", 1.40),
        "xrushov": m("Nikita Xrushov", "Sanoat", "tax", 1.30),
        "brejnev": m("Leonid Brejnev", "Arzon qo'shin", "cost", 0.85)
    }),
    "vizantiya": e("Vizantiya imperiyasi", EUROPE, "Konstantinopol", {
        "yustinian": m("Yustinian I", "Qonunlar", "tax", 1.30),
        "konstantin_v": m("Konstantin", "Poytaxt", "gold", 1.25),
        "vasiliy": m("Vasiliy II", "Quvvat", "power", 1.30),
        "irakliy": m("Irakliy", "Xavfsizlik", "power", 1.15)
    }),
    "gon_sivar": e("Muqaddas Rim", EUROPE, "Aaxen", {
        "otton": m("Otton I", "Qudrat", "power", 1.25),
        "barbarossa": m("Fridrix Barbarossa", "Hudud narxi", "cost", 0.80),
        "charlz5": m("Charlz V", "Soliq", "tax", 1.30),
        "genrix4": m("Genrix IV", "Barqarorlik", "gold", 1.20)
    }),
    "mongol": e("Mo'g'ullar imperiyasi", ANTIK, "Qoraqurum", {
        "chingiz": m("Chingizxon", "Tezkor yurish +45%", "power", 1.45),
        "oqotay": m("O'qotay xon", "Boshqaruv", "tax", 1.30),
        "qubilay": m("Qubilay xon", "Savdo +35%", "gold", 1.35),
        "huloku": m("Hulokuxon", "Bosqinchilik", "power", 1.35)
    }),
    "xunnu": e("Buyuk Xunnu", ANTIK, "Utuken", {
        "modun": m("Modun Chanyu", "Otliqlar +35%", "power", 1.35),
        "laoshang": m("Lao-shang", "Kengayish", "cost", 0.85),
        "gunlu": m("Gunlu", "Quvvat", "power", 1.20),
        "hohanxie": m("Ho-han-xie", "Barqarorlik", "tax", 1.15)
    }),
    "qadimgi_xitoy": e("Sin imperiyasi", ANTIK, "Sian", {
        "sinshi": m("Sin Shi Huang", "Soliq +40%", "tax", 1.40),
        "xanvudi": m("Xan Vu-di", "Ipak yo'li +30%", "gold", 1.30),
        "taytsun": m("Taytsun", "Oltin davr", "tax", 1.35),
        "suyvendi": m("Suy Vendi", "Birlik", "cost", 0.85)
    }),
    "fors_ahamoniylar": e("Ahamoniylar", ANTIK, "Persepol", {
        "kir2": m("Kir II", "Bagrikenglik", "tax", 1.30),
        "doro1": m("Doro I", "Logistika", "cost", 0.80),
        "kserks": m("Kserks I", "Armiya quvvati", "power", 1.25),
        "artakserks": m("Artakserks I", "Barqarorlik", "gold", 1.20)
    }),
    "qadimgi_misr": e("Qadimgi Misr", ANTIK, "Memfis", {
        "ramses": m("Ramses II", "Obidalar", "power", 1.30),
        "tutmos": m("Tutmos III", "Kengayish", "cost", 0.75),
        "kleopatra": m("Kleopatra", "Xazina", "gold", 1.30),
        "exnaton": m("Exnaton", "Madaniyat", "tax", 1.20)
    }),
    "makedoniya": e("Makedoniya imperiyasi", ANTIK, "Pella", {
        "filipp2_m": m("Filipp II", "Falanga", "power", 1.25),
        "aleksandr": m("Aleksandr", "Saltanat +50%", "power", 1.50),
        "antigon": m("Antigon I", "Nazorat", "cost", 0.85),
        "polemey": m("Polemey I", "Ilm va xazina", "gold", 1.30)
    }),
    "yaponiya": e("Tokugava shogunati", ANTIK, "Edo", {
        "tokugava": m("Tokugava", "Intizom", "tax", 1.30),
        "nobunaga": m("Oda Nobunaga", "Islohotlar", "power", 1.35),
        "toyotomi": m("Toyotomi", "Birlik", "cost", 0.85),
        "miyamoto": m("Miyamoto", "Mahorat", "power", 1.20)
    }),
    "turk_xoqonligi": e("Buyuk Turk xoqonligi", ANTIK, "Suyob", {
        "bumin": m("Bumin Xoqon", "Qudrat", "power", 1.35),
        "istami": m("Istami Yabg'u", "Ipak yo'li", "gold", 1.30),
        "tardu": m("Tardu", "Kengayish", "cost", 0.80),
        "bilga": m("Bilga Xoqon", "Soliq", "tax", 1.30)
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
alliances = {}

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot ishlamoqda!")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = ThreadingHTTPServer(("0.0.0.0", port), HealthHandler)
    server.serve_forever()

def get_main_menu_markup():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📜 Profil", callback_data="profile"),
        types.InlineKeyboardButton("🗺 Xarita", callback_data="map"),
        types.InlineKeyboardButton("⚔️ Qorgon", callback_data="army_menu"),
        types.InlineKeyboardButton("💰 Soliq", callback_data="collect_tax"),
        types.InlineKeyboardButton("🤝 Diplomatiya", callback_data="diplomacy_menu"),
        types.InlineKeyboardButton("🏆 Reyting", callback_data="leaderboard")
    )
    return markup

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
            btn_text = f"👑 {m_val['name']} ({m_val['desc']})"
            btn_data = f"monarch_{emp_key}_{m_key}"
            markup.add(types.InlineKeyboardButton(btn_text, callback_data=btn_data))
        markup.add(types.InlineKeyboardButton("🔙 Orqaga", callback_data=f"cat_{emp['group']}"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"✅ **{emp['name']}** uchun Hukmdorni tanlang:", reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("monarch_"):
        parts = call.data.split("_", 2)
        emp_key = parts[1]
        monarch_key = parts[2]
        emp = EMPIRES[emp_key]
        monarch = emp["monarchs"][monarch_key]
        initial_gold = int(emp["gold"] * monarch["val"]) if monarch["type"] == "gold" else emp["gold"]

        user_game_data[user_id] = {
            "empire": emp_key, "monarch": monarch_key, "player_name": call.from_user.first_name,
            "gold": initial_gold, "conquered": [], "army": {"piyoda": 0, "otliq": 0, "qamal": 0},
            "total_power": 0, "last_tax_time": 0
        }

        bot.answer_callback_query(call.id, f"Hukmdor {monarch['name']} tanlandi!")
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"👑 **{emp['name']}**\nHukmdor: {monarch['name']}\n💰 Xazina: {initial_gold:,} oltin", reply_markup=get_main_menu_markup(), parse_mode="Markdown")

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

    # DIPLOMATIYA BO'LIMI
    elif call.data == "diplomacy_menu":
        data = user_game_data.get(user_id)
        if not data: return
        
        other_players = [uid for uid in user_game_data.keys() if uid != user_id]
        markup = types.InlineKeyboardMarkup(row_width=1)
        if not other_players:
            markup.add(types.InlineKeyboardButton("❌ Hozircha boshqa o'yinchilar yo'q", callback_data="none"))
        else:
            for op_id in other_players:
                op_name = user_game_data[op_id]["player_name"]
                op_emp = EMPIRES[user_game_data[op_id]["empire"]]["name"]
                markup.add(types.InlineKeyboardButton(f"🤝 Alyans taklif qilish: {op_name} ({op_emp})", callback_data=f"alliance_{op_id}"))
        
        markup.add(types.InlineKeyboardButton("🔙 Menyu", callback_data="back_to_menu"))
        bot.answer_callback_query(call.id)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🤝 **Diplomatiya Markazi**\n\nBoshqa real o'yinchi bilan alyans tuzing:", reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("alliance_"):
        target_id = int(call.data.split("_")[1])
        sender_name = user_game_data[user_id]["player_name"]
        
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("✅ Qabul qilish", callback_data=f"accept_all_{user_id}"),
            types.InlineKeyboardButton("❌ Rad etish", callback_data=f"reject_all_{user_id}")
        )
        bot.send_message(target_id, f"👑 **{sender_name}** sizga alyans taklif qilmoqda!", reply_markup=markup, parse_mode="Markdown")
        bot.answer_callback_query(call.id, "Alyans taklifingiz yuborildi!", show_alert=True)

    elif call.data.startswith("accept_all_"):
        sender_id = int(call.data.split("_")[2])
        if user_id not in alliances: alliances[user_id] = []
        if sender_id not in alliances[user_id]: alliances[user_id].append(sender_id)
        
        if sender_id not in alliances: alliances[sender_id] = []
        if user_id not in alliances[sender_id]: alliances[sender_id].append(user_id)
        
        bot.answer_callback_query(call.id, "Alyans muvaffaqiyatli tuzildi!", show_alert=True)
        bot.send_message(sender_id, f"🎉 {user_game_data[user_id]['player_name']} alyans taklifingizni qabul qildi!")
        
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("🔄 Barter", callback_data=f"inter_barter_{user_id}"),
            types.InlineKeyboardButton("💂‍♂️ Askar so'rash", callback_data=f"inter_army_{user_id}"),
            types.InlineKeyboardButton("👑 Vassallik", callback_data=f"inter_vassal_{user_id}"),
            types.InlineKeyboardButton("🔙 Menyu", callback_data="back_to_menu")
        )
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🤝 **Ittifoqdoshsiz!** Nima qilmoqchisiz?", reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("reject_all_"):
        sender_id = int(call.data.split("_")[2])
        bot.answer_callback_query(call.id, "Taklif rad etildi.")
        bot.send_message(sender_id, f"❌ {user_game_data[user_id]['player_name']} alyans taklifini rad etdi.")

    elif call.data.startswith("inter_barter_") or call.data.startswith("inter_army_") or call.data.startswith("inter_vassal_"):
        parts = call.data.split("_")
        action = parts[1]
        target_id = int(parts[2])
        
        sender_name = user_game_data[user_id]["player_name"]
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("✅ Roziman", callback_data=f"res_yes_{action}_{user_id}"),
            types.InlineKeyboardButton("❌ Yo'q", callback_data=f"res_no_{action}")
        )
        
        text_map = {
            "barter": f"🔄 **{sender_name}** sizga barter taklif qilmoqda. Rozimisiz?",
            "army": f"💂‍♂️ **{sender_name}** sizdan askar so'ramoqda. Yuborasizmi?",
            "vassal": f"👑 **{sender_name}** sizni vassal qilishni so'ramoqda. Rozimisiz?"
        }
        bot.send_message(target_id, text_map[action], reply_markup=markup, parse_mode="Markdown")
        bot.answer_callback_query(call.id, "So'rov yuborildi!", show_alert=True)

    elif call.data.startswith("res_yes_"):
        parts = call.data.split("_")
        action = parts[2]
        sender_id = int(parts[3])
        
        if action == "barter":
            user_game_data[user_id]["gold"] += 2_000_000
            if sender_id in user_game_data: user_game_data[sender_id]["gold"] += 2_000_000
            bot.send_message(sender_id, "✅ Barter bajarildi: +2,000,000 oltin!")
        elif action == "army":
            if sender_id in user_game_data:
                user_game_data[sender_id]["army"]["piyoda"] += 3
                user_game_data[sender_id]["total_power"] += 30
            bot.send_message(sender_id, "✅ Ittifoqchingiz 3 ta piyoda yubordi!")
        elif action == "vassal":
            bot.send_message(sender_id, "✅ Vassallik shartnomasi tuzildi!")
            
        bot.answer_callback_query(call.id, "Bajarildi!", show_alert=True)

    elif call.data.startswith("res_no_"):
        bot.answer_callback_query(call.id, "Taklif rad etildi.")

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
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"✅ **{emp['name']}**\n💰 Xazina: {data['gold']:,} oltin", reply_markup=get_main_menu_markup(), parse_mode="Markdown")

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
            bot.answer_callback_query(call.id, "Oltin yetarli emas!", show_alert=True)
            return

        markup = types.InlineKeyboardMarkup(row_width=1)
        for tk, tv in TROOPS.items():
            c = int(tv["cost"] * (monarch["val"] if monarch["type"] == "cost" else 1.0))
            markup.add(types.InlineKeyboardButton(f"➕ {tv['name']} ({c:,} oltin)", callback_data=f"recruit_{tk}"))
        markup.add(types.InlineKeyboardButton("🔙 Menyu", callback_data="back_to_menu"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"⚔️ **Harbiy Qorgon:**\n💂‍♂️ Piyoda: {data['army']['piyoda']}\n🐎 Otliq: {data['army']['otliq']}\n💣 Qamal: {data['army']['qamal']}\n🛡 Kuch: {data['total_power']}\n💰 Xazina: {data['gold']:,}", reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("conquer_"):
        p_key = call.data.split("_", 1)[1]
        data = user_game_data.get(user_id)
        if not data: return
        monarch = EMPIRES[data["empire"]]["monarchs"][data["monarch"]]
        prov = PROVINCES[p_key]
        cost = int(prov["cost"] * (monarch["val"] if monarch["type"] == "cost" else 1.0))

        if data["gold"] < cost:
            bot.answer_callback_query(call.id, "Oltin yetarli emas!", show_alert=True)
            return

        req_pwr = prov["power_required"]
        
        if data["total_power"] < req_pwr:
            data["army"] = {"piyoda": 0, "otliq": 0, "qamal": 0}
            data["total_power"] = 0
            bot.answer_callback_query(call.id, "Mag'lubiyat! Armiyangiz yo'q qilindi!", show_alert=True)
            markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔙 Menyu", callback_data="back_to_menu"))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"💀 **Mag'lubiyat!**\n{prov['name']} uchun jangda armiyangiz qirilib ketdi.\n🛡 Kuch: 0", reply_markup=markup, parse_mode="Markdown")
            return

        data["gold"] -= cost
        old_pwr = data["total_power"]
        new_pwr = old_pwr - req_pwr
        ratio = new_pwr / old_pwr if old_pwr > 0 else 0
        
        data["army"]["piyoda"] = int(data["army"]["piyoda"] * ratio)
        data["army"]["otliq"] = int(data["army"]["otliq"] * ratio)
        data["army"]["qamal"] = int(data["army"]["qamal"] * ratio)
        data["total_power"] = new_pwr
        data["conquered"].append(p_key)

        bot.answer_callback_query(call.id, f"G'alaba! -{req_pwr} kuch yo'qotildi.")
        markup = types.InlineKeyboardMarkup(row_width=1)
        for pk, pv in PROVINCES.items():
            if pk not in data["conquered"]:
                c = int(pv["cost"] * (monarch["val"] if monarch["type"] == "cost" else 1.0))
                markup.add(types.InlineKeyboardButton(f"⚔️ {pv['name']} ({c:,} oltin | {pv['power_required']} kuch)", callback_data=f"conquer_{pk}"))
        markup.add(types.InlineKeyboardButton("🔙 Menyu", callback_data="back_to_menu"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"🎉 **G'alaba!** {prov['name']} zabt etildi!\n💥 Yo'qotilgan kuch: -{req_pwr}\n💰 Xazina: {data['gold']:,}\n🛡 Qolgan kuch: {data['total_power']}", reply_markup=markup, parse_mode="Markdown")

    elif call.data == "back_to_menu":
        data = user_game_data.get(user_id)
        if not data: return
        emp = EMPIRES[data["empire"]]
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"✅ **{emp['name']}**\n💰 Xazina: {data['gold']:,} oltin\n🛡 Kuch: {data['total_power']}", reply_markup=get_main_menu_markup(), parse_mode="Markdown")

if __name__ == "__main__":
    threading.Thread(target=run_server, daemon=True).start()
    bot.remove_webhook()
    print("Bot ishga tushdi...")
    while True:
        try:
            bot.infinity_polling(skip_pending=True, timeout=60, long_polling_timeout=60)
        except Exception as e:
            print(f"Xatolik: {e}")
            time.sleep(5)
