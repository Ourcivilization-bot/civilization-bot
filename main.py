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
        "cities": ["Samarqand", "Buxoro", "Hirot"],
        "monarchs": {
            "timur": {"name": "Amir Timur", "desc": "Harbiy quvvat +25%", "type": "power", "val": 1.25},
            "shohrux": {"name": "Shohrux Mirzo", "desc": "Soliq daromadi +20%", "type": "tax", "val": 1.20},
            "ulugbek": {"name": "Mirzo Ulug‘bek", "desc": "Qo'shin narxi -15%", "type": "cost", "val": 0.85},
            "husayn": {"name": "Husayn Boyqaro", "desc": "Xazina o'sishi +20%", "type": "gold", "val": 1.20}
        }
    },
    "omaviylar": {
        "name": "Omaviylar xalifaligi",
        "group": "Sharq va Islom olami",
        "specialization": "Diplomatiya / Kengayish",
        "gold": 100_000_000,
        "capital": "Damashq",
        "cities": ["Damashq", "Kufa", "Basra"],
        "monarchs": {
            "muoviya": {"name": "Muoviya I", "desc": "Diplomatiya va kengayish", "type": "cost", "val": 0.90},
            "abdulmalik": {"name": "Abdulmalik ibn Marvon", "desc": "Soliqlar +30%", "type": "tax", "val": 1.30},
            "valid": {"name": "Valid I", "desc": "Zabt etish kuchi -10%", "type": "power", "val": 1.10},
            "umar2": {"name": "Umar II", "desc": "Adolat va xazina", "type": "gold", "val": 1.20}
        }
    },
    "abbosiylar": {
        "name": "Abbosiylar xalifaligi",
        "group": "Sharq va Islom olami",
        "specialization": "Ilm-fan / Madaniyat",
        "gold": 100_000_000,
        "capital": "Bagdod",
        "cities": ["Bagdod", "Qohira", "Basra"],
        "monarchs": {
            "horun": {"name": "Horun ar-Rashid", "desc": "Xazina va oltin +30%", "type": "gold", "val": 1.30},
            "mamun": {"name": "Al-Ma’mun", "desc": "Qo'shinlar narxi -10%", "type": "cost", "val": 0.90},
            "mansur": {"name": "Al-Mansur", "desc": "Soliq daromadi +20%", "type": "tax", "val": 1.20},
            "mutasim": {"name": "Al-Mu'tasim", "desc": "Armiya kuchi +15%", "type": "power", "val": 1.15}
        }
    },
    "usmonlilar": {
        "name": "Usmonlilar imperiyasi",
        "group": "Sharq va Islom olami",
        "specialization": "Harbiy / Dengiz floti",
        "gold": 100_000_000,
        "capital": "Istanbul",
        "cities": ["Istanbul", "Edirne", "Bursa"],
        "monarchs": {
            "osman": {"name": "Osman I", "desc": "Asoschilik bonusi", "type": "gold", "val": 1.15},
            "mehmed": {"name": "Fotih Sulton Mehmed", "desc": "Qamal qurollari kuchi +30%", "type": "power", "val": 1.30},
            "sulaymon": {"name": "Sulaymon Qonuniy", "desc": "Hudud zabt narxi -20%", "type": "cost", "val": 0.80},
            "boyazid": {"name": "Yildirim Boyazid", "desc": "Tezkor hujum va kuch +25%", "type": "power", "val": 1.25}
        }
    },
    "ayyubiylar": {
        "name": "Ayyubiylar sulolasi",
        "group": "Sharq va Islom olami",
        "specialization": "Harbiy / Himoya",
        "gold": 100_000_000,
        "capital": "Qohira",
        "cities": ["Qohira", "Aleppo", "Damashq"],
        "monarchs": {
            "salohiddin": {"name": "Salohiddin Ayyubi", "desc": "Harbiy quvvat +25%", "type": "power", "val": 1.25},
            "adil": {"name": "Al-Adil", "desc": "Iqtisod va soliq +20%", "type": "tax", "val": 1.20},
            "komil": {"name": "Al-Komil", "desc": "Hudud narxi -15%", "type": "cost", "val": 0.85},
            "nosir": {"name": "An-Nosir Yusuf", "desc": "Otliq kuchlari +20%", "type": "power", "val": 1.20}
        }
    },
    "xorazmshohlar": {
        "name": "Xorazmshohlar davlati",
        "group": "Sharq va Islom olami",
        "specialization": "Savdo / Kengayish",
        "gold": 100_000_000,
        "capital": "Kunya-Urganch",
        "cities": ["Urganch", "Gurlan", "Marv", "Samarqand"],
        "monarchs": {
            "anushtegin": {"name": "Anushtegin G‘archa", "desc": "Soliq o'sishi +10%", "type": "tax", "val": 1.10},
            "otsiz": {"name": "Otsiz Xorazmshoh", "desc": "Hudud narxi -15%", "type": "cost", "val": 0.85},
            "muhammad": {"name": "Alouddin Muhammad II", "desc": "Armiya kuchi +20%", "type": "power", "val": 1.20},
            "jaloliddin": {"name": "Jaloliddin Manguberdi", "desc": "Qahramonlik quvvati +35%", "type": "power", "val": 1.35}
        }
    },
    "gaznaviylar": {
        "name": "Gaznaviylar davlati",
        "group": "Sharq va Islom olami",
        "specialization": "Harbiy / Bosqinchilik",
        "gold": 100_000_000,
        "capital": "Gazna",
        "cities": ["Gazna", "Lahor", "Balx"],
        "monarchs": {
            "sabuqtigin": {"name": "Sabuqtigin", "desc": "Xazina o'sishi +15%", "type": "gold", "val": 1.15},
            "mahmud": {"name": "Mahmud G‘aznaviy", "desc": "Oltin topish +30%", "type": "tax", "val": 1.30},
            "masud": {"name": "Mas’ud I", "desc": "Otliq kuchlari +20%", "type": "power", "val": 1.20},
            "ibrohim": {"name": "Ibrohim Gaznaviy", "desc": "Barqarorlik va soliq +15%", "type": "tax", "val": 1.15}
        }
    },
    "safaviylar": {
        "name": "Safaviylar imperiyasi",
        "group": "Sharq va Islom olami",
        "specialization": "Madaniyat / Savdo",
        "gold": 100_000_000,
        "capital": "Isfahon",
        "cities": ["Isfahon", "Tebriz", "Sheroz"],
        "monarchs": {
            "ismoil": {"name": "Shoh Ismoil I", "desc": "Harbiy shijoat +25%", "type": "power", "val": 1.25},
            "abbos": {"name": "Shoh Abbos I Buyuk", "desc": "Savdo va soliq +30%", "type": "tax", "val": 1.30},
            "tahmosib": {"name": "Tahmosib I", "desc": "Himoya va quvvat", "type": "power", "val": 1.15},
            "husayn_s": {"name": "Sulton Husayn", "desc": "Madaniyat va oltin", "type": "gold", "val": 1.20}
        }
    },
    "boburiylar": {
        "name": "Boburiylar imperiyasi",
        "group": "Sharq va Islom olami",
        "specialization": "Arxitektura / Boylik",
        "gold": 100_000_000,
        "capital": "Dehli",
        "cities": ["Dehli", "Agra", "Lahor"],
        "monarchs": {
            "bobur": {"name": "Zahriddin Muhammad Bobur", "desc": "Harbiy taktika +25%", "type": "power", "val": 1.25},
            "akbar": {"name": "Akbarshoh", "desc": "Soliq daromadi +30%", "type": "tax", "val": 1.30},
            "jahon": {"name": "Shoh Jahon", "desc": "Xazina o'sishi +25%", "type": "gold", "val": 1.25},
            "avrangzeb": {"name": "Avrangzeb", "desc": "Hudud narxi -20%", "type": "cost", "val": 0.80}
        }
    },
    "oltin_orda": {
        "name": "Oltin Orda",
        "group": "Sharq va Islom olami",
        "specialization": "Kochmanchi qudrati / Soliq",
        "gold": 100_000_000,
        "capital": "Saroy-Bot",
        "cities": ["Saroy-Bot", "Qozon", "Astraxan"],
        "monarchs": {
            "botu": {"name": "Botuxon", "desc": "Soliq yig'ish +35%", "type": "tax", "val": 1.35},
            "beraka": {"name": "Berakaxon", "desc": "Savdo va iqtisod +20%", "type": "gold", "val": 1.20},
            "uzbek": {"name": "O‘zbekxon", "desc": "Madaniyat va barqarorlik", "type": "tax", "val": 1.20},
            "toxtamish": {"name": "To‘xtamishxon", "desc": "Tezkor hujum +20%", "type": "power", "val": 1.20}
        }
    },
    "shayboniylar": {
        "name": "Shayboniylar sulolasi",
        "group": "Sharq va Islom olami",
        "specialization": "Dasht qudrati / Mintaqa",
        "gold": 100_000_000,
        "capital": "Samarqand",
        "cities": ["Samarqand", "Buxoro", "Toshkent", "Balkh"],
        "monarchs": {
            "abulxayr": {"name": "Abulxayrxon", "desc": "Dasht qudrati +25%", "type": "power", "val": 1.25},
            "shayboniy": {"name": "Muhammad Shayboniyxon", "desc": "Mintaqani birlashtirish +35%", "type": "power", "val": 1.35},
            "ubaydulla": {"name": "Ubaydullaxon", "desc": "Markaziy boshqaruv solig'i +30%", "type": "tax", "val": 1.30},
            "abdulla2": {"name": "Abdullaxon II", "desc": "Hudud kengaytirish -20%", "type": "cost", "val": 0.80}
        }
    },
    "buxoro_amirligi": {
        "name": "Buxoro amirligi",
        "group": "Sharq va Islom olami",
        "specialization": "Ilm-fan / Diniy markaz",
        "gold": 100_000_000,
        "capital": "Buxoro",
        "cities": ["Buxoro", "Samarqand", "Qarshi"],
        "monarchs": {
            "rahimxon_b": {"name": "Muhammad Rahimxon", "desc": "Amirlik asosi +25%", "type": "power", "val": 1.25},
            "shohmurod": {"name": "Shohmurod (Amir Mas’um)", "desc": "Adolatli siyosat +30%", "type": "tax", "val": 1.30},
            "haydar": {"name": "Amir Haydar", "desc": "Madaniyat va ilm-fan +20%", "type": "gold", "val": 1.20},
            "olimxon": {"name": "Said Olimxon", "desc": "Qiyin davrdagi mudofaa +25%", "type": "power", "val": 1.25}
        }
    },
    "xiva_xonligi": {
        "name": "Xiva xonligi",
        "group": "Sharq va Islom olami",
        "specialization": "Voha / Qo'shin shijoati",
        "gold": 100_000_000,
        "capital": "Xiva",
        "cities": ["Xiva", "Urganch", "Gurlan"],
        "monarchs": {
            "olloquli": {"name": "Olloqulixon", "desc": "Ichan qal'a obidalari +30%", "type": "gold", "val": 1.30},
            "rahimxon2": {"name": "Muhammad Rahimxon II (Firouz)", "desc": "Ma'rifat va qudrat +35%", "type": "tax", "val": 1.35},
            "isfandiyor": {"name": "Isfandiyorxon", "desc": "Islohotlar va soliqlar +20%", "type": "tax", "val": 1.20},
            "junaid": {"name": "Junaidxon", "desc": "Qat'iy qarshilik va shijoat +30%", "type": "power", "val": 1.30}
        }
    },
    "qoqon_xonligi": {
        "name": "Qo‘qon xonligi",
        "group": "Sharq va Islom olami",
        "specialization": "Vodiy savdosi / Markazlashuv",
        "gold": 100_000_000,
        "capital": "Qo‘qon",
        "cities": ["Qo‘qon", "Namangan", "Andijon", "O‘sh"],
        "monarchs": {
            "norbotabiy": {"name": "Norbo‘tabiy", "desc": "Dehqonchilik va xazina +25%", "type": "gold", "val": 1.25},
            "olimxon_q": {"name": "Olimxon", "desc": "Markazlashgan armiya +30%", "type": "power", "val": 1.30},
            "madalixon": {"name": "Muhammad Aminxon (Madalixon)", "desc": "Savdo yo'llari yuksalishi +35%", "type": "tax", "val": 1.35},
            "xudoyorxon": {"name": "Xudoyorxon", "desc": "Saroy arxitekturasi +25%", "type": "gold", "val": 1.25}
        }
    },
    "salibchilar": {
        "name": "Salibchilar (Quddus qirolligi)",
        "group": "Sharq va Islom olami",
        "specialization": "Ritsarlar / Himoya",
        "gold": 100_000_000,
        "capital": "Quddus",
        "cities": ["Quddus", "Antioxiya", "Akkon"],
        "monarchs": {
            "gotfrid": {"name": "Gotfrid Bulonskiy", "desc": "Asoschilik kuchi +25%", "type": "power", "val": 1.25},
            "baldvin4": {"name": "Baldvin IV", "desc": "Iroda va mudofaa +30%", "type": "power", "val": 1.30},
            "richard": {"name": "Richard Sheryurak", "desc": "Afsonaviy jangovar quvvat +40%", "type": "power", "
