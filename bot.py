import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Telegram API tokenini bevosita kiritish (bu xavfsiz emas, lekin faqat test uchun)
TOKEN = '8165659026:AAGjrs7mL7HwiYl3tgavtNVEWXg5HqCjKcs'  # o'z tokeningizni shu yerga qo'ying

# Loggingni sozlash
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Harf o'zgartirish lug'ati
latin_to_cyrillic_dict = {
    'A': 'А', 'a': 'а', 'B': 'Б', 'b': 'б', 'D': 'Д', 'd': 'д', 'E': 'Э', 'e': 'е', 
    'F': 'Ф', 'f': 'ф', 'G': 'Г', 'g': 'г', 'H': 'Х', 'h': 'х', 'I': 'И', 'i': 'и',
    'J': 'Ж', 'j': 'ж', 'K': 'К', 'k': 'к', 'L': 'Л', 'l': 'л', 'M': 'М', 'm': 'м',
    'N': 'Н', 'n': 'н', 'O': 'О', 'o': 'о', 'P': 'П', 'p': 'п', 'Q': 'Қ', 'q': 'қ',
    'R': 'Р', 'r': 'р', 'S': 'С', 's': 'с', 'Sh': 'Ш', 'sh': 'ш', 'T': 'Т', 't': 'т',
    'U': 'У', 'u': 'у', 'V': 'В', 'v': 'в', 'X': 'Х', 'x': 'х', 'Y': 'Й', 'y': 'й',
    'Z': 'З', 'z': 'з', 'O\'': 'Ў', 'o\'': 'ў', 'Ch': 'Ч', 'ch': 'ч', 'Ng': 'Нг', 'ng': 'нг',
    'Yo': 'Ё', 'yo': 'ё', 'Yu': 'Ю', 'yu': 'ю', 'Ye': 'Е', 'ye': 'е', 'Ya': 'Я', 'ya': 'я',
    'Ъ': '’', 'ъ': '’'
}

cyrillic_to_latin_dict = {v: k for k, v in latin_to_cyrillic_dict.items()}

# Start komandasi
async def start(update, context):
    keyboard = [
        ['LOTIN ➡️ KIRILL', 'КИРИЛЛ ➡️ ЛОТИН'],
        ['AVTO✨']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    await update.message.reply_text(
        "Salom!👋\nBot Shakhzod Norkobilov tomonidan ishlab chiqilgan!👨🏻‍💻\nMurojaat uchun: @shakhzod_norkobilov ✍️",
        reply_markup=reply_markup
    )

# Matnni harfma-harf o'zgartirish
def convert_text(text, conversion_dict):
    result = ''
    i = 0
    while i < len(text):
        # Harf birikmalarini tekshirish
        if i + 1 < len(text) and text[i:i+2] in conversion_dict:
            result += conversion_dict[text[i:i+2]]
            i += 2  # Ikki harfni almashtirdik
        elif text[i] in conversion_dict:
            result += conversion_dict[text[i]]
            i += 1  # Bitta harfni almashtirdik
        else:
            result += text[i]
            i += 1  # O'zgarmagan harfni qo'shamiz
    return result

# Matnlarni alifbo bo'yicha o'zgartirish
async def text_translation(update, context):
    text = update.message.text

    if 'LOTIN ➡️ KIRILL' in update.message.text:
        # Lotin alifbosini Kirillga o'zgartirish
        converted_text = convert_text(text, latin_to_cyrillic_dict)
        await update.message.reply_text(converted_text)
    
    elif 'КИРИЛЛ ➡️ ЛОТИН' in update.message.text:
        # Kirill alifbosini Lotinga o'zgartirish
        converted_text = convert_text(text, cyrillic_to_latin_dict)
        await update.message.reply_text(converted_text)

# Main funksiyasi
def main():
    # Botni ishga tushirish
    application = Application.builder().token(TOKEN).build()

    # Handlerlarni qo'shish
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.Regex('^LOTIN ➡️ KIRILL$'), start))
    application.add_handler(MessageHandler(filters.Regex('^КИРИЛЛ ➡️ ЛОТИН$'), start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_translation))

    # Pollingni boshlash
    application.run_polling()

if __name__ == '__main__':
    main()
