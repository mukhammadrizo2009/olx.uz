import requests
from decouple import config
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes


BOT_TOKEN = config("BOT_TOKEN")
BACKEND_URL = config("BACKEND_URL")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    data = {
        "telegram_id": user.id,
        "username": user.username or "",
        "first_name": user.first_name or "",
        "last_name": user.last_name or "",
    }

    try:
        response = requests.post(BACKEND_URL, json=data)

        if response.status_code == 200:
            result = response.json()
            context.user_data["access_token"] = result["access"]

            await update.message.reply_text(
                f"✅ Siz muvaffaqiyatli tizimga kirdingiz!"
            )
        else:
            await update.message.reply_text("❌ Backend xatolik qaytardi")

    except Exception as e:
        await update.message.reply_text("❌ Server bilan bog'lanishda xatolik")


app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))

app.run_polling()