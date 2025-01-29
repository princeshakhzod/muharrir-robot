import telebot
import requests
from datetime import datetime

# Telegram bot token va AccuWeather API key
API_KEY = "n9Nd7iseF4VOZthNyg1Ilho2kvAewhSr"  # AccuWeather API kalitini shu yerga kiriting
TOKEN = "8168027431:AAEep52n4U9pP65eTZmO09LnuUqN5wION04"  # Telegram bot tokenini shu yerga kiriting

bot = telebot.TeleBot(TOKEN)

# Foydalanuvchi tomonidan tanlangan viloyatga qarab Location Key olish
def get_location_key(city_name):
    url = f"http://dataservice.accuweather.com/locations/v1/cities/search?apikey={API_KEY}&q={city_name}&language=en-us"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if len(data) > 0:
            return data[0]["Key"]
    return None

# 5 kunlik ob-havo prognozini olish
def get_weather_forecast(location_key):
    url = f"http://dataservice.accuweather.com/forecasts/v1/daily/5day/{location_key}?apikey={API_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        forecast_data = response.json()
        weather_data = []
        for day in forecast_data["DailyForecasts"]:
            date = datetime.strptime(day["Date"], "%Y-%m-%dT%H:%M:%SZ").strftime("%d-%m-%Y")
            min_temp = day["Temperature"]["Minimum"]["Value"]
            max_temp = day["Temperature"]["Maximum"]["Value"]
            weather = day["Day"]["IconPhrase"]
            weather_data.append({"date": date, "min_temp": min_temp, "max_temp": max_temp, "weather": weather})
        return weather_data
    return None

# /start buyrug'i uchun
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=3)
    buttons = ["Andijon", "Buxoro", "Fargʻona", "Jizzax", "Namangan", "Navoiy", 
               "Qashqadaryo", "Qoraqalpogʻiston Respublikasi", "Samarqand", 
               "Sirdaryo", "Surxondaryo", "Toshkent", "Xorazm"]
    markup.add(*buttons)
    
    bot.send_message(message.chat.id, "Salom!👋 Bot Shakhzod Norkobilov tomonidan ishlab chiqilgan!👨🏻‍💻 Murojaat uchun: @shakhzod_norkobilov ✍️\n\nHududni tanlang", reply_markup=markup)

# Foydalanuvchi hududni tanlaganda ob-havo ma'lumotlarini chiqarish
@bot.message_handler(func=lambda message: True)
def send_weather(message):
    city_name = message.text
    location_key = get_location_key(city_name)
    
    if location_key:
        forecast_data = get_weather_forecast(location_key)
        if forecast_data:
            forecast_text = "5 kunlik ob-havo prognozi:\n\n"
            for day in forecast_data:
                forecast_text += f"{day['date']} - Min: {day['min_temp']}°C, Max: {day['max_temp']}°C, Weather: {day['weather']}\n"
            bot.send_message(message.chat.id, forecast_text)
        else:
            bot.send_message(message.chat.id, "Ob-havo ma'lumotlarini olishda xatolik yuz berdi. Keyinroq urinib ko'ring.")
    else:
        bot.send_message(message.chat.id, "Shahar topilmadi. Iltimos, to'g'ri shahar nomini kiriting.")

bot.polling()
