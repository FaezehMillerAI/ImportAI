"""
Logistics & Customs Agent: مدیریت حمل، تخصیص ارز نیما و ترخیص گمرکی
"""
from services.llm_service import LLMService

SYSTEM_PROMPT = """
شما ایجنت هوشمند Logistics & Customs Advisor هستید.
وظیفه شما مشاوره در زمینه روش‌های حمل (دریایی، هوایی)، محاسبه تقریبی فریت، مراحل تخصیص ارز نیما و ترخیص گمرکی است.
"""

class LogisticsAgent:
    @staticmethod
    async def process_chat(user_message: str) -> str:
        return await LLMService.generate_response(SYSTEM_PROMPT, user_message)
