import os
import requests
import datetime
import telebot
from telebot import types

# Telegram bot token va AccuWeather API kalitini muhit o'zgaruvchilardan olish
TOKEN = os.getenv("8168027431:AAEep52n4U9pP65eTZmO09LnuUqN5wION04")
API_KEY = os.getenv("n9Nd7iseF4VOZthNyg1Ilho2kvAewhSr")

# Telegram botini ishga tushurish
bot = telebot.TeleBot(TOKEN)

# Viloyatlar va ularning AccuWeather location kodlari
locations = {
    "Andijon": "349727",
    "Buxoro": "123456",
    "Fargʻona": "789012",
    "Jizzax": "345678",
    "Namangan": "567890",
    "Navoiy": "678901",
    "Qashqadaryo": "890123",
    "Qoraqalpogʻiston Respublikasi": "901234",
    "Samarqand": "234567",
    "Sirdaryo": "345789",
    "Surxondaryo": "456890",
    "Toshkent": "567123",
    "Xorazm": "678234"
}

# Botning start komandasiga javob berish
@bot.message_handler(commands=["start"])
def start(message):
    # Salomlashish va hudud tanlash uchun tugmalar
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    for region in locations.keys():
        markup.add(types.KeyboardButton(region))
    
    bot.send_message(
        message.chat.id,
        "Salom!👋\nBot Shakhzod Norkobilov tomonidan ishlab chiqilgan!👨🏻‍💻\nMurojaat uchun: @shakhzod_norkobilov ✍️\n\nHududni tanlang:",
        reply_markup=markup
    )

# Foydalanuvchi hududni tanlaganida ob-havo ma'lumotini olish
@bot.message_handler(func=lambda message: message.text in locations)
def get_weather(message):
    region = message.text
    location_code = locations[region]
    url = f"http://dataservice.accuweather.com/forecasts/v1/daily/5day/{location_code}?apikey={API_KEY}&language=uz-uz&metric=true"

    # API dan ma'lumot olish
    response = requests.get(url)
    
    # Agar API javobi muvaffaqiyatli bo'lsa
    if response.status_code == 200:
        try:
            data = response.json()
            forecast = f"📍 *{region}* hududining 5 kunlik ob-havo ma'lumoti:\n\n"

            # 5 kunlik ob-havo ma'lumotlarini chiqarish
            for day in data['DailyForecasts']:
                date = datetime.datetime.strptime(day['Date'], "%Y-%m-%dT%H:%M:%S%z").strftime("%d-%b, %A")
                min_temp = day['Temperature']['Minimum']['Value']
                max_temp = day['Temperature']['Maximum']['Value']
                condition = day['Day']['IconPhrase']

                forecast += f"📅 *{date}*\n🌡 {min_temp}°C - {max_temp}°C\n🌥 {condition}\n\n"

            # Foydalanuvchiga ob-havo ma'lumotlarini yuborish
            bot.send_message(message.chat.id, forecast, parse_mode="Markdown")
        except Exception as e:
            bot.send_message(message.chat.id, f"❌ Xatolik yuz berdi: {str(e)}")
    else:
        bot.send_message(message.chat.id, f"❌ Ob-havo ma'lumotlarini olishda xatolik yuz berdi. Xatolik kodi: {response.status_code}")

# Botni ishga tushurish
bot.polling(none_stop=True)
