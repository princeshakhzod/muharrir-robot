import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Telegram API tokenini bevosita kiritish (bu xavfsiz emas, lekin faqat test uchun)
TOKEN = '8165659026:AAGjrs7mL7HwiYl3tgavtNVEWXg5HqCjKcs'

# Loggingni sozlash
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Alifbo o'zgartirishning lug'ati
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

# Kirill alifbosidagi harflar
cyrillic_letters = "Аа, Бб, Вв, Гг, Дд, Ее, Ёё, Жж, Зз, Ии, Йй, Кк, Лл, Мм, Нн, Оо, Пп, Рр, Сс, Тт, Уу, Фф, Хх, Цц, Чч, Шш, Щщ, Ъъ, Ыы, Ьь, Ээ, Юю, Яя"

# Lotin alifbosidagi harflar
latin_letters = "A a, B b, D d, E e, F f, G g, H h, I i, J j, Z z, X x, Q q, K k, L l, M m, N n, O o, P p, R r, S s, T t, U u, V v, X x, Y y, O' o', Sh sh, Ch ch, Ng ng"

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

# Lotin alifbosini Kirillga o'zgartirish
async def latin_to_cyrillic(update, context):
    await update.message.reply_text("Matnni yuboring!")

# Kirill alifbosini Lotinga o'zgartirish
async def cyrillic_to_latin(update, context):
    await update.message.reply_text("Матнни юборинг!")

# Alifbo bo'yicha o'zgartirish
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
    
    # "LOTIN ➡️ KIRILL" tugmasi bosilganda Kirill harflari bo'lsa, javob bermaslik
    if any(char in cyrillic_letters for char in text):
        return
    
    # "КИРИЛЛ ➡️ ЛОТИН" tugmasi bosilganda Lotin harflari bo'lsa, javob bermaslik
    if any(char in latin_letters for char in text):
        return
    
    # Matnni o'zgartirish
    if text.isascii():
        # Lotin alifbosini Kirillga o'zgartirish
        converted_text = convert_text(text, latin_to_cyrillic_dict)
    elif all(ord(char) >= 128 for char in text):
        # Kirill alifbosini Lotinga o'zgartirish
        converted_text = convert_text(text, cyrillic_to_latin_dict)
    else:
        converted_text = text  # Agar matnni o'zgartirish shart emas bo'lsa

    await update.message.reply_text(converted_text)

# Main funksiyasi
def main():
    # Botni ishga tushirish
    application = Application.builder().token(TOKEN).build()

    # Handlerlarni qo'shish
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.Regex('^LOTIN ➡️ KIRILL$'), latin_to_cyrillic))
    application.add_handler(MessageHandler(filters.Regex('^КИРИЛЛ ➡️ ЛОТИН$'), cyrillic_to_latin))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_translation))

    # Pollingni boshlash
    application.run_polling()

if __name__ == '__main__':
    main()  # asyncio.run() ishlatmaslik kerak
