import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Loggingni sozlash
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Flask ilovasini yaratish (Telegram Mini App bilan muloqot uchun)
app = Flask(__name__)
CORS(app)  # CORS xatolarining oldini olish uchun

# Bot tokeningizni shu yerga yozasiz (yoki Render Environment Variables'dan o'qiydi)
TOKEN = os.getenv("BOT_TOKEN", "SIZNING_BOT_TOKENINGIZ")
WEB_APP_URL = "https://helpful-marshmallow-91609c.netlify.app"

# Vaqtinchalik o'yinchi bazasi (sinov uchun)
PLAYERS_DB = {
    123456789: {
        "player_name": "Amir Temur",
        "monarch_name": "Sohibqiron",
        "empire_name": "Turon Sivilizatsiyasi",
        "gold": 50000,
        "total_power": 12500,
        "conquered": ["Samarqand", "Buxoro", "Xorazm"]
    }
}

@app.route(f'/api/user/<int:user_id>', methods=['GET'])
def get_user_data(user_id):
    """Mini App uchun foydalanuvchi ma'lumotlarini qaytaruvchi API"""
    user_data = PLAYERS_DB.get(user_id)
    if not user_data:
        # Agar foydalanuvchi bazada bo'lmasa, standart qiymat qaytaramiz
        return jsonify({
            "player_name": "Hokim",
            "monarch_name": "Imperator",
            "empire_name": "Yangi Sivilizatsiya",
            "gold": 1000,
            "total_power": 500,
            "conquered": []
        })
    return jsonify(user_data)

@app.route('/')
def home():
    return "Sivilizatsiya Bot Backend ishlayapti!"

# Telegram Bot /start buyrug'i
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    # Agar foydalanuvchi bazada bo'lmasa, uni qo'shamiz
    if user.id not in PLAYERS_DB:
        PLAYERS_DB[user.id] = {
            "player_name": user.first_name or "Hokim",
            "monarch_name": "Buyuk Hukmdor",
            "empire_name": f"{user.first_name} Imperiyasi",
            "gold": 2500,
            "total_power": 1200,
            "conquered": ["Poytaxt"]
        }

    # Mini App ochish uchun tugma
    keyboard = [[
        InlineKeyboardButton(
            "🚀 Sivilizatsiyani Boshqarish", 
            web_app=WebAppInfo(url=WEB_APP_URL)
        )
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"Salom, <b>{user.first_name}</b>! Sivilizatsiya strategiya o'yiniga xush kelibsiz.\n\n"
        "Imperiyangizni boshqarish va xazinangizni ko'rish uchun quyidagi tugmani bosing:",
        reply_markup=reply_markup,
        parse_mode="HTML"
    )

def main():
    # Telegram botni sozlash
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    
    # Pollingni ishga tushirish
    print("Bot ishga tushdi...")
    application.run_polling()

if __name__ == '__main__':
    # Render muhitida Flask va Botni birga ishlatish uchun portni sozlaymiz
    port = int(os.environ.get('PORT', 5000))
    # Eslatma: Render orqali botni to'liq ishlatish uchun Webhook yoki threading ishlatish kerak bo'ladi, 
    # agar oddiy run_polling ishlatayotgan bo'lsangiz Render'da background worker sifatida ochganingiz maqbul.
    app.run(host='0.0.0.0', port=port)
