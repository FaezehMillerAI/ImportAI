"""
EduLead Agent: آموزش واردات، اجرای گیمیفیکیشن و جذب لید اولیه
"""
from services.llm_service import LLMService

SYSTEM_PROMPT = """
شما "آریا"، ایجنت هوشمند EduLead پلتفرم مشاوره واردات هستید.
وظایف اصلی شما:
۱. آموزش مراحل واردات به زبان کاملاً ساده، کاربردی و جذاب.
۲. دعوت کاربر به شرکت در بازی شبیه‌ساز ۵۰,۰۰۰ دلاری واردات.
۳. تاکید بر این‌که ما فروشنده کالا نیستیم، بلکه Sourcing Agent و مشاور کاهش ریسک واردات هستیم.
۴. داشتن لحنی بسیار صمیمی، حرفه‌ای و ایجاد حس اعتماد در مخاطب.
"""

class EduLeadAgent:
    @staticmethod
    async def process_chat(user_message: str) -> str:
        return await LLMService.generate_response(SYSTEM_PROMPT, user_message)

    @staticmethod
    def get_gamification_scenario(capital: float = 50000, industry: str = "machinery"):
        return {
            "title": f"شبیه‌سازی واردات با سرمایه {capital:,.0f} دلار در صنعت {industry}",
            "steps": [
                {"step": 1, "question": "انتخاب صنعت و کالای اصلی"},
                {"step": 2, "question": "انتخاب کارخانه: قیمت ارزان vs کارخانه ثبت‌شده در QCC"},
                {"step": 3, "question": "بازرسی قبل از حمل (PSI): آیا کنترل کیفیت انجام شود؟"},
                {"step": 4, "question": "تخصیص ارز: ارز نیما vs ارز صادراتی"}
            ]
        }
