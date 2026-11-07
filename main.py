import os
import time
import threading
import sqlite3
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import telebot
from telebot import types

TOKEN = "9163206553:AAEjs1mCITIow9KnvmTjGzr6f0wNdHmlRvQ"
bot = telebot.TeleBot(TOKEN)

START_GOLD = 100_000_000
EAST, EUROPE, ANTIK = "Sharq", "Yevropa", "Antik"

def init_db():
    conn = sqlite3.connect('game.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS players (
        user_id INTEGER PRIMARY KEY, player_name TEXT, empire TEXT, 
        monarch TEXT, gold INTEGER, conquered TEXT, army_piyoda INTEGER, 
        army_otliq INTEGER, army_qamal INTEGER, total_power INTEGER, last_tax_time REAL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS alliances (user_id_1 INTEGER, user_id_2 INTEGER)''')
    conn.commit()
    conn.close()

init_db()

def get_db():
    return sqlite3.connect('game.db', check_same_thread=False)

def get_user_data(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT player_name, empire, monarch, gold, conquered, army_piyoda, army_otliq, army_qamal, total_power, last_tax_time FROM players WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "player_name": row[0], "empire": row[1], "monarch": row[2], "gold": row[3],
            "conquered": row[4].split(",") if row[4] else [],
            "army": {"piyoda": row[5], "otliq": row[6], "qamal": row[7]},
            "total_power": row[8], "last_tax_time": row[9]
        }
    return None

def save_user_data(user_id, data):
    conn = get_db()
    cursor = conn.cursor()
    conquered_str = ",".join(data["conquered"])
    cursor.execute('''INSERT OR REPLACE INTO players 
        (user_id, player_name, empire, monarch, gold, conquered, army_piyoda, army_otliq, army_qamal, total_power, last_tax_time)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
        (user_id, data["player_name"], data["empire"], data["monarch"], data["gold"], conquered_str, 
         data["army"]["piyoda"], data["army"]["otliq"], data["army"]["qamal"], data["total_power"], data["last_tax_time"]))
    conn.commit()
    conn.close()

def get_all_users():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, player_name, empire, monarch, gold, conquered, army_piyoda, army_otliq, army_qamal, total_power, last_tax_time FROM players")
    rows = cursor.fetchall()
    conn.close()
    users = {}
    for row in rows:
        users[row[0]] = {
            "player_name": row[1], "empire": row[2], "monarch": row[3], "gold": row[4],
            "conquered": row[5].split(",") if row[5] else [],
            "army": {"piyoda": row[6], "otliq": row[7], "qamal": row[8]},
            "total_power": row[9], "last_tax_time": row[10]
        }
    return users

def m(name, desc, type_, val):
    return {"name": name, "desc": desc, "type": type_, "val": val}

def e(name, group, cap, monarchs):
    return {"name": name, "group": group, "gold": START_GOLD, "capital": cap, "monarchs": monarchs}

EMPIRES = {
    "temuriylar": e("Temuriylar", EAST, "Samarqand", {"timur": m("Amir Timur", "Quvvat +25%", "power", 1.25), "shohrux": m("Shohrux", "Soliq +20%", "tax", 1.20), "ulugbek": m("Ulug'bek", "Narx -15%", "cost", 0.85), "husayn": m("Husayn Boyqaro", "Xazina", "gold", 1.20)}),
    "omaviylar": e("Omaviylar", EAST, "Damashq", {"muoviya": m("Muoviya I", "Diplomatiya", "cost", 0.90), "abdulmalik": m("Abdulmalik", "Soliq +30%", "tax", 1.30), "valid": m("Valid I", "Zabt -10%", "power", 1.10), "umar2": m("Umar II", "Adolat", "gold", 1.20)}),
    "abbosiylar": e("Abbosiylar", EAST, "Bagdod", {"horun": m("Horun ar-Rashid", "Xazina", "gold", 1.30), "mamun": m("Al-Ma'mun", "Narx -10%", "cost", 0.90), "mansur": m("Al-Mansur", "Soliq", "tax", 1.20), "mutasim": m("Al-Mu'tasim", "Armiya", "power", 1.15)}),
    "usmonlilar": e("Usmonlilar", EAST, "Istanbul", {"osman": m("Osman I", "Asos", "gold", 1.15), "mehmed": m("Fotih Mehmed", "Qamal", "power", 1.30), "sulaymon": m("Sulaymon", "Zabt -20%", "cost", 0.80), "boyazid": m("Boyazid", "Hujum", "power", 1.25)}),
    "ayyubiylar": e("Ayyubiylar", EAST, "Qohira", {"salohiddin": m("Salohiddin", "Quvvat", "power", 1.25), "adil": m("Al-Adil", "Soliq", "tax", 1.20), "komil": m("Al-Komil", "Narx", "cost", 0.85), "nosir": m("Nosir", "Otliq", "power", 1.20)}),
    "xorazmshohlar": e("Xorazmshohlar", EAST, "Urganch", {"anushtegin": m("Anushtegin", "Soliq", "tax", 1.10), "otsiz": m("Otsiz", "Narx", "cost", 0.85), "muhammad": m("Muhammad II", "Armiya", "power", 1.20), "jaloliddin": m("Jaloliddin", "Qahramon", "power", 1.35)}),
    "gaznaviylar": e("Gaznaviylar", EAST, "Gazna", {"sabuqtigin": m("Sabuqtigin", "Xazina", "gold", 1.15), "mahmud": m("Mahmud", "Oltin +30%", "tax", 1.30), "masud": m("Mas'ud I", "Otliq", "power", 1.20), "ibrohim": m("Ibrohim", "Barqaror", "tax", 1.15)}),
    "safaviylar": e("Safaviylar", EAST, "Isfahon", {"ismoil": m("Ismoil I", "Shijoat", "power", 1.25), "abbos": m("Shoh Abbos", "Savdo", "tax", 1.30), "tahmosib": m("Tahmasp I", "Himoya", "power", 1.15), "husayn_s": m("Sulton Husayn", "Madaniyat", "gold", 1.20)}),
    "boburiylar": e("Boburiylar", EAST, "Dehli", {"bobur": m("Zahriddin Bobur", "Taktika", "power", 1.25), "akbar": m("Akbarshoh", "Soliq", "tax", 1.30), "jahon": m("Shoh Jahon", "Xazina", "gold", 1.25), "avrangzeb": m("Avrangzeb", "Narx", "cost", 0.80)}),
    "oltin_orda": e("Oltin Orda", EAST, "Saroy", {"botu": m("Botuxon", "Soliq", "tax", 1.35), "beraka": m("Berakaxon", "Savdo", "gold", 1.20), "uzbek": m("O'zbekxon", "Barqaror", "tax", 1.20), "toxtamish": m("To'xtamish", "Hujum", "power", 1.20)}),
    "shayboniylar": e("Shayboniylar", EAST, "Samarqand", {"abulxayr": m("Abulxayr", "Dasht", "power", 1.25), "shayboniy": m("Shayboniy", "Birlik", "power", 1.35), "ubaydulla": m("Ubaydulla", "Soliq", "tax", 1.30), "abdulla2": m("Abdullaxon II", "Narx", "cost", 0.80)}),
    "buxoro_amirligi": e("Buxoro amirligi", EAST, "Buxoro", {"rahimxon_b": m("Rahimxon", "Asos", "power", 1.25), "shohmurod": m("Shohmurod", "Soliq", "tax", 1.30), "haydar": m("Amir Haydar", "Ilm", "gold", 1.20), "olimxon": m("Olimxon", "Mudofaa", "power", 1.25)}),
    "xiva_xonligi": e("Xiva xonligi", EAST, "Xiva", {"olloquli": m("Olloquli", "Ichan qal'a", "gold", 1.30), "rahimxon2": m("Rahimxon II", "Soliq", "tax", 1.35), "isfandiyor": m("Isfandiyor", "Islohot", "tax", 1.20), "junaid": m("Junaidxon", "Shijoat", "power", 1.30)}),
    "qoqon_xonligi": e("Qo'qon xonligi", EAST, "Qo'qon", {"norbotabiy": m("Norbo'tabiy", "Xazina", "gold", 1.25), "olimxon_q": m("Olimxon", "Armiya", "power", 1.30), "madalixon": m("Madalixon", "Savdo", "tax", 1.35), "xudoyorxon": m("Xudoyorxon", "Saroy", "gold", 1.25)}),
    "salibchilar": e("Salibchilar", EAST, "Quddus", {"gotfrid": m("Gotfrid", "Asos", "power", 1.25), "baldvin4": m("Baldvin IV", "Mudofaa", "power", 1.30), "richard": m("Richard", "Quvvat", "power", 1.40), "reno": m("Reno", "Shijoat", "tax", 1.20)}),
    "saljuqiylar": e("Saljuqiylar", EAST, "Isfahon", {"togʻrulbek": m("Togʻrulbek", "Asos", "power", 1.25), "alp_arslon": m("Alp Arslon", "Quvvat", "power", 1.40), "malikshoh": m("Malikshoh", "Oltin davr", "tax", 1.35), "sultan_sanjar": m("Sanjar", "Kengayish", "gold", 1.30)}),
    
    "britaniya": e("Britaniya", EUROPE, "London", {"elizaveta": m("Yelizaveta I", "Flot", "gold", 1.30), "viktoriya": m("Viktoriya", "Soliq", "tax", 1.35), "cherchill": m("Cherchill", "Qat'iyat", "power", 1.25), "genrix8": m("Genrix VIII", "Siyosat", "cost", 0.90)}),
    "rim": e("Rim", EUROPE, "Rim", {"sezar": m("Yuliy Sezar", "Legion", "power", 1.30), "august": m("August", "Infratuzilma", "tax", 1.25), "trayan": m("Trayan", "Zabt", "cost", 0.80), "konstantin_r": m("Konstantin", "Barqaror", "gold", 1.20)}),
    "fransiya": e("Fransiya", EUROPE, "Parij", {"karl_buyuk": m("Karl Buyuk", "Qudrat", "power", 1.25), "lyudovik": m("Lyudovik XIV", "Soliq", "tax", 1.35), "napoleon": m("Napoleon", "Strategiya", "power", 1.40), "jovanni": m("Janna d'Ark", "Ruh", "power", 1.20)}),
    "rossiya": e("Rossiya", EUROPE, "Sankt-Peterburg", {"pyotr": m("Buyuk Pyotr", "Sanoat", "gold", 1.30), "yekaterina": m("Yekaterina II", "Kengayish", "cost", 0.65), "ivan": m("Ivan Grozniy", "Tazyiq", "power", 1.25), "alex2": m("Aleksandr II", "O'sish", "tax", 1.20)}),
    "ispan": e("Ispaniya", EUROPE, "Madrid", {"izabella": m("Izabella", "Ekspeditsiya", "gold", 1.30), "karl5": m("Karl V", "Soliq", "tax", 1.25), "filipp2": m("Filipp II", "Flot", "power", 1.25), "elcid": m("El Cid", "Jangovar ruh", "power", 1.20)}),
    "natsist_germaniya": e("Germaniya", EUROPE, "Berlin", {"gitler": m("Adolf Gitler", "Blitskrig", "power", 1.40), "gebbels": m("Gebbel", "Targ'ibot", "gold", 1.25), "goring": m("Goring", "Arzon qo'shin", "cost", 0.80), "gimmler": m("Gimmler", "Tartib", "tax", 1.30)}),
    "aqsh": e("AQSh", EUROPE, "Vashington", {"washington": m("Vashington", "Ozodlik", "power", 1.30), "lincoln": m("Linkoln", "Birlik", "tax", 1.30), "roosevelt": m("Ruzvelt", "Iqtisod", "gold", 1.35), "kennedy": m("Kennedi", "Innovatsiya", "cost", 0.80)}),
    "sssr": e("SSSR", EUROPE, "Moskva", {"lenin": m("Lenin", "Resurs", "gold", 1.25), "stalin": m("Stalin", "Qizil armiya", "power", 1.40), "xrushov": m("Xrushov", "Sanoat", "tax", 1.30), "brejnev": m("Brejnev", "Arzon qo'shin", "cost", 0.85)}),
    "vizantiya": e("Vizantiya", EUROPE, "Konstantinopol", {"yustinian": m("Yustinian I", "Qonun", "tax", 1.30), "konstantin_v": m("Konstantin", "Poytaxt", "gold", 1.25), "vasiliy": m("Vasiliy II", "Quvvat", "power", 1.30), "irakliy": m("Irakliy", "Xavfsizlik", "power", 1.15)}),
    "gon_sivar": e("Muqaddas Rim", EUROPE, "Aaxen", {"otton": m("Otton I", "Qudrat", "power", 1.25), "barbarossa": m("Barbarossa", "Narx", "cost", 0.80), "charlz5": m("Charlz V", "Soliq", "tax", 1.30), "genrix4": m("Genrix IV", "Barqaror", "gold", 1.20)}),

    "mongol": e("Mo'g'ullar", ANTIK, "Qoraqurum", {"chingiz": m("Chingizxon", "Tezkor yurish", "power", 1.45), "oqotay": m("O'qotay xon", "Boshqaruv", "tax", 1.30), "qubilay": m("Qubilay xon", "Savdo", "gold", 1.35), "huloku": m("Hulokuxon", "Bosqin", "power", 1.35)}),
    "xunnu": e("Buyuk Xunnu", ANTIK, "Utuken", {"modun": m("Modun Chanyu", "Otliqlar", "power", 1.35), "laoshang": m("Lao-shang", "Kengayish", "cost", 0.85), "gunlu": m("Gunlu", "Quvvat", "power", 1.20), "hohanxie": m("Ho-han-xie", "Barqaror", "tax", 1.15)}),
    "qadimgi_xitoy": e("Sin imperiyasi", ANTIK, "Sian", {"sinshi": m("Sin Shi Huang", "Soliq", "tax", 1.40), "xanvudi": m("Xan Vu-di", "Ipak yo'li", "gold", 1.30), "taytsun": m("Taytsun", "Oltin davr", "tax", 1.35), "suyvendi": m("Suy Vendi", "Birlik", "cost", 0.85)}),
    "fors_ahamoniylar": e("Ahamoniylar", ANTIK, "Persepol", {"kir2": m("Kir II", "Bagrikenglik", "tax", 1.30), "doro1": m("Doro I", "Logistika", "cost", 0.80), "kserks": m("Kserks I", "Armiya", "power", 1.25), "artakserks": m("Artakserks I", "Barqaror", "gold", 1.20)}),
    "qadimgi_misr": e("Qadimgi Misr", ANTIK, "Memfis", {"ramses": m("Ramses II", "Obidalar", "power", 1.30), "tutmos": m("Tutmos III", "Kengayish", "cost", 0.75), "kleopatra": m("Kleopatra", "Xazina", "gold", 1.30), "exnaton": m("Exnaton", "Madaniyat", "tax", 1.20)}),
    "makedoniya": e("Makedoniya", ANTIK, "Pella", {"filipp2_m": m("Filipp II", "Falanga", "power", 1.25), "aleksandr": m("Aleksandr", "Saltanat", "power", 1.50), "antigon": m("Antigon I", "Nazorat", "cost", 0.85), "polemey": m("Polemey I", "Ilm", "gold", 1.30)}),
    "yaponiya": e("Tokugava", ANTIK, "Edo", {"tokugava": m("Tokugava", "Intizom", "tax", 1.30), "nobunaga": m("Oda Nobunaga", "Islohot", "power", 1.35), "toyotomi": m("Toyotomi", "Birlik", "cost", 0.85), "miyamoto": m("Miyamoto", "Mahorat", "power", 1.20)}),
    "turk_xoqonligi": e("Turk xoqonligi", ANTIK, "Suyob", {"bumin": m("Bumin Xoqon", "Qudrat", "power", 1.35), "istami": m("Istami Yabg'u", "Ipak yo'li", "gold", 1.30), "tardu": m("Tardu", "Kengayish", "cost", 0.80), "bilga": m("Bilga Xoqon", "Soliq", "tax", 1.30)})
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
            markup.add(types.InlineKeyboardButton(f"👑 {m_val['name']} ({m_val['desc']})", callback_data=f"monarch_{emp_key}_{m_key}"))
        markup.add(types.InlineKeyboardButton("🔙 Orqaga", callback_data=f"cat_{emp['group']}"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"✅ **{emp['name']}** uchun Hukmdorni tanlang:", reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("monarch_"):
        parts = call.data.split("_", 2)
        emp_key = parts[1]
        monarch_key = parts[2]
        emp = EMPIRES[emp_key]
        monarch = emp["monarchs"][monarch_key]
        initial_gold = int(emp["gold"] * monarch["val"]) if monarch["type"] == "gold" else emp["gold"]

        user_data = {
            "empire": emp_key, "monarch": monarch_key, "player_name": call.from_user.first_name,
            "gold": initial_gold, "conquered": [], "army": {"piyoda": 0, "otliq": 0, "qamal": 0},
            "total_power": 0, "last_tax_time": 0
        }
        save_user_data(user_id, user_data)

        bot.answer_callback_query(call.id, f"Hukmdor {monarch['name']} tanlandi!")
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"👑 **{emp['name']}**\nHukmdor: {monarch['name']}\n💰 Xazina: {initial_gold:,} oltin", reply_markup=get_main_menu_markup(), parse_mode="Markdown")

    elif call.data == "profile":
        data = get_user_data(user_id)
        if not data: return
        emp = EMPIRES[data["empire"]]
        monarch = emp["monarchs"][data["monarch"]]
        conq = ", ".join([PROVINCES[p]["name"] for p in data["conquered"]]) if data["conquered"] else "Yo'q"
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, f"📜 **Profil:**\n👑 Imperiya: {emp['name']}\n👑 Hukmdor: {monarch['name']}\n⚔️ Zabt etilgan: {conq}\n🛡 Kuch: {data['total_power']}\n💰 Xazina: {data['gold']:,} oltin", parse_mode="Markdown")

    elif call.data == "map":
        data = get_user_data(user_id)
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
        data = get_user_data(user_id)
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

    elif call.data == "diplomacy_menu":
        data = get_user_data(user_id)
        if not data: return
        all_players = get_all_users()
        other_players = [uid for uid in all_players.keys() if uid != user_id]
        markup = types.InlineKeyboardMarkup(row_width=1)
        if not other_players:
            markup.add(types.InlineKeyboardButton("❌ Hozircha boshqa o'yinchilar yo'q", callback_data="none"))
        else:
            for op_id in other_players:
                op_name = all_players[op_id]["player_name"]
                op_emp = EMPIRES[all_players[op_id]["empire"]]["name"]
                markup.add(types.InlineKeyboardButton(f"🤝 Alyans taklif qilish: {op_name} ({op_emp})", callback_data=f"alliance_{op_id}"))
        markup.add(types.InlineKeyboardButton("🔙 Menyu", callback_data="back_to_menu"))
        bot.answer_callback_query(call.id)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🤝 **Diplomatiya Markazi**\n\nBoshqa real o'yinchi bilan alyans tuzing:", reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("alliance_"):
        target_id = int(call.data.split("_")[1])
        sender_data = get_user_data(user_id)
        sender_name = sender_data["player_name"] if sender_data else "O'yinchi"
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("✅ Qabul qilish", callback_data=f"accept_all_{user_id}"),
            types.InlineKeyboardButton("❌ Rad etish", callback_data=f"reject_all_{user_id}")
        )
        bot.send_message(target_id, f"👑 **{sender_name}** sizga alyans taklif qilmoqda!", reply_markup=markup, parse_mode="Markdown")
        bot.answer_callback_query(call.id, "Alyans taklifingiz yuborildi!", show_alert=True)

    elif call.data.startswith("accept_all_"):
        sender_id = int(call.data.split("_")[2])
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM alliances WHERE (user_id_1 = ? AND user_id_2 = ?) OR (user_id_1 = ? AND user_id_2 = ?)", (user_id, sender_id, sender_id, user_id))
        if not cursor.fetchone():
            cursor.execute("INSERT INTO alliances (user_id_1, user_id_2) VALUES (?, ?)", (user_id, sender_id))
            conn.commit()
        conn.close()
        bot.answer_callback_query(call.id, "Alyans muvaffaqiyatli tuzildi!", show_alert=True)
        my_data = get_user_data(user_id)
        if sender_id in get_all_users():
            bot.send_message(sender_id, f"🎉 {my_data['player_name']} alyans taklifingizni qabul qildi!")
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
        my_data = get_user_data(user_id)
        bot.send_message(sender_id, f"❌ {my_data['player_name'] if my_data else 'O\'yinchi'} alyans taklifini rad etdi.")

    elif call.data.startswith("inter_barter_") or call.data.startswith("inter_army_") or call.data.startswith("inter_vassal_"):
        parts = call.data.split("_")
        action = parts[1]
        target_id = int(parts[2])
        my_data = get_user_data(user_id)
        sender_name = my_data["player_name"] if my_data else "O'yinchi"
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
            u_data = get_user_data(user_id)
            if u_data:
                u_data["gold"] += 2_000_000
                save_user_data(user_id, u_data)
            s_data = get_user_data(sender_id)
            if s_data:
                s_data["gold"] += 2_000_000
                save_user_data(sender_id, s_data)
                bot.send_message(sender_id, "✅ Barter bajarildi: +2,000,000 oltin!")
        elif action == "army":
            s_data = get_user_data(sender_id)
            if s_data:
                s_data["army"]["piyoda"] += 3
                s_data["total_power"] += 30
                save_user_data(sender_id, s_data)
                bot.send_message(sender_id, "✅ Ittifoqchingiz 3 ta piyoda yubordi!")
        elif action == "vassal":
            bot.send_message(sender_id, "✅ Vassallik shartnomasi tuzildi!")
        bot.answer_callback_query(call.id, "Bajarildi!", show_alert=True)

    elif call.data.startswith("res_no_"):
        bot.answer_callback_query(call.id, "Taklif rad etildi.")

    elif call.data == "collect_tax":
        data = get_user_data(user_id)
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
        save_user_data(user_id, data)
        bot.answer_callback_query(call.id, f"+{tax:,} oltin olindi!")
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"✅ **{emp['name']}**\n💰 Xazina: {data['gold']:,} oltin", reply_markup=get_main_menu_markup(), parse_mode="Markdown")

    elif call.data == "leaderboard":
        all_p = get_all_users()
        sorted_p = sorted(all_p.items(), key=lambda x: x[1].get("total_power", 0), reverse=True)
        txt = "🏆 **Top 10 Reyting:**\n\n"
        for i, (u, p) in enumerate(sorted_p[:10], 1):
            txt += f"{i}. **{p.get('player_name')}** | 🛡 {p['total_power']} kuch\n"
        markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔙 Menyu", callback_data="back_to_menu"))
        bot.answer_callback_query(call.id)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=txt, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("recruit_"):
        t_key = call.data.split("_", 1)[1]
        data = get_user_data(user_id)
        if not data: return
        monarch = EMPIRES[data["empire"]]["monarchs"][data["monarch"]]
        t_val = TROOPS[t_key]
        cost = int(t_val["cost"] * (monarch["val"] if monarch["type"] == "cost" else 1.0))
        pwr = int(t_val["power"] * (monarch["val"] if monarch["type"] == "power" else 1.0))
        if data["gold"] >= cost:
            data["gold"] -= cost
            data["army"][t_key] += 1
            data["total_power"] += pwr
            save_user_data(user_id, data)
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
        data = get_user_data(user_id)
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
            save_user_data(user_id, data)
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
        save_user_data(user_id, data)
        bot.answer_callback_query(call.id, f"G'alaba! -{req_pwr} kuch yo'qotildi.")
        markup = types.InlineKeyboardMarkup(row_width=1)
        for pk, pv in PROVINCES.items():
            if pk not in data["conquered"]:
                c = int(pv["cost"] * (monarch["val"] if monarch["type"] == "cost" else 1.0))
                markup.add(types.InlineKeyboardButton(f"⚔️ {pv['name']} ({c:,} oltin | {pv['power_required']} kuch)", callback_data=f"conquer_{pk}"))
        markup.add(types.InlineKeyboardButton("🔙 Menyu", callback_data="back_to_menu"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"🎉 **G'alaba!** {prov['name']} zabt etildi!\n💥 Yo'qotilgan kuch: -{req_pwr}\n💰 Xazina: {data['gold']:,}\n🛡 Qolgan kuch: {data['total_power']}", reply_markup=markup, parse_mode="Markdown")

    elif call.data == "back_to_menu":
        data = get_user_data(user_id)
        if not data: return
        emp = EMPIRES[data["empire"]]
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"✅ **{emp['name']}**\n💰 Xazina: {data['gold']:,} oltin\n🛡 Kuch: {data['total_power']}", reply_markup=get_main_menu_markup(), parse_mode="Markdown")

if __name__ == "__main__":
    threading.Thread(target=run_server, daemon=True).start()
    bot.remove_webhook()
    print("Bot ishga tushdi va bazaga ulandi...")
    while True:
        try:
            bot.infinity_polling(skip_pending=True, timeout=60, long_polling_timeout=60)
        except Exception as e:
            print(f"Xatolik: {e}")
            time.sleep(5)
