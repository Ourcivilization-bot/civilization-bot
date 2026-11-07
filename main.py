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
    "shayboniylar": e("Shayboniylar sulolasi", EAST, "Dasht qudrati / Mintaqa", "Samarqand", ["Samarqand
