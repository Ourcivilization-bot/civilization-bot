import os
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import telebot
from telebot import types

# Render port talab qilgani uchun fon serveri
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

# --- 29 TA IMPERIYA (Guruhlarga bo'lingan holda) ---
EMPIRES = {
    # --- 1. SHARQ VA ISLOM OLAMI IMPERIYALARI ---
    "temuriylar": {
        "name": "Temuriylar imperiyasi",
        "group": "🕌 Sharq va Islom olami",
        "specialization": "Harbiy / Ilm-fan",
        "gold": 100_000_000,
        "capital": "Samarqand",
        "cities": ["Samarqand", "Buxoro", "Hirot"]
    },
    "omaviylar": {
        "name": "Omaviylar xalifaligi",
        "group": "🕌 Sharq va Islom olami",
        "specialization": "Diplomatiya / Kengayish",
        "gold": 100_000_000,
        "capital": "Damashq",
        "cities": ["Damashq", "Kufa", "Basra"]
    },
    "abbosiylar": {
        "name": "Abbosiylar xalifaligi",
        "group": "🕌 Sharq va Islom olami",
        "specialization": "Ilm-fan / Madaniyat",
        "gold": 100_000_000,
        "capital": "Bag‘dod",
        "cities": ["Bag‘dod", "Qohira", "Basra"]
    },
    "usmonlilar": {
        "name": "Usmonlilar imperiyasi",
        "group": "🕌 Sharq va Islom olami",
        "specialization": "Harbiy / Harbiy dengiz floti",
        "gold": 100_000_000,
        "capital": "Istanbul",
        "cities": ["Istanbul", "Edirne", "Bursa"]
    },
    "ayyubiylar": {
        "name": "Ayyubiylar sulolasi",
        "group": "🕌 Sharq va Islom olami",
        "specialization": "Harbiy / Himoya",
        "gold": 100_000_000,
        "capital": "Qohira",
        "cities": ["Qohira", "Aleppo", "Damashq"]
    },
    "xorazmshohlar": {
        "name": "Xorazmshohlar davlati",
        "group": "🕌 Sharq va Islom olami",
        "specialization": "Savdo / Kengayish",
        "gold": 100_000_000,
        "capital": "Kunya-Urganch",
        "cities": ["Urganch", "Gurlan", "Marv", "Samarqand"]
    },
    "gaznaviylar": {
        "name": "G‘aznaviylar davlati",
        "group": "🕌 Sharq va Islom olami",
        "specialization": "Harbiy / Bosqinchilik",
        "gold": 100_000_000,
        "capital": "G‘azna",
        "cities": ["G‘azna", "Lahor", "Balx"]
    },
    "safaviylar": {
        "name": "Safaviylar imperiyasi",
        "group": "🕌 Sharq va Islom olami",
        "specialization": "Madaniyat / Savdo",
        "gold": 100_000_000,
        "capital": "Isfahon",
        "cities": ["Isfahon", "Tebriz", "Sheroz"]
    },
    "boburiylar": {
        "name": "Boburiylar imperiyasi",
        "group": "🕌 Sharq va Islom olami",
        "specialization": "Arxitektura / Boylik",
        "gold": 100_000_000,
        "capital": "Dehli",
        "cities": ["Dehli", "Agra", "Lahor"]
    },
    "oltin_orda": {
        "name": "Oltin Oʻrda",
        "group": "🕌 Sharq va Islom olami",
        "specialization": "Ko‘chmanchi qudrati / Soliq",
        "gold": 100_000_000,
        "capital": "Saroy-Bot",
        "cities": ["Saroy-Bot", "Qozon", "Astraxan"]
    },

    # --- 2. YEVROPA VA JAHON IMPERIYALARI ---
    "britaniya": {
        "name": "Britaniya imperiyasi",
        "group": "🌍 Yevropa va Jahon",
        "specialization": "Iqtisodiy / Savdo",
        "gold": 100_000_000,
        "capital": "London",
        "cities": ["London", "Liverpul", "Edinburg"]
    },
    "rim": {
        "name": "Rim imperiyasi",
        "group": "🌍 Yevropa va Jahon",
        "specialization": "Infratuzilma / Legionlar",
        "gold": 100_000_000,
        "capital": "Rim",
        "cities": ["Rim", "Milano", "Afina"]
    },
    "fransiya": {
        "name": "Fransiya imperiyasi",
        "group": "🌍 Yevropa va Jahon",
        "specialization": "Diplomatiya / Madaniyat",
        "gold": 100_000_000,
        "capital": "Parij",
        "cities": ["Parij", "Marsel", "Lion"]
    },
    "rossiya": {
        "name": "Rossiya imperiyasi",
        "group": "🌍 Yevropa va Jahon",
        "specialization": "Hudud / Resurslar",
        "gold": 100_000_000,
        "capital": "Sankt-Peterburg",
        "cities": ["Moskva", "Sankt-Peterburg", "Kiyev"]
    },
    "ispan": {
        "name": "Ispaniya imperiyasi",
        "group": "🌍 Yevropa va Jahon",
        "specialization": "Dengiz sayohati / Oltin",
        "gold": 100_000_000,
        "capital": "Madrid",
        "cities": ["Madrid", "Barselona", "Seviliya"]
    },
    "germaniya": {
        "name": "Germaniya imperiyasi",
        "group": "🌍 Yevropa va Jahon",
        "specialization": "Sanoat / Ilm-fan",
        "gold": 100_000_000,
        "capital": "Berlin",
        "cities": ["Berlin", "Myunxen", "Gamburg"]
    },
    "avstriya_vengriya": {
        "name": "Avstriya-Vengriya",
        "group": "🌍 Yevropa va Jahon",
        "specialization": "Ko‘pmillatli / Birlik",
        "gold": 100_000_000,
        "capital": "Vena",
        "cities": ["Vena", "Budapesht", "Praga"]
    },
    "shved": {
        "name": "Shved imperiyasi",
        "group": "🌍 Yevropa va Jahon",
        "specialization": "Harbiy taktika / Temir",
        "gold": 100_000_000,
        "capital": "Stokgolm",
        "cities": ["Stokgolm", "Gteborg", "Malmo"]
    },
    "vizantiya": {
        "name": "Vizantiya imperiyasi",
        "group": "🌍 Yevropa va Jahon",
        "specialization": "Diplomatiya / Diniy markaz",
        "gold": 100_000_000,
        "capital": "Konstantinopol",
        "cities": ["Konstantinopol", "Saloniki", "Trabzon"]
    },
    "gon_sivar": {
        "name": "Muqaddas Rim imperiyasi",
        "group": "🌍 Yevropa va Jahon",
        "specialization": "Diniy ta'sir / Birlik",
        "gold": 100_000_000,
        "capital": "Aaxen",
        "cities": ["Aaxen", "Frankfurt", "Vyana"]
    },

    # --- 3. ANTIK VA OSIYO SIVILIZATSIYALARI ---
    "mongol": {
        "name": "Mo‘g‘ullar imperiyasi",
        "group": "⚔️ Antik va Osiyo",
        "specialization": "Tezkor yurish
