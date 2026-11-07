"""Civilization - Telegram strategiya o'yini boti."""

import os
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import telebot
from telebot import types  # noqa: F401  (o'yin tugmalari uchun kerak bo'ladi)

# ----------------------------------------------------------------------
# Imperiyalar va hukmdorlar ma'lumotlari
# Hukmdor turlari: power - harbiy quvvat, tax - soliq, cost - narx
# (kamroq = yaxshi), gold - xazina o'sishi
# ----------------------------------------------------------------------
START_GOLD = 100_000_000

EAST = "Sharq va Islom olami"
EUROPE = "Yevropa va Jahon"
ANTIK = "Antik va Osiyo"


def _monarch(name, desc, type_, val):
    return {"name": name, "desc": desc, "type": type_, "val": val}


def _empire(name, group, specialization, capital, cities, monarchs):
    return {
        "name": name,
        "group": group,
        "specialization": specialization,
        "gold": START_GOLD,
        "capital": capital,
        "cities": cities,
        "monarchs": monarchs,
    }


EMPIRES = {
    # ------------------------------------------------------------------
    # SHARQ VA ISLOM OLAMI
    # ------------------------------------------------------------------
    "temuriylar": _empire(
        "Temuriylar imperiyasi", EAST, "Harbiy / Ilm-fan", "Samarqand",
        ["Samarqand", "Buxoro", "Hirot"],
        {
            "timur": _monarch("Amir Timur", "Harbiy quvvat +25%", "power", 1.25),
            "shohrux": _monarch("Shohrux Mirzo", "Soliq daromadi +20%", "tax", 1.20),
            "ulugbek": _monarch("Mirzo Ulug'bek", "Qo'shin narxi -15%", "cost", 0.85),
            "husayn": _monarch("Husayn Boyqaro", "Xazina o'sishi +20%", "gold", 1.20),
        },
    ),
    "omaviylar": _empire(
        "Omaviylar xalifaligi", EAST, "Diplomatiya / Kengayish", "Damashq",
        ["Damashq", "Kufa", "Basra"],
        {
            "muoviya": _monarch("Muoviya I", "Diplomatiya va kengayish", "cost", 0.90),
            "abdulmalik": _monarch("Abdulmalik ibn Marvon", "Soliqlar +30%", "tax", 1.30),
            "valid": _monarch("Valid I", "Zabt etish kuchi -10%", "power", 1.10),
            "umar2": _monarch("Umar II", "Adolat va xazina", "gold", 1.20),
        },
    ),
    "abbosiylar": _empire(
        "Abbosiylar xalifaligi", EAST, "Ilm-fan / Madaniyat", "Bagdod",
        ["Bagdod", "Qohira", "Basra"],
        {
            "horun": _monarch("Horun ar-Rashid", "Xazina va oltin +30%", "gold", 1.30),
            "mamun": _monarch("Al-Ma'mun", "Qo'shinlar narxi -10%", "cost", 0.90),
            "mansur": _monarch("Al-Mansur", "Soliq daromadi +20%", "tax", 1.20),
            "mutasim": _monarch("Al-Mu'tasim", "Armiya kuchi +15%", "power", 1.15),
        },
    ),
    "usmonlilar": _empire(
        "Usmonlilar imperiyasi", EAST, "Harbiy / Dengiz floti", "Istanbul",
        ["Istanbul", "Edirne", "Bursa"],
        {
            "osman": _monarch("Osman I", "Asoschilik bonusi", "gold", 1.15),
            "mehmed": _monarch("Fotih Sulton Mehmed", "Qamal qurollari kuchi +30%", "power", 1.30),
            "sulaymon": _monarch("Sulaymon Qonuniy", "Hudud zabt narxi -20%", "cost", 0.80),
            "boyazid": _monarch("Yildirim Boyazid", "Tezkor hujum va kuch +25%", "power", 1.25),
        },
    ),
    "ayyubiylar": _empire(
        "Ayyubiylar sulolasi", EAST, "Harbiy / Himoya", "Qohira",
        ["Qohira", "Aleppo", "Damashq"],
        {
            "salohiddin": _monarch("Salohiddin Ayyubi", "Harbiy quvvat +25%", "power", 1.25),
            "adil": _monarch("Al-Adil", "Iqtisod va soliq +20%", "tax", 1.20),
            "komil": _monarch("Al-Komil", "Hudud narxi -15%", "cost", 0.85),
            "nosir": _monarch("An-Nosir Yusuf", "Otliq kuchlari +20%", "power", 1.20),
        },
    ),
    "xorazmshohlar": _empire(
        "Xorazmshohlar davlati", EAST, "Savdo / Kengayish", "Kunya-Urganch",
        ["Urganch", "Gurlan", "Marv", "Samarqand"],
        {
            "anushtegin": _monarch("Anushtegin G'archa", "Soliq o'sishi +10%", "tax", 1.10),
            "otsiz": _monarch("Otsiz Xorazmshoh", "Hudud narxi -15%", "cost", 0.85),
            "muhammad": _monarch("Alouddin Muhammad II", "Armiya kuchi +20%", "power", 1.20),
            "jaloliddin": _monarch("Jaloliddin Manguberdi", "Qahramonlik quvvati +35%", "power", 1.35),
        },
    ),
    "gaznaviylar": _empire(
        "Gaznaviylar davlati", EAST, "Harbiy / Bosqinchilik", "Gazna",
        ["Gazna", "Lahor", "Balx"],
        {
            "sabuqtigin": _monarch("Sabuqtigin", "Xazina o'sishi +15%", "gold", 1.15),
            "mahmud": _monarch("Mahmud G'aznaviy", "Oltin topish +30%", "tax", 1.30),
            "masud": _monarch("Mas'ud I", "Otliq kuchlari +20%", "power", 1.20),
            "ibrohim": _monarch("Ibrohim Gaznaviy", "Barqarorlik va soliq +15%", "tax", 1.15),
        },
    ),
    "safaviylar": _empire(
        "Safaviylar imperiyasi", EAST, "Madaniyat / Savdo", "Isfahon",
        ["Isfahon", "Tabriz", "Sheroz"],
        {
            "ismoil": _monarch("Shoh Ismoil I", "Harbiy shijoat +25%", "power", 1.25),
            "abbos": _monarch("Shoh Abbos I Buyuk", "Savdo va soliq +30%", "tax", 1.30),
            "tahmosib": _monarch("Tahmasp I", "Himoya va quvvat", "power", 1.15),
            "husayn_s": _monarch("Sulton Husayn", "Madaniyat va oltin", "gold", 1.20),
        },
    ),
    "boburiylar": _empire(
        "Boburiylar imperiyasi", EAST, "Arxitektura / Boylik", "Dehli",
        ["Dehli", "Agra", "Lahor"],
        {
            "bobur": _monarch("Zahriddin Muhammad Bobur", "Harbiy taktika +25%", "power", 1.25),
            "akbar": _monarch("Akbarshoh", "Soliq daromadi +30%", "tax", 1.30),
            "jahon": _monarch("Shoh Jahon", "Xazina o'sishi +25%", "gold", 1.25),
            "avrangzeb": _monarch("Avrangzeb", "Hudud narxi -20%", "cost", 0.80),
        },
    ),
    "oltin_orda": _empire(
        "Oltin Orda", EAST, "Ko'chmanchi qudrati / Soliq", "Saroy-Bot",
        ["Saroy-Bot", "Qozon", "Astraxan"],
        {
            "botu": _monarch("Botuxon", "Soliq yig'ish +35%", "tax", 1.35),
            "beraka": _monarch("Berakaxon", "Savdo va iqtisod +20%", "gold", 1.20),
            "uzbek": _monarch("O'zbekxon", "Madaniyat va barqarorlik", "tax", 1.20),
            "toxtamish": _monarch("To'xtamishxon", "Tezkor hujum +20%", "power", 1.20),
        },
    ),
    "shayboniylar": _empire(
        "Shayboniylar sulolasi", EAST, "Dasht qudrati / Mintaqa", "Samarqand",
        ["Samarqand", "Buxoro", "Toshkent", "Balx"],
        {
            "abulxayr": _monarch("Abulxayrxon", "Dasht qudrati +25%", "power", 1.25),
            "shayboniy": _monarch("Muhammad Shayboniyxon", "Mintaqani birlashtirish +35%", "power", 1.35),
            "ubaydulla": _monarch("Ubaydullaxon", "Markaziy boshqaruv solig'i +30%", "tax", 1.30),
            "abdulla2": _monarch("Abdullaxon II", "Hudud kengaytirish -20%", "cost", 0.80),
        },
    ),
    "buxoro_amirligi": _empire(
        "Buxoro amirligi", EAST, "Ilm-fan / Diniy markaz", "Buxoro",
        ["Buxoro", "Samarqand", "Qarshi"],
        {
            "rahimxon_b": _monarch("Muhammad Rahimxon", "Amirlik asosi +25%", "power", 1.25),
            "shohmurod": _monarch("Shohmurod (Amir Ma'sum)", "Adolatli siyosat +30%", "tax", 1.30),
            "haydar": _monarch("Amir Haydar", "Madaniyat va ilm-fan +20%", "gold", 1.20),
            "olimxon": _monarch("Said Olimxon", "Qiyin davrdagi mudofaa +25%", "power", 1.25),
        },
    ),
    "xiva_xonligi": _empire(
        "Xiva xonligi", EAST, "Voha / Qo'shin shijoati", "Xiva",
        ["Xiva", "Urganch", "Gurlan"],
        {
            "olloquli": _monarch("Olloqulixon", "Ichan qal'a obidalari +30%", "gold", 1.30),
            "rahimxon2": _monarch("Muhammad Rahimxon II (Feruz)", "Ma'rifat va qudrat +35%", "tax", 1.35),
            "isfandiyor": _monarch("Isfandiyorxon", "Islohotlar va soliqlar +20%", "tax", 1.20),
            "junaid": _monarch("Junaidxon", "Qat'iy qarshilik va shijoat +30%", "power", 1.30),
        },
    ),
    "qoqon_xonligi": _empire(
        "Qo'qon xonligi", EAST, "Vodiy savdosi / Markazlashuv", "Qo'qon",
        ["Qo'qon", "Namangan", "Andijon", "O'sh"],
        {
            "norbotabiy": _monarch("Norbo'tabiy", "Dehqonchilik va xazina +25%", "gold", 1.25),
            "olimxon_q": _monarch("Olimxon", "Markazlashgan armiya +30%", "power", 1.30),
            "madalixon": _monarch("Muhammad Aminxon (Madalixon)", "Savdo yo'llari yuksalishi +35%", "tax", 1.35),
            "xudoyorxon": _monarch("Xudoyorxon", "Saroy arxitekturasi +25%", "gold", 1.25),
        },
    ),
    "salibchilar": _empire(
        "Salibchilar (Quddus qirolligi)", EAST, "Ritsarlar / Himoya", "Quddus",
        ["Quddus", "Antioxiya", "Akkon"],
        {
            "gotfrid": _monarch("Gotfrid Bulonskiy", "Asoschilik kuchi +25%", "power", 1.25),
            "baldvin4": _monarch("Baldvin IV", "Iroda va mudofaa +30%", "power", 1.30),
            "richard": _monarch("Richard Sheryurak", "Afsonaviy jangovar quvvat +40%", "power", 1.40),
            "reno": _monarch("Reno de Shatiyon", "Shijoat va soliq +20%", "tax", 1.20),
        },
    ),

    # ------------------------------------------------------------------
    # YEVROPA VA JAHON
    # ------------------------------------------------------------------
    "britaniya": _empire(
        "Britaniya imperiyasi", EUROPE, "Iqtisodiy / Savdo", "London",
        ["London", "Liverpul", "Edinburg"],
        {
            "elizaveta": _monarch("Qirolicha Yelizaveta I", "Dengiz floti va savdo +30%", "gold", 1.30),
            "viktoriya": _monarch("Qirolicha Viktoriya", "Global soliq +35%", "tax", 1.35),
            "cherchill": _monarch("Uinston Cherchill", "Harbiy qat'iyat +25%", "power", 1.25),
            "genrix8": _monarch("Genrix VIII", "Siyosiy ta'sir", "cost", 0.90),
        },
    ),
    "rim": _empire(
        "Rim imperiyasi", EUROPE, "Infratuzilma / Legionlar", "Rim",
        ["Rim", "Milano", "Afina"],
        {
            "sezar": _monarch("Yuliy Sezar", "Legionlar kuchi +30%", "power", 1.30),
            "august": _monarch("August Oktavian", "Infratuzilma va soliq +25%", "tax", 1.25),
            "trayan": _monarch("Trayan", "Hudud zabt narxi -20%", "cost", 0.80),
            "konstantin_r": _monarch("Buyuk Konstantin", "Barqarorlik va oltin", "gold", 1.20),
        },
    ),
    "fransiya": _empire(
        "Fransiya imperiyasi", EUROPE, "Diplomatiya / Madaniyat", "Parij",
        ["Parij", "Marsel", "Lion"],
        {
            "karl_buyuk": _monarch("Karl Buyuk", "Imperiya qudrati +25%", "power", 1.25),
            "lyudovik": _monarch("Lyudovik XIV", "Xazina va soliq +35%", "tax", 1.35),
            "napoleon": _monarch("Napoleon Bonapart", "Harbiy strategiya +40%", "power", 1.40),
            "jovanni": _monarch("Janna d'Ark", "Ma'naviy ruh +20%", "power", 1.20),
        },
    ),
    "rossiya": _empire(
        "Rossiya imperiyasi", EUROPE, "Hudud / Resurslar", "Sankt-Peterburg",
        ["Moskva", "Sankt-Peterburg", "Kiyev"],
        {
            "pyotr": _monarch("Buyuk Pyotr", "Sanoat va flot +30%", "gold", 1.30),
            "yekaterina": _monarch("Yekaterina II", "Hudud kengaytirish +35%", "cost", 0.65),
            "ivan": _monarch("Ivan Grozniy", "Harbiy tazyiq +25%", "power", 1.25),
            "alex2": _monarch("Aleksandr II", "Iqtisodiy o'sish", "tax", 1.20),
        },
    ),
    "ispan": _empire(
        "Ispaniya imperiyasi", EUROPE, "Dengiz sayohati / Oltin", "Madrid",
        ["Madrid", "Barselona", "Seviliya"],
        {
            "izabella": _monarch("Katolik Izabella", "Ekspeditsiya va oltin +30%", "gold", 1.30),
            "karl5": _monarch("Karl V", "Dunyo imperiyasi solig'i +25%", "tax", 1.25),
            "filipp2": _monarch("Filipp II", "Dengiz floti qudrati +25%", "power", 1.25),
            "elcid": _monarch("El Cid", "Jangovar ruh +20%", "power", 1.20),
        },
    ),
    "natsist_germaniya": _empire(
        "Natsistlar Germaniyasi", EUROPE, "Blitskrig / Sanoat", "Berlin",
        ["Berlin", "Myunxen", "Gamburg"],
        {
            "gitler": _monarch("Adolf Gitler", "Blitskrig va armiya kuchi +40%", "power", 1.40),
            "gebbels": _monarch("Jozef Gebbels", "Targ'ibot va xazina o'sishi +25%", "gold", 1.25),
            "goring": _monarch("Herman Goring", "Harbiy sanoat va arzon qo'shin -20%", "cost", 0.80),
            "gimmler": _monarch("Genrix Gimmler", "Ichki tartib va soliq +30%", "tax", 1.30),
        },
    ),
    "avstriya_vengriya": _empire(
        "Avstriya-Vengriya", EUROPE, "Ko'p millatli / Birlik", "Vena",
        ["Vena", "Budapesht", "Praga"],
        {
            "mariya": _monarch("Mariya Tereziya", "Iqtisodiy islohotlar +25%", "tax", 1.25),
            "frants": _monarch("Frants Yozef I", "Ko'p millatli barqarorlik", "gold", 1.20),
            "yevgeniy": _monarch("Yevgeniy Savoyskiy", "Harbiy g'alabalar +30%", "power", 1.30),
            "leopold": _monarch("Leopold II", "Tashqi siyosat", "cost", 0.90),
        },
    ),
    "sssr": _empire(
        "SSSR", EUROPE, "Sanoat / Qizil armiya", "Moskva",
        ["Moskva", "Sankt-Peterburg", "Kiyev"],
        {
            "lenin": _monarch("Vladimir Lenin", "Inqilobiy ruh va resurslar +25%", "gold", 1.25),
            "stalin": _monarch("Iosif Stalin", "Temir intizom va Qizil armiya +40%", "power", 1.40),
            "xrushov": _monarch("Nikita Xrushov", "Sanoat va iqtisodiy o'sish +30%", "tax", 1.30),
            "brejnev": _monarch("Leonid Brejnev", "Barqarorlik va arzon qo'shin -15%", "cost", 0.85),
        },
    ),
    "vizantiya": _empire(
        "Vizantiya imperiyasi", EUROPE, "Diplomatiya / Diniy markaz", "Konstantinopol",
        ["Konstantinopol", "Saloniki", "Trabzon"],
        {
            "yustinian": _monarch("Yustinian I", "Qonunlar va soliq +30%", "tax", 1.30),
            "konstantin_v": _monarch("Buyuk Konstantin", "Poytaxt qudrati +25%", "gold", 1.25),
            "vasiliy": _monarch("Vasiliy II", "Harbiy quvvat +30%", "power", 1.30),
            "irakliy": _monarch("Irakliy", "Chegaralar xavfsizligi", "power", 1.15),
        },
    ),
    "gon_sivar": _empire(
        "Muqaddas Rim imperiyasi", EUROPE, "Diniy ta'sir / Birlik", "Aaxen",
        ["Aaxen", "Frankfurt", "Vena"],
        {
            "otton": _monarch("Otton I", "Imperatorlik qudrati +25%", "power", 1.25),
            "barbarossa": _monarch("Fridrix I Barbarossa", "Hudud narxi -20%", "cost", 0.80),
            "charlz5": _monarch("Charlz V", "Global soliq +30%", "tax", 1.30),
            "genrix4": _monarch("Genrix IV", "Siyosiy barqarorlik", "gold", 1.20),
        },
    ),

    # ------------------------------------------------------------------
    # ANTIK VA OSIYO
    # ------------------------------------------------------------------
    "mongol": _empire(
        "Mo'g'ullar imperiyasi", ANTIK, "Tezkor yurish / Qo'shin", "Qoraqurum",
        ["Qoraqurum", "Pekin", "Tabriz"],
        {
            "chingiz": _monarch("Chingizxon", "Tezkor yurish va kuch +45%", "power", 1.45),
            "oqotay": _monarch("O'qotay xon", "Boshqaruv va soliq +30%", "tax", 1.30),
            "qubilay": _monarch("Qubilay xon", "Savdo va boylik +35%", "gold", 1.35),
            "huloku": _monarch("Hulokuxon", "Bosqinchilik quvvati +35%", "power", 1.35),
        },
    ),
    "xunnu": _empire(
        "Buyuk Xunnu imperiyasi", ANTIK, "Otliq qo'shin / Erkinlik", "Utuken",
        ["Utuken", "Orxon", "Gobi"],
        {
            "modun": _monarch("Modun Chanyu", "Otliq qo'shinlar +35%", "power", 1.35),
            "laoshang": _monarch("Lao-shang Chanyu", "Kengayish imkoniyati", "cost", 0.85),
            "gunlu": _monarch("Gunlu", "Harbiy quvvat +20%", "power", 1.20),
            "hohanxie": _monarch("Ho-han-xie", "Tashqi barqarorlik", "tax", 1.15),
        },
    ),
    "qadimgi_xitoy": _empire(
        "Sin imperiyasi (Xitoy)", ANTIK, "Aholi / Devor qurilishi", "Sian",
        ["Sian", "Pekin", "Shanxay"],
        {
            "sinshi": _monarch("Sin Shi Huang", "Aholi solig'i +40%", "tax", 1.40),
            "xanvudi": _monarch("Xan Vu-di", "Ipak yo'li oltini +30%", "gold", 1.30),
            "taytsun": _monarch("Taytsun", "Oltin davr solig'i +35%", "tax", 1.35),
            "suyvendi": _monarch("Suy Vendi", "Birlik bonusi", "cost", 0.85),
        },
    ),
    "fors_ahamoniylar": _empire(
        "Ahamoniylar imperiyasi (Fors)", ANTIK, "Logistika / Shoh yo'li", "Persepol",
        ["Persepol", "Susa", "Bobil"],
        {
            "kir2": _monarch("Kir II Buyuk", "Bagrikenglik va soliq +30%", "tax", 1.30),
            "doro1": _monarch("Doro I Buyuk", "Shoh yo'li logistikasi -20%", "cost", 0.80),
            "kserks": _monarch("Kserks I", "Ulkan armiya quvvati +25%", "power", 1.25),
            "artakserks": _monarch("Artakserks I", "Ichki barqarorlik", "gold", 1.20),
        },
    ),
    "qadimgi_misr": _empire(
        "Qadimgi Misr", ANTIK, "Obidalar / Nil daryosi", "Memfis",
        ["Memfis", "Fiva", "Aleksandriya"],
        {
            "ramses": _monarch("Ramses II Buyuk", "Obidalar va quvvat +30%", "power", 1.30),
            "tutmos": _monarch("Tutmos III", "Strategik kengayish +35%", "cost", 0.75),
            "kleopatra": _monarch("Kleopatra VII", "Diplomatiya va xazina +30%", "gold", 1.30),
            "exnaton": _monarch("Exnaton", "Madaniy rivojlanish", "tax", 1.20),
        },
    ),
    "makedoniya": _empire(
        "Makedoniya imperiyasi", ANTIK, "Aleksandr taktikasi / Tezkor", "Pella",
        ["Pella", "Bobil", "Aleksandriya"],
        {
            "filipp2_m": _monarch("Filipp II", "Falanga taktikasi +25%", "power", 1.25),
            "aleksandr": _monarch("Aleksandr Makedoniyali", "Jahon saltanati quvvati +50%", "power", 1.50),
            "antigon": _monarch("Antigon I", "Hududiy nazorat", "cost", 0.85),
            "polemey": _monarch("Polemey I", "Ilm va xazina +30%", "gold", 1.30),
        },
    ),
    "karfagen": _empire(
        "Karfagen imperiyasi", ANTIK, "Savdo / Dengiz floti", "Karfagen",
        ["Karfagen", "Utika", "Gades"],
        {
            "gannibal": _monarch("Gannibal Barka", "Daho taktikasi +40%", "power", 1.40),
            "hamilkar": _monarch("Hamilkar Barka", "Dengiz va quruqlik +30%", "power", 1.30),
            "magon": _monarch("Magon Barka", "Savdo va soliq +25%", "tax", 1.25),
            "dido": _monarch("Dido", "Poytaxt xazinasi +20%", "gold", 1.20),
        },
    ),
    # DIQQAT: sizning faylingiz shu yerda kesilib qolgan edi (shahar ro'yxatidan
    # keyin). Quyidagi shahar va hukmdorlarni men taxminan to'ldirdim -
    # o'zingizdagi asl ma'lumot bilan almashtiring.
    "yaponiya": _empire(
        "Tokugava shogunati (Yaponiya)", ANTIK, "Samuraylar / Intizom", "Edo",
        ["Edo", "Kioto", "Osaka"],
        {
            "ieyasu": _monarch("Tokugava Iyeyasu", "Intizom va soliq +30%", "tax", 1.30),
            "nobunaga": _monarch("Oda Nobunaga", "Samuraylar kuchi +30%", "power", 1.30),
            "hideyoshi": _monarch("Toyotomi Xideyoshi", "Hudud zabt narxi -20%", "cost", 0.80),
            "iemitsu": _monarch("Tokugava Iyemitsu", "Xazina o'sishi +20%", "gold", 1.20),
        },
    ),
}


# Token KODDA YOZILMAYDI. Render'da Environment bo'limiga BOT_TOKEN nomi bilan
# qo'shiladi, kompyuterda esa: export BOT_TOKEN="..."
TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN:
    sys.exit("XATO: BOT_TOKEN topilmadi. Uni muhit o'zgaruvchisi sifatida kiriting.")

bot = telebot.TeleBot(TOKEN)


# ----------------------------------------------------------------------
# Render uchun kichik veb-server (Render portni ochiq ko'rishi shart)
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

    def do_HEAD(self):  # UptimeRobot kabi xizmatlar HEAD yuboradi
        self._reply(send_body=False)

    def log_message(self, format, *args):  # keraksiz loglarni o'chiradi
        pass


def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = ThreadingHTTPServer(("0.0.0.0", port), HealthHandler)
    server.serve_forever()


# ----------------------------------------------------------------------
# Bot buyruqlari
# ----------------------------------------------------------------------
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        f"Civilization o'yiniga xush kelibsiz!\nMavjud imperiyalar: {len(EMPIRES)} ta.",
    )


# >>> O'yinning qolgan buyruqlari (imperiya tanlash, urush, diplomatiya va h.k.)
# >>> shu yerga qo'shiladi.


# ----------------------------------------------------------------------
# Ishga tushirish
# ----------------------------------------------------------------------
if __name__ == "__main__":
    threading.Thread(target=run_server, daemon=True).start()
    bot.remove_webhook()  # eski webhook bo'lsa, polling bilan to'qnashmasin
    print("Bot ishga tushdi...")
    bot.infinity_polling(skip_pending=True, timeout=20, long_polling_timeout=20)
