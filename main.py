# from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
# from telegram.ext import Application, CommandHandler, ContextTypes
#
# TOKEN = "ВСТАВЬ_СВОЙ_ТОКЕН"
# WEBAPP_URL = "https://your-domain.com/index.html"  # Ссылка на мини-приложение
#
# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     keyboard = [
#         [KeyboardButton("🚀 Открыть Mini App", web_app=WebAppInfo(url=WEBAPP_URL))]
#     ]
#     reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
#     await update.message.reply_text("Нажми кнопку, чтобы открыть Mini App:", reply_markup=reply_markup)
#
# def main():
#     app = Application.builder().token(TOKEN).build()
#     app.add_handler(CommandHandler("start", start))
#     print("Бот запущен...")
#     app.run_polling()
#
# if __name__ == "__main__":
#     main()
