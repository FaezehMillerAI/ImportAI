"""
سرویس پاسخگویی خودکار ۲۴/۷ به دایرکت‌های اینستاگرام (Instagram DM Webhook & Agent Responder)
"""
from agents.orchestrator import MasterOrchestrator
from database import Lead, get_db

class InstagramDMAgent:
    @staticmethod
    async def handle_incoming_dm(user_instagram_id: str, username: str, message_text: str):
        """
        پردازش پیام دریافت شده در دایرکت اینستاگرام و پاسخگویی خودکار با ارکستریتور ایجنت‌ها
        """
        msg = message_text.strip()

        # Keyword trigger for Lead / Gamification
        if any(w in msg.lower() for w in ["واردات", "شروع", "بازی", "راهنما", "شروع بازی"]):
            reply = (
                f"سلام {username} عزیز! 👋 به پلتفرم هوشمند واردات خوش آمدید.\n\n"
                f"🎮 برای شروع بازی شبیه‌ساز ۵۰,۰۰۰ دلاری واردات یا دریافت استعلام کد HS، یکی از گزینه‌های زیر را بفرستید:\n"
                f"۱️⃣ عدد ۱: شبیه‌سازی واردات ۵۰ هزار دلاری\n"
                f"۲️⃣ عدد ۲: استعلام اعتبار کارخانه چین با QCC\n"
                f"۳️⃣ عدد ۳: استعلام کد HS و تعرفه گمرک\n"
                f"۴️⃣ یا کالا/سوال خودتون رو مستقیماً بنویسید تا ایجنت پاسخ بدهد!"
            )
            return reply

        # Process via Master Orchestrator
        result = await MasterOrchestrator.route_request(msg, target_agent="auto")
        
        reply = (
            f"🤖 {result['agent_name']}:\n\n"
            f"{result['response']}\n\n"
            f"📲 جهت رزرو جلسه مشاوره سورسینگ اختصاصی، شماره تماس خود را دایرکت کنید."
        )
        return reply
