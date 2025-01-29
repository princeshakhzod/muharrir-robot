import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from transliterate import translit

# Telegram API tokenini bevosita kiritish (bu xavfsiz emas, lekin faqat test uchun)
TOKEN = '8165659026:AAGjrs7mL7HwiYl3tgavtNVEWXg5HqCjKcs'

# Loggingni sozlash
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Start komandasi
async def start(update, context):
    # Doimiy ko'rinadigan tugmalarni yaratish
    keyboard = [
        [InlineKeyboardButton("LOTIN ➡️ KIRILL", callback_data='latin_to_cyrillic')],
        [InlineKeyboardButton("КИРИЛЛ ➡️ ЛОТИН", callback_data='cyrillic_to_latin')],
        [InlineKeyboardButton("AVTO✨", callback_data='auto')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Salom!👋\nBot Shakhzod Norkobilov tomonidan ishlab chiqilgan!👨🏻‍💻\nMurojaat uchun: @shakhzod_norkobilov ✍️",
        reply_markup=reply_markup
    )

# Lotin alifbosini Kirillga o'zgartirish
async def latin_to_cyrillic(update, context):
    await update.callback_query.answer()
    await update.callback_query.message.reply_text("Matnni yuboring!")

# Kirill alifbosini Lotinga o'zgartirish
async def cyrillic_to_latin(update, context):
    await update.callback_query.answer()
    await update.callback_query.message.reply_text("Матнни юборинг!")

# Matnni avtomatik tarzda tarjima qilish
async def auto(update, context):
    await update.callback_query.answer()
    await update.callback_query.message.reply_text("Matnni yuboring!\nМатнни юборинг!")

# Matnlarni alifbo bo'yicha o'zgartirish
async def text_translation(update, context):
    text = update.message.text
    if text.isascii():
        # Lotin alifbosida bo'lsa
        converted_text = translit(text, 'ru', reversed=True)
    elif all(ord(char) >= 128 for char in text):
        # Kirill alifbosida bo'lsa
        converted_text = translit(text, 'ru')
    else:
        converted_text = text

    await update.message.reply_text(converted_text)

# Xatoliklarni qayta ishlash
async def error(update, context):
    logger.error(f"Error: {context.error}")

# Main funksiyasi
def main():
    # Botni ishga tushirish
    application = Application.builder().token(TOKEN).build()

    # Handlerlarni qo'shish
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(latin_to_cyrillic, pattern='latin_to_cyrillic'))
    application.add_handler(CallbackQueryHandler(cyrillic_to_latin, pattern='cyrillic_to_latin'))
    application.add_handler(CallbackQueryHandler(auto, pattern='auto'))
    application.add_handler(MessageHandler(filters.TEXT, text_translation))

    # Xatoliklarni qayta ishlash
    application.add_error_handler(error)

    # Pollingni boshlash
    application.run_polling()

if __name__ == '__main__':
    main()
