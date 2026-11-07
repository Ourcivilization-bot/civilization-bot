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
            "shohmurod": _monarch("Shohmurod", "Adolatli siyosat +30%", "tax", 1.30),
            "haydar": _monarch("Amir Haydar", "Madaniyat va ilm-fan +20%", "gold", 1.20),
            "olimxon": _monarch("Said Olimxon", "Qiyin davrdagi mudofaa +25%", "power", 1.25),
        },
    ),
    "xiva_xonligi": _empire(
        "Xiva xonligi", EAST, "Voha / Qo'shin shijoati", "Xiva",
        ["Xiva", "Urganch", "Gurlan"],
        {
            "olloquli": _monarch("Olloqulixon", "Ichan qal'a obidalari +30%", "gold", 1.30),
            "rahimxon2": _monarch("Muhammad Rahimxon II", "Ma'rifat va qudrat +35%", "tax", 1.35),
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
            "madalixon": _monarch("Madalixon", "Savdo yo'llari yuksalishi +35%", "tax", 1.35),
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
            "sezar": _monarch("Yuliy Sezar
