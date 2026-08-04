"""
Sales & Conversion Agent: تبدیل لید داغ به مشتری و رزولوشن قرارداد
"""
from services.llm_service import LLMService

SYSTEM_PROMPT = """
شما ایجنت هوشمند Sales & Conversion هستید.
وظیفه شما دریافت مشخصات سفارش، گرفتن شماره تماس/واتساپ واردکنندگان، هماهنگی جلسات مشاوره با مدیران ارشد بازرگانی و صادر کردن پیش‌فاکتور خدمات سورسینگ و اعتبارسنجی است.
"""

class SalesAgent:
    @staticmethod
    async def process_chat(user_message: str) -> str:
        msg = user_message.lower().strip()
        
        # If user confirmed or said "بله لطفا"
        if any(w in msg for w in ["بله", "اره", "آره", "لطفا", "لطفاً", "میخوام", "می‌خوام", "بفرست"]):
            return (
                "بسیار عالی! 🎯\n\n"
                "جهت استعلام دقیق قیمت واقعی FOB، دریافت پیش‌فاکتور و معرفی ۲ تامین‌کننده برتر در چین، لطفاً موارد زیر را ارسال کنید:\n\n"
                "۱. **حجم سفارش مورد نیاز** (مثلاً: ۵۰۰ حلقه / ۱ کانتینر ۴۰ فوت)\n"
                "۲. **شماره تماس / واتساپ** شما جهت ارسال گزارش رسمی سورسینگ\n\n"
                "📞 *تیم سورسینگ بین‌المللی ما در کمتر از ۲ ساعت گزارش کامل قیمت و شرایط تحویل را برای شما ارسال خواهد کرد.*"
            )

        return await LLMService.generate_response(SYSTEM_PROMPT, user_message)
