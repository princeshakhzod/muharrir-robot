import telebot
import requests
from datetime import datetime

# Telegram bot token va AccuWeather API kalitini o'rnatish
TOKEN = "8168027431:AAEep52n4U9pP65eTZmO09LnuUqN5wION04"
API_KEY = "n9Nd7iseF4VOZthNyg1Ilho2kvAewhSr"

bot = telebot.TeleBot(TOKEN)

# Viloyatlar ro'yxati
regions = [
    "Andijon", "Buxoro", "Fargʻona", "Jizzax", "Namangan", 
    "Navoiy", "Qashqadaryo", "Qoraqalpogʻiston Respublikasi", 
    "Samarqand", "Sirdaryo", "Surxondaryo", "Toshkent", "Xorazm"
]

# Shahar nomini qidirish uchun funksiya
def get_location_key(city_name):
    url = f"http://dataservice.accuweather.com/locations/v1/cities/search?apikey={API_KEY}&q={city_name}&language=en-us"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if len(data) > 0:
            return data[0]["Key"]
        else:
            return None  # Agar shahar topilmasa, None qaytarish
    else:
        print(f"Error: {response.status_code}")  # Xatolik haqida ma'lumot
        return None

# 5 kunlik ob-havo prognozini olish
def get_weather_forecast(location_key):
    url = f"http://dataservice.accuweather.com/forecasts/v1/daily/5day/{location_key}?apikey={API_KEY}&language=en-us"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        forecast = []
        for day in data['DailyForecasts']:
            forecast.append({
                'date': datetime.utcfromtimestamp(day['Date']/1000).strftime('%Y-%m-%d'),
                'min_temp': day['Temperature']['Minimum']['Value'],
                'max_temp': day['Temperature']['Maximum']['Value'],
                'weather': day['Day']['IconPhrase']
            })
        return forecast
    else:
        print(f"Error: {response.status_code}")  # Xatolik haqida ma'lumot
        return None

# Start komandasiga javob berish
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Salom!👋\nBot Shakhzod Norkobilov tomonidan ishlab chiqilgan!👨🏻‍💻\nMurojaat uchun: @shakhzod_norkobilov ✍️\n\nHududni tanlang:")
    
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for region in regions:
        markup.add(region)
    bot.send_message(message.chat.id, "Hududni tanlang", reply_markup=markup)

# Foydalanuvchi viloyat tanlasa
@bot.message_handler(func=lambda message: message.text in regions)
def send_forecast(message):
    region = message.text.strip().title()  # Foydalanuvchidan kiritilgan matnni tozalash va titullarni o'zgartirish
    location_key = get_location_key(region)
    
    if location_key:
        forecast_data = get_weather_forecast(location_key)
        if forecast_data:
            forecast_text = f"{region} viloyati uchun 5 kunlik ob-havo prognozi:\n\n"
            for day in forecast_data:
                forecast_text += f"{day['date']} - Min: {day['min_temp']}°C, Max: {day['max_temp']}°C, Weather: {day['weather']}\n"
            bot.send_message(message.chat.id, forecast_text)
        else:
            bot.send_message(message.chat.id, "Ob-havo ma'lumotlarini olishda xatolik yuz berdi. Keyinroq urinib ko'ring.")
    else:
        bot.send_message(message.chat.id, "Shahar topilmadi. Iltimos, to'g'ri shahar nomini kiriting.")

# Botni ishga tushirish
bot.polling()
