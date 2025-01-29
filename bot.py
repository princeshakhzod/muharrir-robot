import telebot
import requests
import datetime

# Telegram bot tokenini shu yerga kiriting
TOKEN = "8168027431:AAEep52n4U9pP65eTZmO09LnuUqN5wION04"
bot = telebot.TeleBot(TOKEN)

# AccuWeather API kalitingiz
API_KEY = "n9Nd7iseF4VOZthNyg1Ilho2kvAewhSr"

# Viloyatlar va ularning AccuWeather lokatsiya kodlari (o'zingiz to'ldiring)
locations = {
    "Andijon": "123456",
    "Buxoro": "654321",
    "Fargʻona": "789012",
    "Jizzax": "345678",
    "Namangan": "987654",
    "Navoiy": "321098",
    "Qashqadaryo": "210987",
    "Qoraqalpogʻiston Respublikasi": "456789",
    "Samarqand": "567890",
    "Sirdaryo": "876543",
    "Surxondaryo": "765432",
    "Toshkent": "432109",
    "Xorazm": "543210",
}

# Boshlang'ich xabar
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for region in locations.keys():
        markup.add(telebot.types.KeyboardButton(region))
    
    bot.send_message(message.chat.id, 
                     "Salom!👋\n"
                     "Bot Shakhzod Norkobilov tomonidan ishlab chiqilgan!👨🏻‍💻\n"
                     "Murojaat uchun: @shakhzod_norkobilov ✍️\n\n"
                     "Hududni tanlang:", 
                     reply_markup=markup)

# Viloyat tanlanganda ob-havo ma'lumotlarini olish
@bot.message_handler(func=lambda message: message.text in locations)
def get_weather(message):
    region = message.text
    location_code = locations[region]
    url = f"http://dataservice.accuweather.com/forecasts/v1/daily/5day/{location_code}?apikey={API_KEY}&language=uz-uz&metric=true"

    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        forecast = f"📍 *{region}* hududining 5 kunlik ob-havo ma'lumoti:\n\n"

        for day in data['DailyForecasts']:
            date = datetime.datetime.strptime(day['Date'], "%Y-%m-%dT%H:%M:%S%z").strftime("%d-%b, %A")
            min_temp = day['Temperature']['Minimum']['Value']
            max_temp = day['Temperature']['Maximum']['Value']
            condition = day['Day']['IconPhrase']

            forecast += f"📅 *{date}*\n🌡 {min_temp}°C - {max_temp}°C\n🌥 {condition}\n\n"

        bot.send_message(message.chat.id, forecast, parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id, "Ob-havo ma'lumotlarini olishda xatolik yuz berdi. Keyinroq urinib ko'ring.")

# Botni doimiy ishga tushirish
bot.polling(none_stop=True)
