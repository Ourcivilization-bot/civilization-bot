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
        "specialization": "Arxitekt
