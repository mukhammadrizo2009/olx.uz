# users/bot.py
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from django.conf import settings
from .models import User

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg_user = update.effective_user
    
    user, created = User.objects.get_or_create(
        telegram_id=tg_user.id,
        defaults={
            'username': tg_user.username or f"user_{tg_user.id}",
            'first_name': tg_user.first_name,
            'last_name': tg_user.last_name or "",
        }
    )

    text = f"Xush kelibsiz, {user.first_name}!\n"
    if created:
        text += "Siz muvaffaqiyatli ro'yxatdan o'tdingiz."
    else:
        text += "Sizni qayta ko'rganimizdan xursandmiz."

    await update.message.reply_text(text)

def run_bot():
    # settings.py dagi TELEGRAM_BOT_TOKEN ni ishlatamiz
    app = ApplicationBuilder().token(settings.TELEGRAM_BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    
    print("Bot ishga tushdi...")
    app.run_polling()