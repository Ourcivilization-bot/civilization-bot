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
    "rim": e("Rim imper
