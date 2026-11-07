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
    # ------------------------------------------------------------------
    # SHARQ VA ISLOM OLAMI
    # ------------------------------------------------------------------
    "temuriylar": e("Temuriylar imperiyasi", EAST, "Harbiy / Ilm-fan", "Samarqand", ["Samarqand", "Buxoro", "Hirot"], {
        "timur": m("Amir Timur", "Harbiy quvvat +25%", "power", 1.25),
        "shohrux": m("Shohrux Mirzo", "Soliq daromadi +20%", "tax", 1.20),
        "ulugbek": m("Mirzo Ulug'bek", "Qo'shin narxi -15%", "cost", 0.85),
        "husayn": m("Husayn Boyqaro", "Xazina o'sishi +20%", "gold", 1.20),
    }),
    "omaviylar": e("Omaviylar xalifaligi", EAST, "Diplomatiya / Kengayish", "Damashq", ["Damashq", "Kufa", "Basra"], {
        "muoviya": m("Muoviya I", "Diplomatiya va kengayish", "cost", 0.90),
        "abdulmalik": m("Abdulmalik ibn Marvon", "Soliqlar +30%", "tax", 1.30),
        "valid": m("Valid I", "Zabt etish kuchi -10%", "power", 1.10),
        "umar2": m("Umar II", "Adolat va xazina", "gold", 1.20),
    }),
    "abbosiylar": e("Abbosiylar xalifaligi", EAST, "Ilm-fan / Madaniyat", "Bagdod", ["Bagdod", "Qohira", "Basra"], {
        "horun": m("Horun ar-Rashid", "Xazina va oltin +30%", "gold", 1.30),
        "mamun": m("Al-Ma'mun", "Qo'shinlar narxi -10%", "cost", 0.90),
        "mansur": m("Al-Mansur", "Soliq daromadi +20%", "tax", 1.20),
        "mutasim": m("Al-Mu'tasim", "Armiya kuchi +15%", "power", 1.15),
    }),
    "usmonlilar": e("Usmonlilar imperiyasi", EAST, "Harbiy / Dengiz floti", "Istanbul", ["Istanbul", "Edirne", "Bursa"], {
        "osman": m("Osman I", "Asoschilik bonusi", "gold", 1.15),
        "mehmed": m("Fotih Sulton Mehmed", "Qamal qurollari +30%", "power", 1.30),
        "sulaymon": m("Sulaymon Qonuniy", "Zabt narxi -20%", "cost", 0.80),
        "boyazid": m("Yildirim Boyazid", "Tezkor hujum +25%", "power", 1.25),
    }),
    "ayyubiylar": e("Ayyubiylar sulolasi", EAST, "Harbiy / Himoya", "Qohira", ["Qohira", "Aleppo", "Damashq"], {
        "salohiddin": m("Salohiddin Ayyubi", "Harbiy quvvat +25%", "power", 1.25),
        "adil": m("Al-Adil", "Iqtisod va soliq +20%", "tax", 1.20),
        "komil": m("Al-Komil", "Hudud narxi -15%", "cost", 0.85),
        "nosir": m("An-Nosir Yusuf", "Otliq kuchlari +20%", "power", 1.20),
    }),
    "xorazmshohlar": e("Xorazmshohlar davlati", EAST, "Savdo / Kengayish", "Kunya-Urganch", ["Urganch", "Gurlan", "Marv", "Samarqand"], {
        "anushtegin": m("Anushtegin G'archa", "Soliq o'sishi +10%", "tax", 1.10),
        "otsiz": m("Otsiz Xorazmshoh", "Hudud narxi -15%", "cost", 0.85),
        "muhammad": m("Alouddin Muhammad II", "Armiya kuchi +20%", "power", 1.20),
        "jaloliddin": m("Jaloliddin Manguberdi", "Qahramonlik +35%", "power", 1.35),
    }),
    "gaznaviylar": e("Gaznaviylar davlati", EAST, "Harbiy / Bosqinchilik", "Gazna", ["Gazna", "Lahor", "Balx"], {
        "sabuqtigin": m("Sabuqtigin", "Xazina o'sishi +15%", "gold", 1.15),
        "mahmud": m("Mahmud G'aznaviy", "Oltin topish +30%", "tax", 1.30),
        "masud": m("Mas'ud I", "Otliq kuchlari +20%", "power", 1.20),
        "ibrohim": m("Ibrohim Gaznaviy", "Barqarorlik +15%", "tax", 1.15),
    }),
    "safaviylar": e("Safaviylar imperiyasi", EAST, "Madaniyat / Savdo", "Isfahon", ["Isfahon", "Tabriz", "Sheroz"], {
        "ismoil": m("Shoh Ismoil I", "Harbiy shijoat +25%", "power", 1.25),
        "abbos": m("Shoh Abbos I Buyuk", "Savdo va soliq +30%", "tax", 1.30),
        "tahmosib": m("Tahmasp I", "Himoya va quvvat", "power", 1.15),
        "husayn_s": m("Sulton Husayn", "Madaniyat va oltin", "gold", 1.20),
    }),
    "boburiylar": e("Boburiylar imperiyasi", EAST, "Arxitektura / Boylik", "Dehli", ["Dehli", "Agra", "Lahor"], {
        "bobur": m("Zahriddin Muhammad Bobur", "Harbiy taktika +25%", "power", 1.25),
        "akbar": m("Akbarshoh", "Soliq daromadi +30%", "tax", 1.30),
        "jahon": m("Shoh Jahon", "Xazina o'sishi +25%", "gold", 1.25),
        "avrangzeb": m("Avrangzeb", "Hudud narxi -20%", "cost", 0.80),
    }),
    "oltin_orda": e("Oltin Orda", EAST, "Ko'chmanchi qudrati / Soliq", "Saroy-Bot", ["Saroy-Bot", "Qozon", "Astraxan"], {
        "botu": m("Botuxon", "Soliq yig'ish +35%", "tax", 1.35),
        "beraka": m("Berakaxon", "Savdo va iqtisod +20%", "gold", 1.20),
        "uzbek": m("O'zbekxon", "Madaniyat va barqarorlik", "tax", 1.20),
        "toxtamish": m("To'xtamishxon", "Tezkor hujum +20%", "power", 1.20),
    }),
    "shayboniylar": e("Shayboniylar sulolasi", EAST, "Dasht qudrati / Mintaqa", "Samarqand", ["Samarqand", "Buxoro", "Toshkent", "Balx"], {
        "abulxayr": m("Abulxayrxon", "Dasht qudrati +25%", "power", 1.25),
        "shayboniy": m("Muhammad Shayboniyxon", "Mintaqani birlashtirish +35%", "power", 1.35),
        "ubaydulla": m("Ubaydullaxon", "Markaziy boshqaruv solig'i +30%", "tax", 1.30),
        "abdulla2": m("Abdullaxon II", "Hudud kengaytirish -20%", "cost", 0.80),
    }),
    "buxoro_amirligi": e("Buxoro amirligi", EAST, "Ilm-fan / Diniy markaz", "Buxoro", ["Buxoro", "Samarqand", "Qarshi"], {
        "rahimxon_b": m("Muhammad Rahimxon", "Amirlik asosi +25%", "power", 1.25),
        "shohmurod": m("Shohmurod", "Adolatli siyosat +30%", "tax", 1.30),
        "haydar": m("Amir Haydar", "Madaniyat va ilm-fan +20%", "gold", 1.20),
        "olimxon": m("Said Olimxon", "Qiyin davrdagi mudofaa +25%", "power", 1.25),
    }),
    "xiva_xonligi": e("Xiva xonligi", EAST, "Voha / Qo'shin shijoati", "Xiva", ["Xiva", "Urganch", "Gurlan"], {
        "olloquli": m("Olloqulixon", "Ichan qal'a obidalari +30%", "gold", 1.30),
        "rahimxon2": m("Muhammad Rahimxon II", "Ma'rifat va qudrat +35%", "tax", 1.35),
        "isfandiyor": m("Isfandiyorxon", "Islohotlar va soliqlar +20%", "tax", 1.20),
        "junaid": m("Junaidxon", "Qat'iy qarshilik va shijoat +30%", "power", 1.30),
    }),
    "qoqon_xonligi": e("Qo'qon xonligi", EAST, "Vodiy savdosi / Markazlashuv", "Qo'qon", ["Qo'qon", "Namangan", "Andijon", "O'sh"], {
        "norbotabiy": m("Norbo'tabiy", "Dehqonchilik va xazina +25%", "gold", 1.25),
        "olimxon_q": m("Olimxon", "Markazlashgan armiya +30%", "power", 1.30),
        "madalixon": m("Madalixon", "Savdo yo'llari yuksalishi +35%", "tax", 1.35),
        "xudoyorxon": m("Xudoyorxon", "Saroy arxitekturasi +25%", "gold", 1.25),
    }),
    "salibchilar": e("Salibchilar (Quddus qirolligi)", EAST, "Ritsarlar / Himoya", "Quddus", ["Quddus", "Antioxiya", "Akkon"], {
        "gotfrid": m("Gotfrid Bulonskiy", "Asoschilik kuchi +25%", "power", 1.25),
        "baldvin4": m("Baldvin IV", "Iroda va mudofaa +30%", "power", 1.30),
        "richard": m("Richard Sheryurak", "Afsonaviy jangovar quvvat +40%", "power", 1.40),
        "reno": m("Reno de Shatiyon", "Shijoat va soliq +20%", "tax", 1.20),
    }),

    # ------------------------------------------------------------------
    # YEVROPA VA JAHON
    # ------------------------------------------------------------------
    "britaniya": e("Britaniya imperiyasi", EUROPE, "Iqtisodiy / Savdo", "London", ["London", "Liverpul", "Edinburg"], {
        "elizaveta": m("Qirolicha Yelizaveta I", "Dengiz floti va savdo +30%", "gold", 1.30),
        "viktoriya": m("Qirolicha Viktoriya", "Global soliq +35%", "tax", 1.35),
        "cherchill": m("Uinston Cherchill", "Harbiy qat'iyat +25%", "power", 1.25),
        "genrix8": m("Genrix VIII", "Siyosiy ta'sir", "cost", 0.90),
    }),
    "rim": e("Rim imperiyasi", EUROPE, "Infratuzilma / Legionlar", "Rim", ["Rim", "Milano", "Afina"], {
        "sezar": m("Yuliy Sezar", "Legionlar kuchi +30%", "power", 1.30),
        "august": m("August Oktavian", "Infratuzilma va soliq +25%", "tax", 1.25),
        "trayan": m("Trayan", "Hudud zabt narxi -20%", "cost", 0.80),
        "konstantin_r": m("Buyuk Konstantin", "Barqarorlik va oltin", "gold", 1.20),
    }),
    "fransiya": e("Fransiya imperiyasi", EUROPE, "Diplomatiya / Madaniyat", "Parij", ["Parij", "Marsel", "Lion"], {
        "karl_buyuk": m("Karl Buyuk", "Imperiya qudrati +25%", "power", 1.25),
        "lyudovik": m("Lyudovik XIV", "Xazina va soliq +35%", "tax", 1.35),
        "napoleon": m("Napoleon Bonapart", "Harbiy strategiya +40%", "power", 1.40),
        "jovanni": m("Janna d'Ark", "Ma'naviy ruh +20%", "power", 1.20),
    }),
    "rossiya": e("Rossiya imperiyasi", EUROPE, "Hudud / Resurslar", "Sankt-Peterburg", ["Moskva", "Sankt-Peterburg", "Kiyev"], {
        "pyotr": m("Buyuk Pyotr", "Sanoat va flot +30%", "gold", 1.30),
        "yekaterina": m("Yekaterina II", "Hudud kengaytirish +35%", "cost", 0.65),
        "ivan": m("Ivan Grozniy", "Harbiy tazyiq +25%", "power", 1.25),
        "alex2": m("Aleksandr II", "Iqtisodiy o'sish", "tax", 1.20),
    }),
    "ispan": e("Ispaniya imperiyasi", EUROPE, "Dengiz sayohati / Oltin", "Madrid", ["Madrid", "Barselona", "Seviliya"], {
        "izabella": m("Katolik Izabella", "Ekspeditsiya va oltin +30%", "gold", 1.30),
        "karl5": m("Karl V", "Dunyo imperiyasi solig'i +25%", "tax", 1.25),
        "filipp2": m("Filipp II", "Dengiz floti qudrati +25%", "power", 1.25),
        "elcid": m("El Cid", "Jangovar ruh +20%", "power", 1.20),
    }),
    "natsist_germaniya": e("Natsistlar Germaniyasi", EUROPE, "Blitskrig / Sanoat", "Berlin", ["Berlin", "Myunxen", "Gamburg"], {
        "gitler": m("Adolf Gitler", "Blitskrig va armiya kuchi +40%", "power", 1.40),
        "gebbels": m("Jozef Gebbels", "Targ'ibot va xazina o'sishi +25%", "gold", 1.25),
        "goring": m("Herman Goring", "Harbiy sanoat va arzon qo'shin -20%", "cost", 0.80),
        "gimmler": m("Genrix Gimmler", "Ichki tartib va soliq +30%", "tax", 1.30),
    }),
    "avstriya_vengriya": e("Avstriya-Vengriya", EUROPE, "Ko'p millatli / Birlik", "Vena", ["Vena", "Budapesht", "Praga"], {
        "mariya": m("Mariya Tereziya", "Iqtisodiy islohotlar +25%", "tax", 1.25),
        "frants": m("Frants Yozef I", "Ko'p millatli barqarorlik", "gold", 1.20),
        "yevgeniy": m("Yevgeniy Savoyskiy", "Harbiy g'alabalar +30%", "power", 1.30),
        "leopold": m("Leopold II", "Tashqi siyosat", "cost", 0.90),
    }),
    "sssr": e("SSSR", EUROPE, "Sanoat / Qizil armiya", "Moskva", ["Moskva", "Sankt-Peterburg", "Kiyev"], {
        "lenin": m("Vladimir Lenin", "Inqilobiy ruh va resurslar +25%", "gold", 1.25),
        "stalin": m("Iosif Stalin", "Temir intizom va Qizil armiya +40%", "power", 1.40),
        "xrushov": m("Nikita Xrushov", "Sanoat va iqtisodiy o'sish +30%", "tax", 1.30),
        "brejnev": m("Leonid Brejnev", "Barqarorlik va arzon qo'shin -15%", "cost", 0.85),
    }),
    "vizantiya": e("Vizantiya imperiyasi", EUROPE, "Diplomatiya / Diniy markaz", "Konstantinopol", ["Konstantinopol", "Saloniki", "Trabzon"], {
        "yustinian": m("Yustinian I", "Qonunlar va soliq +30%", "tax", 1.30),
        "konstantin_v": m("Buyuk Konstantin", "Poytaxt qudrati +25%", "gold", 1.25),
        "vasiliy": m("Vasiliy II", "Harbiy quvvat +30%", "power", 1.30),
        "irakliy": m("Irakliy", "Chegaralar xavfsizligi", "power", 1.15),
    }),
    "gon_sivar": e("Muqaddas Rim imperiyasi", EUROPE, "Diniy ta'sir / Birlik", "Aaxen", ["Aaxen", "Frankfurt", "Vena"], {
        "otton": m("Otton I", "Imperatorlik qudrati +25%", "power", 1.25),
        "barbarossa": m("Fridrix I Barbarossa", "Hudud narxi -20%", "cost", 0.80),
        "charlz5": m("Charlz V", "Global soliq +30%", "tax", 1.30),
        "genrix4": m("Genrix IV", "Siyosiy barqarorlik", "gold", 1.20),
    }),

    # ------------------------------------------------------------------
    # ANTIK VA OSIYO
    # ------------------------------------------------------------------
    "mongol": e("Mo'g'ullar imperiyasi", ANTIK, "Tezkor yurish / Qo'shin", "Qoraqurum", ["Qoraqurum", "Pekin", "Tabriz"], {
        "chingiz": m("Chingizxon", "Tezkor yurish va kuch +45%", "power", 1.45),
        "oqotay": m("O'qotay xon", "Boshqaruv va soliq +30%", "tax", 1.30),
        "qubilay": m("Qubilay xon", "Savdo va boylik +35%", "gold", 1.35),
        "huloku": m("Hulokuxon", "Bosqinchilik quvvati +35%", "power", 1.35),
    }),
    "xunnu": e("Buyuk Xunnu imperiyasi", ANTIK, "Otliq qo'shin / Erkinlik", "Utuken", ["Utuken", "Orxon", "Gobi"], {
        "modun": m("Modun Chanyu", "Otliq qo'shinlar +35%", "power", 1.35),
        "laoshang": m("Lao-shang Chanyu", "Kengayish imkoniyati", "cost", 0.85),
        "gunlu": m("Gunlu", "Harbiy quvvat +20%", "power", 1.20),
        "hohanxie": m("Ho-han-xie", "Tashqi barqarorlik", "tax", 1.15),
    }),
    "qadimgi_xitoy": e("Sin imperiyasi (Xitoy)", ANTIK, "Aholi / Devor qurilishi", "Sian", ["Sian", "Pekin", "Shanxay"], {
        "sinshi": m("Sin Shi Huang", "Aholi solig'i +40%", "tax", 1.40),
        "xanvudi": m("Xan Vu-di", "Ipak yo'li oltini +30%", "gold", 1.30),
        "taytsun": m("Taytsun", "Oltin davr solig'i +35%", "tax", 1.35),
        "suyvendi": m("Suy Vendi", "Birlik bonusi", "cost", 0.85),
    }),
    "fors_ahamoniylar": e("Ahamoniylar imperiyasi (Fors)", ANTIK, "Logistika / Shoh yo'li", "Persepol", ["Persepol", "Susa", "Bobil"], {
        "kir2": m("Kir II Buyuk", "Bagrikenglik va soliq +30%", "tax", 1.30),
        "doro1": m("Doro I Buyuk", "Shoh yo'li logistikasi -20%", "cost", 0.80),
        "kserks": m("Kserks I", "Ulkan armiya quvvati +25%", "power", 1.25),
        "artakserks": m("Artakserks I", "Ichki barqarorlik", "gold", 1.20),
    }),
    "qadimgi_misr": e("Qadimgi Misr", ANTIK, "Obidalar / Nil daryosi", "Memfis", ["Memfis", "Fiva", "Aleksandriya"], {
        "ramses": m("Ramses II Buyuk", "Obidalar va quvvat +30%", "power", 1.30),
        "tutmos": m("Tutmos III", "Strategik kengayish +35%", "cost", 0.75),
        "kleopatra": m("Kleopatra VII", "Diplomatiya va xazina +30%", "gold", 1.30),
        "exnaton": m("Exnaton", "Madaniy rivojlanish", "tax", 1.20),
    }),
    "makedoniya": e("Makedoniya imperiyasi", ANTIK, "Aleksandr taktikasi / Tezkor", "Pella", ["Pella", "Bobil", "Aleksandriya"], {
        "filipp2_m": m("Filipp II", "Falanga taktikasi +25%", "power", 1.25),
        "aleksandr": m("Aleksandr Makedoniyali", "Jahon saltanati quvvati +50%", "power", 1.50),
        "antigon": m("Antigon I", "Hududiy nazorat", "cost", 0.85),
        "polemey": m("Polemey I", "Ilm va xazina +30%", "gold", 1.30),
    }),
    "karfagen": e("Karfagen imperiyasi", ANTIK, "Savdo / Dengiz floti", "Karfagen", ["Karfagen", "Utika", "Gades"], {
        "gannibal": m("Gannibal Barka", "Daho taktikasi +40%", "power", 1.40),
        "hamilkar": m("Hamilkar Barka", "Dengiz va quruqlik +30%", "power", 1.30),
        "magon": m("Magon Barka", "Savdo va soliq +25%", "tax", 1.25),
        "dido": m("Dido", "Poytaxt xazinasi +20%", "gold", 1.20),
    }),
    "yaponiya": e("Tokugava shogunati (Yaponiya)", ANTIK, "Samuraylar / Intizom", "Edo", ["Edo", "Kioto", "Osaka"], {
        "tokugava": m("Tokugava Iyeyasu", "Samuraylar intizomi +30%", "tax", 1.30),
        "nobunaga": m("Oda Nobunaga", "Harbiy islohotlar +35%", "power", 1.35),
        "toyotomi": m("Toyotomi Xideyoshi", "Hududiy birlashish", "cost", 0.85),
        "miyamoto": m("Miyamoto Musashi", "Jangovar mahorat +20%", "power", 1.20),
    }),
    "turk_xoqonligi": e("Buyuk Turk xoqonligi", ANTIK, "Chegarasiz dasht / Ittifoq", "Suyob", ["Suyob", "Otuken", "Beshbaliq"], {
        "bumin": m("Bumin Xoqon", "Xoqonlik qudrati +35%", "power", 1.35),
        "istami": m("Istami Yabg'u", "Ipak yo'li savdosi +30%", "gold", 1.30),
        "tardu": m("Tardu Xoqon", "Chegarasiz dasht kengayishi", "cost", 0.80),
        "bilga": m("Bilga Xoqon", "Madaniyat va soliq +30%", "tax", 1.30),
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
        parts = call.data.
