"""
Sourcing & HS Specialist Agent: مشاور ارشد تعیین تعرفه و استراتژی سورسینگ بین‌المللی
"""
from services.llm_service import LLMService
from services.hs_database import search_hs_code

SYSTEM_PROMPT = """
شما مدیر ارشد سورسینگ بین‌المللی و کارشناس خبره تعیین تعرفه و کد HS کالاها (Chief Sourcing Officer) هستید.

اصول پاسخگویی:
۱. از هرگونه معرفی‌های رباتیک و تکراری (مثل «من ایجنت هستم») کاملاً پرهیز کنید.
۲. هنگام دریافت مشخصات یا نام کالا، کد ۸ رقمی HS، درصد حقوق و عوارض گمرکی ایران، وضعیت تخصیص ارز (نیما / صادراتی)، مجوزهای الزامی صمت/استاندارد/بهداشت و برترین استان‌های تولیدکننده در چین (مانند گوانگ‌دونگ، ژجیانگ، جیانگسو، شاندونگ) را به شکل کاملاً ساختاریافته، جذاب و کاربردی ارائه دهید.
۳. در پایان با یک سوال یا پیشنهاد هوشمندانه، کاربر را به ادامه گفتگو برای استعلام قیمت واقعی FOB یا بررسی نمونه کالا ترغیب کنید.
"""

class SourcingAgent:
    @staticmethod
    async def process_chat(user_message: str) -> str:
        matches = search_hs_code(user_message)
        context = ""
        if matches and len(matches) > 0:
            item = matches[0]
            context = f"\n[سیستم داده‌های پایگاه را استخراج کرد: کد HS={item['hs_code']} | عوارض گمرکی={item['customs_duty_percent']}% | ارز={'نیما' if item['nima_eligible'] else 'صادراتی'} | مجوز={item['import_permit']} | گروه کالایی={item['priority_group']} | مبدأ={item['recommended_origin']}]"

        enriched_prompt = SYSTEM_PROMPT + context
        return await LLMService.generate_response(enriched_prompt, user_message)
