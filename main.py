import os
import time
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import telebot
from telebot import types

# ----------------------------------------------------------------------
# Token va Botni sozlash
# ----------------------------------------------------------------------
TOKEN = "9163206553:AAEjs1mCITIow9KnvmTjGzr6f0wNdHmlRvQ"
bot = telebot.TeleBot(TOKEN)

START_GOLD = 100_000_000

EAST = "Sharq va Islom olami"
EUROPE = "Yevropa va Jahon"
ANTIK = "Antik va Osiyo"


def m(name, desc, type_, val):
    return {"name": name, "desc": desc, "type": type_, "val": val}


def e(name, group, spec, cap, cities, monarchs):
    return {
        "name": name,
        "group": group,
        "specialization": spec,
        "gold": START_GOLD,
        "capital": cap,
        "cities": cities,
        "monarchs": monarchs,
    }


EMPIRES = {
    # SHARQ VA ISLOM OLAMI
    "temuriylar": e("Temuriylar imperiyasi", EAST, "Harbiy / Ilm-fan", "Samarqand", ["Samarqand", "Buxoro", "Hirot"], {
        "timur": m("Amir Timur", "Harbiy quvvat +25%", "power", 1.25),
        "shohrux": m("Shohrux Mirzo", "Soliq +20%", "tax", 1.20),
        "ulugbek": m("Mirzo Ulug'bek", "Qo'shin narxi -15%", "cost", 0.85),
        "husayn": m("Husayn Boyqaro", "Xazina +20%", "gold", 1.20)
    }),
    "omaviylar": e("Omaviylar xalifaligi", EAST, "Diplomatiya / Kengayish", "Damashq", ["Damashq", "Kufa", "Basra"], {
        "muoviya": m("Muoviya I", "Diplomatiya", "cost", 0.90),
        "abdulmalik": m("Abdulmalik", "Soliqlar +30%", "tax", 1.30),
        "valid": m("Valid I", "Zabt kuchi -10%", "power", 1.10),
        "umar2": m("Umar II", "Adolat va xazina", "gold", 1.20)
    }),
    "abbosiylar": e("Abbosiylar xalifaligi", EAST, "Ilm-fan / Madaniyat", "Bagdod", ["Bagdod", "Qohira", "Basra"], {
        "horun": m("Horun ar-Rashid", "Xazina +30%", "gold", 1.30),
        "mamun": m("Al-Ma'mun", "Qo'shin narxi -10%", "cost", 0.90),
        "mansur": m("Al-Mansur", "Soliq +20%", "tax", 1.20),
        "mutasim": m("Al-Mu'tasim", "Armiya +15%", "power", 1.15)
    }),
    "usmonlilar": e("Usmonlilar imperiyasi", EAST, "Harbiy / Flot", "Istanbul", ["Istanbul", "Edirne", "Bursa"], {
        "osman": m("Osman I", "Asoschilik", "gold", 1.15),
        "mehmed": m("Fotih Mehmed", "Qamal +30%", "power", 1.30),
        "sulaymon": m("Sulaymon Qonuniy", "Zabt narxi -20%", "cost", 0.80),
        "boyazid": m("Yildirim Boyazid", "Hujum +25%", "power", 1.25)
    }),
    "ayyubiylar": e("Ayyubiylar sulolasi", EAST, "Harbiy / Himoya", "Qohira", ["Qohira", "Aleppo", "Damashq"], {
        "salohiddin": m("Salohiddin Ayyubi", "Harbiy quvvat +25%", "power", 1.25),
        "adil": m("Al-Adil", "Soliq +20%", "tax", 1.20),
        "komil": m("Al-Komil", "Hudud narxi -15%", "cost", 0.85),
        "nosir": m("An-Nosir Yusuf", "Otliqlar +20%", "power", 1.20)
    }),
    "xorazmshohlar": e("Xorazmshohlar davlati", EAST, "Savdo / Kengayish", "Kunya-Urganch", ["Urganch", "Gurlan", "Marv", "Samarqand"], {
        "anushtegin": m("Anushtegin", "Soliq +10%", "tax", 1.10),
        "otsiz": m("Otsiz", "Hudud narxi -15%", "cost", 0.85),
        "muhammad": m("Muhammad II", "Armiya +20%", "power", 1.20),
        "jaloliddin": m("Jaloliddin Manguberdi", "Qahramonlik +35%", "power", 1.35)
    }),
    "gaznaviylar": e("Gaznaviylar davlati", EAST, "Harbiy / Bosqinchilik", "Gazna", ["Gazna", "Lahor", "Balx"], {
        "sabuqtigin": m("Sabuqtigin", "Xazina +15%", "gold", 1.15),
        "mahmud": m("Mahmud G'aznaviy", "Oltin +30%", "tax", 1.30),
        "masud": m("Mas'ud I", "Otliqlar +20%", "power", 1.20),
        "ibrohim": m("Ibrohim", "Barqarorlik", "tax", 1.15)
    }),
    "safaviylar": e("Safaviylar imperiyasi", EAST, "Madaniyat / Savdo", "Isfahon", ["Isfahon", "Tabriz", "Sheroz"], {
        "ismoil": m("Shoh Ismoil I", "Shijoat +25%", "power", 1.25),
        "abbos": m("Shoh Abbos", "Savdo va soliq +30%", "tax", 1.30),
        "tahmosib": m("Tahmasp I", "Himoya", "power", 1.15),
        "husayn_s": m("Sulton Husayn", "Madaniyat", "gold", 1.20)
    }),
    "boburiylar": e("Boburiylar imperiyasi", EAST, "Arxitektura / Boylik", "Dehli", ["Dehli", "Agra", "Lahor"], {
        "bobur": m("Zahriddin Bobur", "Taktika +25%", "power", 1.25),
        "akbar": m("Akbarshoh", "Soliq +30%", "tax", 1.30),
        "jahon": m("Shoh Jahon", "Xazina +25%", "gold", 1.25),
        "avrangzeb": m("Avrangzeb", "Hudud narxi -20%", "cost", 0.80)
    }),
    "oltin_orda": e("Oltin Orda", EAST, "Ko'chmanchi / Soliq", "Saroy-Bot", ["Saroy-Bot", "Qozon", "Astraxan"], {
        "botu": m("Botuxon", "Soliq yig'ish +35%", "tax", 1.35),
        "beraka": m("Berakaxon", "Savdo +20%", "gold", 1.20),
        "uzbek": m("O'zbekxon", "Barqarorlik", "tax", 1.20),
        "toxtamish": m("To'xtamishxon", "Tezkor hujum", "power", 1.20)
    }),
    "shayboniylar": e("Shayboniylar sulolasi", EAST, "Dasht qudrati", "Samarqand", ["Samarqand", "Buxoro", "Toshkent", "Balx"], {
        "abulxayr": m("Abulxayrxon", "Dasht qudrati", "power", 1.25),
        "shayboniy": m("Muhammad Shayboniy", "Birlashish +35%", "power", 1.35),
        "ubaydulla": m("Ubaydullaxon", "Soliq +30%", "tax", 1.30),
        "abdulla2": m("Abdullaxon II", "Kengaytirish -20%", "cost", 0.80)
    }),
    "buxoro_amirligi": e("Buxoro amirligi", EAST, "Ilm-fan / Diniy markaz", "Buxoro", ["Buxoro", "Samarqand", "Qarshi"], {
        "rahimxon_b": m("Muhammad Rahimxon", "Amirlik asosi", "power", 1.25),
        "shohmurod": m("Shohmurod", "Adolatli siyosat", "tax", 1.30),
        "haydar": m("Amir Haydar", "Ilm-fan", "gold", 1.20),
        "olimxon": m("Said Olimxon", "Mudofaa +25%", "power", 1.25)
    }),
    "xiva_xonligi": e("Xiva xonligi", EAST, "Voha / Shijoat", "Xiva", ["Xiva", "Urganch", "Gurlan"], {
        "olloquli": m("Olloqulixon", "Ichan qal'a", "gold", 1.30),
        "rahimxon2": m("Muhammad Rahimxon II", "Ma'rifat", "tax", 1.35),
        "isfandiyor": m("Isfandiyorxon", "Islohotlar", "tax", 1.20),
        "junaid": m("Junaidxon", "Shijoat", "power", 1.30)
    }),
    "qoqon_xonligi": e("Qo'qon xonligi", EAST, "Vodiy savdosi", "Qo'qon", ["Qo'qon", "Namangan", "Andijon", "O'sh"], {
        "norbotabiy": m("Norbo'tabiy", "Xazina", "gold", 1.25),
        "olimxon_q": m("Olimxon", "Armiya", "power", 1.30),
        "madalixon": m("Madalixon", "Savdo yo'llari", "tax", 1.35),
        "xudoyorxon": m("Xudoyorxon", "Saroy", "gold", 1.25)
    }),
    "salibchilar": e("Salibchilar", EAST, "Ritsarlar / Himoya", "Quddus", ["Quddus", "Antioxiya", "Akkon"], {
        "gotfrid": m("Gotfrid", "Asoschilik", "power", 1.25),
        "baldvin4": m("Baldvin IV", "Mudofaa +30%", "power", 1.30),
        "richard": m("Richard Sheryurak", "Quvvat +40%", "power", 1.40),
        "reno": m("Reno", "Shijoat", "tax", 1.20)
    }),

    # YEVROPA VA JAHON
    "britaniya": e("Britaniya imperiyasi", EUROPE, "Iqtisodiy / Savdo", "London", ["London", "Liverpul", "Edinburg"], {
        "elizaveta": m("Yelizaveta I", "Flot va savdo", "gold", 1.30),
        "viktoriya": m("Viktoriya", "Global soliq", "tax", 1.35),
        "cherchill": m("Uinston Cherchill", "Qat'iyat", "power", 1.25),
        "genrix8": m("Genrix VIII", "Siyosat", "cost", 0.90)
    }),
    "rim": e("Rim imperiyasi", EUROPE, "Infratuzilma", "Rim", ["Rim", "Milano", "Afina"], {
        "sezar": m("Yuliy Sezar", "Legionlar +30%", "power", 1.30),
        "august": m("August", "Infratuzilma", "tax", 1.25),
        "trayan": m("Trayan", "Zabt narxi -20%", "cost", 0.80),
        "konstantin_r": m("Konstantin", "Barqarorlik", "gold", 1.20)
    }),
    "fransiya": e("Fransiya imperiyasi", EUROPE, "Diplomatiya", "Parij", ["Parij", "Marsel", "Lion"], {
        "karl_buyuk": m("Karl Buyuk", "Qudrat", "power", 1.25),
        "lyudovik": m("Lyudovik XIV", "Xazina", "tax", 1.35),
        "napoleon": m("Napoleon", "Strategiya +40%", "power", 1.40),
        "jovanni": m("Janna d'Ark", "Ruh", "power", 1.20)
    }),
    "rossiya": e("Rossiya imperiyasi", EUROPE, "Hudud / Resurslar", "Sankt-Peterburg", ["Moskva", "Sankt-Peterburg", "Kiyev"], {
        "pyotr": m("Buyuk Pyotr", "Sanoat", "gold", 1.30),
        "yekaterina": m("Yekaterina II", "Kengaytirish", "cost", 0.65),
        "ivan": m("Ivan Grozniy", "Tazyiq", "power", 1.25),
        "alex2": m("Aleksandr II", "O'sish", "tax", 1.20)
    }),
    "ispan": e("Ispaniya imperiyasi", EUROPE, "Dengiz / Oltin", "Madrid", ["Madrid", "Barselona", "Seviliya"], {
        "izabella": m("Izabella", "Ekspeditsiya", "gold", 1.30),
        "karl5": m("Karl V", "Soliq", "tax", 1.25),
        "filipp2": m("Filipp II", "Flot", "power", 1.25),
        "elcid": m("El Cid", "Jangovar ruh", "power", 1.20)
    }),
    "natsist_germaniya": e("Natsistlar Germaniyasi", EUROPE, "Blitskrig", "Berlin", ["Berlin", "Myunxen", "Gamburg"], {
        "gitler": m("Adolf Gitler", "Blitskrig +40%", "power", 1.40),
        "gebbels": m("Jozef Gebbels", "Targ'ibot", "gold", 1.25),
        "goring": m("Herman Goring", "Arzon qo'shin", "cost", 0.80),
        "gimmler": m("Genrix Gimmler", "Tartib", "tax", 1.30)
    }),
    "avstriya_vengriya": e("Avstriya-Vengriya", EUROPE, "Ko'p millatli", "Vena", ["Vena", "Budapesht", "Praga"], {
        "mariya": m("Mariya Tereziya", "Islohotlar", "tax", 1.25),
        "frants": m("Frants Yozef I", "Barqarorlik", "gold", 1.20),
        "yevgeniy": m("Yevgeniy Savoyskiy", "G'alabalar", "power", 1.30),
        "leopold": m("Leopold II", "Siyosat", "cost", 0.90)
    }),
    "sssr": e("SSSR", EUROPE, "Sanoat", "Moskva", ["Moskva", "Sankt-Peterburg", "Kiyev"], {
        "lenin": m("Vladimir Lenin", "Resurslar", "gold", 1.25),
        "stalin": m("Iosif Stalin", "Qizil armiya +40%", "power", 1.40),
        "xrushov": m("Nikita Xrushov", "Sanoat", "tax", 1.30),
        "brejnev": m("Leonid Brejnev", "Arzon qo'shin", "cost", 0.85)
    }),
    "vizantiya": e("Vizantiya imperiyasi", EUROPE, "Diplomatiya", "Konstantinopol", ["Konstantinopol", "Saloniki", "Trabzon"], {
        "yustinian": m("Yustinian I", "Qonunlar", "tax", 1.30),
        "konstantin_v": m("Konstantin", "Poytaxt", "gold", 1.25),
        "vasiliy": m("Vasiliy II", "Quvvat", "power", 1.30),
        "irakliy": m("Irakliy", "Xavfsizlik", "power", 1.15)
    }),
    "gon_sivar": e("Muqaddas Rim", EUROPE, "Diniy ta'sir", "Aaxen", ["Aaxen", "Frankfurt", "Vena"], {
        "otton": m("Otton I", "Qudrat", "power", 1.25),
        "barbarossa": m("Fridrix Barbarossa", "Hudud narxi", "cost", 0.80),
        "charlz5": m("Charlz V", "Soliq", "tax", 1.30),
        "genrix4": m("Genrix IV", "Barqarorlik", "gold", 1.20)
    }),

    # ANTIK VA OSIYO
    "mongol": e("Mo'g'ullar imperiyasi", ANTIK, "Tezkor yurish", "Qoraqurum", ["Qoraqurum", "Pekin", "Tabriz"], {
        "chingiz": m("Chingizxon", "Tezkor yurish +45%", "power", 1.45),
        "oqotay": m("O'qotay xon", "Boshqaruv", "tax", 1.30),
        "qubilay": m("Qubilay xon", "Savdo", "gold", 1.35),
        "huloku": m("Hulokuxon", "Bosqinchilik", "power", 1.35)
    }),
    "xunnu": e("Buyuk Xunnu", ANTIK, "Otliq qo'shin", "Utuken", ["Utuken", "Orxon", "Gobi"], {
        "modun": m("Modun Chanyu", "Otliqlar +35%", "power", 1.35),
        "laoshang": m("Lao-shang", "Kengayish", "cost", 0.85),
        "gunlu": m("Gunlu", "Quvvat", "power", 1.20),
        "hohanxie": m("Ho-han-xie", "Barqarorlik", "tax", 1.15)
    }),
    "qadimgi_xitoy": e("Sin imperiyasi", ANTIK, "Devor qurilishi", "Sian", ["Sian", "Pekin", "Shanxay"], {
        "sinshi": m("Sin Shi Huang", "Aholi solig'i", "tax", 1.40),
        "xanvudi": m("Xan Vu-di", "Ipak yo'li", "gold", 1.30),
        "taytsun": m("Taytsun", "Oltin davr", "tax", 1.35),
        "suyvendi": m("Suy Vendi", "Birlik", "cost", 0.85)
    }),
    "fors_ahamoniylar": e("Ahamoniylar", ANTIK, "Shoh yo'li", "Persepol", ["Persepol", "Susa", "Bobil"], {
        "kir2": m("Kir II", "Bagrikenglik", "tax", 1.30),
        "doro1": m("Doro I", "Logistika", "cost", 0.80),
        "kserks": m("Kserks I", "Armiya quvvati", "power", 1.25),
        "artakserks": m("Artakserks I", "Barqarorlik", "gold", 1.20)
    }),
    "qadimgi_misr": e("Qadimgi Misr", ANTIK, "Obidalar", "Memfis", ["Memfis", "Fiva", "Aleksandriya"], {
        "ramses": m("Ramses II", "Obidalar", "power", 1.30),
        "tutmos": m("Tutmos III", "Kengayish", "cost", 0.75),
        "kleopatra": m("Kleopatra", "Xazina", "gold", 1.30),
        "exnaton": m("Exnaton", "Madaniyat", "tax", 1.20)
    }),
    "makedoniya": e("Makedoniya imperiyasi", ANTIK, "Tezkor", "Pella", ["Pella", "Bobil", "Aleksandriya"], {
        "filipp2_m": m("Filipp II", "Falanga", "power", 1.25),
        "aleksandr": m("Aleksandr", "Saltanat +50%", "power", 1.50),
        "antigon": m("Antigon I", "Nazorat", "cost", 0.85),
        "polemey": m("Polemey I", "Ilm va xazina", "gold", 1.30)
    }),
    "karfagen": e("Karfagen imperiyasi", ANTIK, "Dengiz floti", "Karfagen", ["Karfagen", "Utika", "Gades"], {
        "gannibal": m("Gannibal", "Taktika +40%", "power", 1.40),
        "hamilkar": m("Hamilkar", "Dengiz va quruqlik", "power", 1.30),
        "magon": m("Magon", "Soliq", "tax", 1.25),
        "dido": m("Dido", "Poytaxt xazinasi", "gold", 1.20)
    }),
    "yaponiya": e("Tokugava shogunati", ANTIK, "Samuraylar", "Edo", ["Edo", "Kioto", "Osaka"], {
        "tokugava": m("Tokugava", "Intizom", "tax", 1.30),
        "nobunaga": m("Oda Nobunaga", "Islohotlar", "power", 1.35),
        "toyotomi": m("Toyotomi", "Birlik", "cost", 0.85),
        "miyamoto": m("Miyamoto", "Mahorat", "power", 1.20)
    }),
    "turk_xoqonligi": e("Buyuk Turk xoqonligi", ANTIK, "Dasht", "Suyob", ["Suyob", "Otuken", "Beshbaliq"], {
        "bumin": m("Bumin Xoqon", "Qudrat", "power", 1.35),
        "istami": m("Istami Yabg'u", "Ipak yo'li", "gold", 1.30),
        "tardu": m("Tardu", "Kengayish", "cost", 0.80),
        "bilga": m("Bilga Xoqon", "Soliq", "tax", 1.30)
    }),
}

PROVINCES = {
    "anadolu": {"name": "Anadolu yarimoroli", "cost": 10_000_000, "power_required": 30},
    "xuroson": {"name": "Xuroson hududi", "cost": 15_000_000, "power_required": 70},
    "mesopotamiya": {"name": "Mesopotamiya", "cost": 20_000_000, "power_required": 120},
    "sharqiy_yevropa": {"name": "Sharqiy Yevropa", "cost": 25_000_000, "power_required": 200},
    "hindiston": {"name": "Hindiston vodiysi", "cost": 30_000_000, "power_required": 300},
}

TROOPS = {
    "piyoda": {"name": "Piyoda askarlar", "cost": 1_000_000, "power": 10},
    "otliq": {"name": "Saralangan otliqlar", "cost": 3_000_000, "power": 35},
    "qamal": {"name": "Qamal qurollari", "cost": 7_000_000, "power": 90},
}

user_game_data = {}


# ----------------------------------------------------------------------
# Render uchun Health Check Veb-Serveri
# ----------------------------------------------------------------------
class HealthHandler(BaseHTTPRequestHandler):
    def _reply(self, send_body=True):
        body = b"Bot is running!"
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if send_body:
            self.wfile.write(body)

    def do_GET(self):
        self._reply()

    def do_HEAD(self):
        self._reply(send_body=False)

    def log_message(self, format, *args):
        pass


def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = ThreadingHTTPServer(("0.0.0.0", port), HealthHandler)
    server.serve_forever()


# ----------------------------------------------------------------------
# Bot Handlerlari
# ----------------------------------------------------------------------
@bot.message_handler(commands=["start"])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("🕌 Sharq va Islom olami", callback_data="cat_Sharq va Islom olami"),
        types.InlineKeyboardButton("🌍 Yevropa va Jahon", callback_data="cat_Yevropa va Jahon"),
        types.InlineKeyboardButton("⚔️ Antik va Osiyo", callback_data="cat_Antik va Osiyo"),
    )
    bot.reply_to(
        message,
        "Salom! Sivilizatsiya o'yiniga xush kelibsiz.\nQuyidagi kategoriyalardan birini tanlang:",
        reply_markup=markup,
    )


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
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f"📂 **{cat_name}** kategoriyasidagi imperiyalar:",
            reply_markup=markup,
            parse_mode="Markdown",
        )

    elif call.data == "back_to_cats":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🕌 Sharq va Islom olami", callback_data="cat_Sharq va Islom olami"),
            types.InlineKeyboardButton("🌍 Yevropa va Jahon", callback_data="cat_Yevropa va Jahon"),
            types.InlineKeyboardButton("⚔️ Antik va Osiyo", callback_data="cat_Antik va Osiyo"),
        )
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Salom! Sivilizatsiya o'yiniga xush kelibsiz.\nQuyidagi kategoriyalardan birini tanlang:",
            reply_markup=markup,
            parse_mode="Markdown",
        )

    elif call.data.startswith("select_"):
        emp_key = call.data.split("_", 1)[1]
        emp = EMPIRES[emp_key]

        markup = types.InlineKeyboardMarkup(row_width=1)
        for m_key, m_val in emp["monarchs"].items():
            markup.add(types.InlineKeyboardButton(f"👑 {m_val['name']} — ({m_val['desc']})", callback_data=f"monarch_{emp_key}_{m_key}"))
        markup.add(types.InlineKeyboardButton("🔙 Orqaga", callback_data=f"cat_{emp['group']}"))

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f"✅ **Sizning tanlovingiz:** {emp['name']}\n\nEndi imperiyangiz uchun **Buyuk Qirolni** tanlang:",
            reply_markup=markup,
            parse_mode="Markdown",
        )

    elif call.data.startswith("monarch_"):
        parts = call.data.split("_", 2)
        emp_key = parts[1]
        monarch_key = parts[2]
        emp = EMPIRES[emp_key]
        monarch = emp["monarchs"][monarch_key]

        initial_gold = emp["gold"]
        if monarch["type"] == "gold":
            initial_gold = int(initial
