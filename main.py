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

# ----------------------------------------------------------------------
# MA'LUMOTLAR BAZASINI SOZLASH (SQLITE)
# ----------------------------------------------------------------------
def init_db():
    conn = sqlite3.connect('game.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            user_id INTEGER PRIMARY KEY,
            player_name TEXT,
            empire TEXT,
            monarch TEXT,
            gold INTEGER,
            conquered TEXT,
            army_piyoda INTEGER,
            army_otliq INTEGER,
            army_qamal INTEGER,
            total_power INTEGER,
            last_tax_time REAL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alliances (
            user_id_1 INTEGER,
            user_id_2 INTEGER
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def get_db():
    return sqlite3.connect('game.db', check_same_thread=False)

def get_user_data(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT player_name, empire, monarch, gold, conquered, "
        "army_piyoda, army_otliq, army_qamal, total_power, last_tax_time "
        "FROM players WHERE user_id = ?", (user_id,)
    )
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "player_name": row[0],
            "empire": row[1],
            "monarch": row[2],
            "gold": row[3],
            "conquered": row[4].split(",") if row[4] else [],
            "army": {
                "piyoda": row[5],
                "otliq": row[6],
                "qamal": row[7]
            },
            "total_power": row[8],
            "last_tax_time": row[9]
        }
    return None

def save_user_data(user_id, data):
    conn = get_db()
    cursor = conn.cursor()
    conquered_str = ",".join(data["conquered"])
    cursor.execute('''
        INSERT OR REPLACE INTO players 
        (user_id, player_name, empire, monarch, gold, conquered, 
         army_piyoda, army_otliq, army_qamal, total_power, last_tax_time)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        user_id,
        data["player_name"],
        data["empire"],
        data["monarch"],
        data["gold"],
        conquered_str,
        data["army"]["piyoda"],
        data["army"]["otliq"],
        data["army"]["qamal"],
        data["total_power"],
        data["last_tax_time"]
    ))
    conn.commit()
    conn.close()

def get_all_users():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT user_id, player_name, empire, monarch, gold, conquered, "
        "army_piyoda, army_otliq, army_qamal, total_power, last_tax_time "
        "FROM players"
    )
    rows = cursor.fetchall()
    conn.close()
    users = {}
    for row in rows:
        users[row[0]] = {
            "player_name": row[1],
            "empire": row[2],
            "monarch": row[3],
            "gold": row[4],
            "conquered": row[5].split(",") if row[5] else [],
            "army": {
                "piyoda": row[6],
                "otliq": row[7],
                "qamal": row[8]
            },
            "total_power": row[9],
            "last_tax_time": row[10]
        }
    return users
# ----------------------------------------------------------------------

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
        "ramses": m("Ramses II", "Ob
