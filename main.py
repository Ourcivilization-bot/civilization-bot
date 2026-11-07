import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Dispatcher, CommandHandler

# Loggingni sozlash
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Flask ilovasini yaratish
app = Flask(__name__)
CORS(app)

TOKEN = os.getenv("BOT_TOKEN", "SIZNING_BOT_TOKENINGIZ")
WEB_APP_URL = "https://helpful-marshmallow-91609c.netlify.app"
RENDER_URL = "https://civilization-bot-4.onrender.com"

# Vaqtinchalik o'yinchi bazasi
PLAYERS_DB = {}

# Bot va Dispatcher yaratish (v13 sintaksisi)
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot, None, use_context=True)

def start(update, context):
    user = update.effective_user
    if user.id not in PLAYERS_DB:
        PLAYERS_DB[user.id] = {
            "player_name": user.first_name or "Hokim",
            "monarch_name": "Buyuk Hukmdor",
            "empire_name": f"{user.first_name} Imperiyasi",
            "gold": 2500,
            "total_power": 1200,
            "conquered": ["Poytaxt"]
        }

    keyboard = [[
        InlineKeyboardButton(
            "🚀 Sivilizatsiyani Boshqarish", 
            web_app=WebAppInfo(url=WEB_APP_URL)
        )
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        f"Salom, <b>{user.first_name}</b>! Sivilizatsiya strategiya o'yiniga xush kelibsiz.\n\n"
        "Imperiyangizni boshqarish va xazinangizni ko'rish uchun quyidagi tugmani bosing:",
        reply_markup=reply_markup,
        parse_mode="HTML"
    )

dispatcher.add_handler(CommandHandler("start", start))

@app.route(f'/api/user/<int:user_id>', methods=['GET'])
def get_user_data(user_id):
    user_data = PLAYERS_DB.get(user_id)
    if not user_data:
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
    return "Sivilizatsiya Bot Backend va Webhook ishlayapti!"

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    """Telegramdan keladigan xabarlarni qabul qilish"""
    json_str = request.get_data().decode('UTF-8')
    update = Update.de_json(json_str, bot)
    dispatcher.process_update(update)
    return "OK", 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    
    # Webhookni Telegramga ulaymiz
    webhook_url = f"{RENDER_URL}/{TOKEN}"
    bot.set_webhook(url=webhook_url)
    
    app.run(host='0.0.0.0', port=port)
