from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from transliterate import translit

# Botni ishga tushirish uchun Tokenni kiritish
TOKEN = '8165659026:AAGjrs7mL7HwiYl3tgavtNVEWXg5HqCjKcs'

# Start komandasi
def start(update, context):
    keyboard = [
        [InlineKeyboardButton("LOTIN ➡️ KIRILL", callback_data='latin_to_cyrillic')],
        [InlineKeyboardButton("КИРИЛЛ ➡️ ЛОТИН", callback_data='cyrillic_to_latin')],
        [InlineKeyboardButton("AVTO✨", callback_data='auto')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        "Salom!👋\nBot Shakhzod Norkobilov tomonidan ishlab chiqilgan!👨🏻‍💻\nMurojaat uchun: @shakhzod_norkobilov ✍️",
        reply_markup=reply_markup
    )

# Lotin alifbosini Kirillga o'zgartirish
def latin_to_cyrillic(update, context):
    update.callback_query.answer()
    update.callback_query.message.reply_text("Matnni yuboring!")

# Kirill alifbosini Lotinga o'zgartirish
def cyrillic_to_latin(update, context):
    update.callback_query.answer()
    update.callback_query.message.reply_text("Матнни юборинг!")

# Matnni avtomatik tarzda tarjima qilish
def auto(update, context):
    update.callback_query.answer()
    update.callback_query.message.reply_text("Matnni yuboring!\nМатнни юборинг!")

# Matnlarni alifbo bo'yicha o'zgartirish
def text_translation(update, context):
    text = update.message.text
    if text.isascii():
        # Lotin alifbosida bo'lsa
        converted_text = translit(text, 'ru', reversed=True)
    elif all(ord(char) < 128 for char in text):
        # Kirill alifbosida bo'lsa
        converted_text = translit(text, 'ru')
    else:
        converted_text = text

    update.message.reply_text(converted_text)

# Main funksiyasi
def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CallbackQueryHandler(latin_to_cyrillic, pattern='latin_to_cyrillic'))
    dispatcher.add_handler(CallbackQueryHandler(cyrillic_to_latin, pattern='cyrillic_to_latin'))
    dispatcher.add_handler(CallbackQueryHandler(auto, pattern='auto'))
    dispatcher.add_handler(MessageHandler(Filters.text, text_translation))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
