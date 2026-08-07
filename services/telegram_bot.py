"""
سرویس ربات تلگرام چندایجنتی واقعی پلتفرم واردات (همراه با حافظه مکالمه و سیستم خودکار بازیابی شبکه)
"""
import sys
import os
import asyncio

# Add root directory to python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from telegram.request import HTTPXRequest
from config import settings
from agents.orchestrator import MasterOrchestrator
from services.qcc_verifier import verify_china_company

# Memory dictionary to store chat history per user
user_chat_history = {}

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_text = (
        f"سلام {user.first_name} عزیز! 👋\n"
        f"به **پلتفرم هوشمند مشاوره، اعتبارسنجی و سورسینگ واردات** خوش آمدید.\n\n"
        f"🤖 شبکه ایجنت‌های فوق‌هوشمند ۲۴/۷ در خدمت شما هستند:\n"
        f"• 🎓 آموزش واردات و گیمیفیکیشن ۵۰k$\n"
        f"• 🔎 استعلام کد HS و تعرفه گمرک تمام کالاها\n"
        f"• 🛡️ اعتبارسنجی ثبتی کارخانجات چین (QCC Audit)\n"
        f"• 🚢 مشاوره حمل، تخصیص ارز نیما و ترخیص\n\n"
        f"هر سوالی در مورد واردات، قوانین گمرک یا شرکت‌های چینی دارید بپرسید، یا یکی از گزینه‌های زیر را انتخاب کنید:"
    )

    keyboard = [
        [InlineKeyboardButton("🎮 شروع بازی شبیه‌ساز واردات", callback_query_data="game_start")],
        [InlineKeyboardButton("🛡️ استعلام اعتبار کارخانه چین", callback_query_data="audit_start")],
        [InlineKeyboardButton("🔍 جستجوی کد HS و تعرفه گمرک", callback_query_data="hs_search")],
        [InlineKeyboardButton("📞 درخواست مشاوره اختصاصی", callback_query_data="lead_form")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(welcome_text, parse_mode="Markdown", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "game_start":
        text = (
            "🎮 **شبیه‌ساز گیمیفیکیشن واردات (سرمایه ۵۰,۰۰۰ دلار)**\n\n"
            "مرحله ۱: صنعت هدف خود را انتخاب کنید:"
        )
        keyboard = [
            [InlineKeyboardButton("🩺 تجهیزات پزشکی", callback_query_data="game_ind_med")],
            [InlineKeyboardButton("🏭 ماشین‌آلات صنعتی", callback_query_data="game_ind_mac")],
            [InlineKeyboardButton("🧪 مواد اولیه شیمیایی", callback_query_data="game_ind_chem")],
            [InlineKeyboardButton("📱 لوازم جانبی دیجیتال", callback_query_data="game_ind_digi")]
        ]
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data.startswith("game_ind_"):
        text = (
            "مرحله ۲: انتخاب کارخانه در چین\n\n"
            "🏭 **کارخانه A:** قیمت ۱۵٪ ارزان‌تر، بدون ثبت رسمی QCC، تسویه ۱۰۰٪ قبل حمل!\n"
            "🏭 **کارخانه B:** دارای ثبت رسمی QCC و CE، پرداخت ۳۰٪ پیش‌پرداخت + ۷۰٪ پس از PSI."
        )
        keyboard = [
            [InlineKeyboardButton("✅ انتخاب کارخانه B (معتبر)", callback_query_data="game_supp_verified")],
            [InlineKeyboardButton("⚠️ انتخاب کارخانه A (ارزان)", callback_query_data="game_supp_cheap")]
        ]
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data.startswith("game_supp_"):
        is_cheap = "cheap" in query.data
        if is_cheap:
            result_text = (
                "⚠️ **نتیجه شبیه‌سازی:**\n"
                "متاسفانه با انتخاب تامین‌کننده ارزانِ ثبت‌نشده، احتمال از دست رفتن سرمایه و کلاهبرداری وجود داشت!\n\n"
                "💡 **توصیه ایجنت:** همیشه قبل از ارسال حواله، اعتبارسنجی QCC و بازرسی PSI انجام دهید."
            )
        else:
            result_text = (
                "🎉 **نتیجه شبیه‌سازی:**\n"
                "سود خالص تخمینی: **۱۲,۴۰۰ دلار (۲۴.۸٪)**\n"
                "سطح ریسک: **بسیار پایین** ✅\n\n"
                "با انتخاب اعتبارسنجی QCC و بازرسی PSI، معامله با امنیت کامل انجام شد."
            )
        await query.edit_message_text(result_text, parse_mode="Markdown")

    elif query.data == "audit_start":
        await query.edit_message_text("لطفا نام انگلیسی کارخانه یا شناسه ثبتی شرکت در چین را ارسال کنید:\nمثال: `Shenzhen Precision Machinery Co., Ltd`", parse_mode="Markdown")
    elif query.data == "hs_search":
        await query.edit_message_text("لطفا نام کالا یا حوزه وارداتی را ارسال کنید:\nمثال: `تجهیزات دندانپزشکی` یا `پلی اتیلن`", parse_mode="Markdown")
    elif query.data == "lead_form":
        await query.edit_message_text("📞 جهت دریافت مشاوره سورسینگ اختصاصی، نام و شماره تماس خود را ارسال کنید تا مشاوران ارشد با شما تماس بگیرند.", parse_mode="Markdown")

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_msg = update.message.text

    # Retrieve history
    if user_id not in user_chat_history:
        user_chat_history[user_id] = []
    
    history = user_chat_history[user_id]

    result = await MasterOrchestrator.route_request(user_msg, target_agent="auto")
    
    # Store turn in history
    history.append({"role": "user", "content": user_msg})
    history.append({"role": "assistant", "content": result['response']})

    formatted_reply = f"🤖 **{result['agent_name']}**:\n\n{result['response']}"
    await update.message.reply_text(formatted_reply, parse_mode="Markdown")

async def start_telegram_bot_async():
    if not settings.TELEGRAM_BOT_TOKEN:
        print("[Telegram Bot] Warning: TELEGRAM_BOT_TOKEN is not set in .env. Bot skipped.")
        return

    request_client = HTTPXRequest(read_timeout=60.0, connect_timeout=60.0)

    try:
        app = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).request(request_client).build()
        app.add_handler(CommandHandler("start", start_command))
        app.add_handler(CallbackQueryHandler(button_handler))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

        print("[Telegram Bot] Initializing unified Telegram Bot background task...")
        await app.initialize()
        await app.start()
        await app.updater.start_polling(bootstrap_retries=10)
        print("[Telegram Bot] Live Telegram Bot polling active!")
    except Exception as e:
        print(f"[Telegram Bot Async Error] {e}")

def run_telegram_bot():
    asyncio.run(start_telegram_bot_async())

if __name__ == "__main__":
    run_telegram_bot()
