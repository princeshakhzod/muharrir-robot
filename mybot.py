from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ConversationHandler, ContextTypes, filters

# Bosqichlar uchun o'zgaruvchilar
AMOUNT, DURATION, INTEREST, CONFIRM = range(4)

# Ma'lumotlarni vaqtinchalik saqlash
user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Botni boshlash va foydalanuvchidan omonat summasini so‘rash"""
    user_data.clear()  # Avvalgi ma'lumotlarni tozalash
    await update.message.reply_text("Salom!👋\n"
        "Bot Shakhzod Norkobilov tomonidan ishlab chiqilgan!👨🏻‍💻\n"
        "Murojaat uchun: @shakhzod_norkobilov ✍️\n\n"
        "Omonat summasini kiriting: 👇")
    return AMOUNT

async def amount(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Foydalanuvchidan omonat summasini olish"""
    try:
        user_data["amount"] = float(update.message.text)
        await update.message.reply_text("Omonat muddatini kiriting (oylarda):")
        return DURATION
    except ValueError:
        await update.message.reply_text("Iltimos, to'g'ri summani kiriting.")
        return AMOUNT

async def duration(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Foydalanuvchidan omonat muddatini olish"""
    try:
        user_data["duration"] = int(update.message.text)
        await update.message.reply_text("Omonat foizini kiriting (yillik):")
        return INTEREST
    except ValueError:
        await update.message.reply_text("Iltimos, to'g'ri muddatni kiriting.")
        return DURATION

async def interest(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Foydalanuvchidan yillik foiz stavkasini olish"""
    try:
        user_data["interest"] = float(update.message.text)
        message = (
            f"Kiritilgan ma'lumotlar:\n"
            f"💰 Omonat summasi: {user_data['amount']} so'm\n"
            f"📅 Omonat muddati: {user_data['duration']} oy\n"
            f"📈 Foiz stavkasi: {user_data['interest']}%\n\n"
            "Ma'lumotlarni tasdiqlash uchun quyidagi tugmalardan birini bosing:"
        )
        reply_markup = ReplyKeyboardMarkup([["OK"], ["Qayta boshlash"]], one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text(message, reply_markup=reply_markup)
        return CONFIRM
    except ValueError:
        await update.message.reply_text("Iltimos, to'g'ri foiz stavkasini kiriting.")
        return INTEREST

async def confirm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Foydalanuvchi ma'lumotlarni tasdiqlaganda hisob-kitobni bajarish"""
    if update.message.text == "OK":
        amount = user_data["amount"]
        duration = user_data["duration"]
        interest = user_data["interest"]

        # Oddiy foiz hisoblash
        profit = amount * (interest / 100) * (duration / 12)
        total = amount + profit

        # Har oy uchun foiz hisoblash
        interest_details = "\n".join([f"{i+1}. oy: {profit / duration:.2f} so'm" for i in range(duration)])

        result = (
            f"Hisob-kitob natijalari:\n"
            f"💰 Omonat summasi: {amount} so'm\n"
            f"📅 Omonat muddati: {duration} oy\n"
            f"📈 Yillik foiz: {interest}%\n"
            f"----------------------\n"
            f"🔹 Foyda: {profit:.2f} so'm\n"
            f"🔹 Umumiy summa: {total:.2f} so'm\n\n"
            f"📊 Har oyda to'lanadigan foiz summalari:\n{interest_details}"
        )
        reply_markup = ReplyKeyboardMarkup([["/START YANGI HISOB-KITOB"]], one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text(result, reply_markup=reply_markup)
        return ConversationHandler.END

    elif update.message.text == "Qayta boshlash":
        return await start(update, context)  # Jarayonni qaytadan boshlash

async def new_calculation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Yangi hisob-kitob tugmasi bosilganda jarayonni qayta boshlash"""
    return await start(update, context)

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Botdan foydalanishni bekor qilish"""
    await update.message.reply_text("Botdan foydalanish bekor qilindi.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def main() -> None:
    """Botni ishga tushirish"""
    application = ApplicationBuilder().token("7740837657:AAETai-i5V2BnuSsgU8jILuOpZwrTY9b2lE").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, amount)],
            DURATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, duration)],
            INTEREST: [MessageHandler(filters.TEXT & ~filters.COMMAND, interest)],
            CONFIRM: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, confirm),
                MessageHandler(filters.Regex("^/START YANGI HISOB-KITOB$"), new_calculation),  # "/START YANGI HISOB-KITOB" tugmasi ishlaydi
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == "__main__":
    main()