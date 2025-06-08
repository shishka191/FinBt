import os
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext
from db import get_user_data, update_user_data

TOKEN = os.getenv("TOKEN", "8151676195:AAGAxxkgVYIC1FPdfe405Kk33ecP0vW7uMg")
ADMIN_ID = int(os.getenv("ADMIN_ID", "5160389108"))
BACKUP_CHANNEL_ID = int(os.getenv("BACKUP_CHANNEL_ID", "-1002589404034"))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

main_keyboard = [["➕ Доход", "➖ Расход"], ["📊 Статистика", "💰 Максимум на день"]]

async def start(update: Update, context: CallbackContext.DEFAULT_TYPE):
    user_id = update.effective_user.id
    get_user_data(user_id)
    await update.message.reply_text(
        "Привет! Я твой финансовый помощник.",
        reply_markup=ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)
    )

async def send_backup(context: CallbackContext.DEFAULT_TYPE, message: str):
    try:
        await context.bot.send_message(chat_id=BACKUP_CHANNEL_ID, text=message)
    except Exception as e:
        logger.error(f"Ошибка отправки бэкапа: {e}")

async def handle_message(update: Update, context: CallbackContext.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if text.startswith("➕"):
        await update.message.reply_text("Введи сумму дохода:")
        context.user_data["mode"] = "income"
    elif text.startswith("➖"):
        await update.message.reply_text("Введи сумму расхода:")
        context.user_data["mode"] = "expense"
    elif text == "📊 Статистика":
        data = get_user_data(user_id)
        await update.message.reply_text(f"Статистика: {data}")
    elif text == "💰 Максимум на день":
        await update.message.reply_text("Пока не реализовано.")
    else:
        if "mode" in context.user_data:
            try:
                amount = float(text)
                mode = context.user_data.pop("mode")
                update_user_data(user_id, amount, mode)
                await update.message.reply_text(f"{'Доход' if mode == 'income' else 'Расход'} добавлен: {amount}")

                # Отправка бэкапа в канал
                await send_backup(context, f"Пользователь {user_id} добавил {'доход' if mode == 'income' else 'расход'}: {amount}")
            except ValueError:
                await update.message.reply_text("Это не похоже на число...")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
