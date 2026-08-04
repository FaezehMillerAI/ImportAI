"""
Sourcing & HS Specialist Agent: تعیین کد HS و سورسینگ بین‌المللی
"""
from services.llm_service import LLMService
from services.hs_database import search_hs_code

SYSTEM_PROMPT = """
شما ایجنت هوشمند Sourcing & HS Specialist هستید.
وظیفه شما دریافت مشخصات کالا، استخراج کد HS، بررسی تعرفه گمرکی و پیشنهاد برترین هاب‌های خرید (چین، هند، ترکیه) است.
"""

class SourcingAgent:
    @staticmethod
    async def process_chat(user_message: str) -> str:
        # Search in HS database
        matches = search_hs_code(user_message)
        if matches and len(matches) > 0:
            item = matches[0]
            summary = (
                f"📦 **گزارش تخصصی کد HS و تعرفه گمرکی:**\n\n"
                f"• **نام و عنوان کالا:** {item['title_fa']}\n"
                f"• **کد تعرفه گمرکی (HS Code):** `{item['hs_code']}`\n"
                f"• **حقوق و عوارض گمرکی:** {item['customs_duty_percent']}٪\n"
                f"• **مبنای ارز:** {'✅ ارز نیما / تالار دوم مرکز مبادله' if item['nima_eligible'] else '⚠️ ارز حاصل از صادرات'}\n"
                f"• **مجوزهای الزامی:** {item['import_permit']}\n"
                f"• **گروه کالایی صمت:** {item['priority_group']}\n"
                f"• **کشورهای مبدأ پیشنهادی:** {item['recommended_origin']}\n\n"
                f"💡 *آیا مایلید استعلام قیمت واقعی FOB از ۲ تامین‌کننده برتر چین برای شما دریافت شود؟*"
            )
            return summary

        return await LLMService.generate_response(SYSTEM_PROMPT, user_message)
