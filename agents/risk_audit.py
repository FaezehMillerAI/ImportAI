"""
Risk & Audit Analyst Agent: کارشناس ارشد اعتبارسنجی حقوقی و تحلیل ریسک کارخانجات چین
"""
from services.llm_service import LLMService
from services.qcc_verifier import verify_china_company

SYSTEM_PROMPT = """
شما مدیر ارشد تحلیل ریسک حقوقی و اعتبارسنجی تامین‌کنندگان خارجی (Head of Due Diligence & Risk) هستید.

اصول و چارچوب پاسخگویی:
۱. از مقدمه‌چینی‌های تکراری و کلیشه‌ای بپرهیزید.
۲. با تسلط بر سامانه‌های دولتی چین (SAMR, QCC 企查查, TianYanCha 天眼查)، اصالت ثبت رسمی، سرمایه ثبتی، سوابق دادگاهی و انطباق حساب بانکی شرکت را به صورت کاملاً حرفه‌ای و تحلیلی ارزیابی کنید.
۳. ریسک‌های بالقوه (مانند اصرار به تسویه ۱۰۰٪ قبل از بازرسی یا حساب‌های شخصی فیک) را به وضوح هشدار دهید و راهکار قطعی رفع ریسک (بازرسی حضوری PSI و پرداخت امن ۳۰/۷۰) را پیشنهاد دهید.
"""

class RiskAuditAgent:
    @staticmethod
    async def process_chat(user_message: str) -> str:
        audit_res = verify_china_company(user_message)
        context = (
            f"\n[داده‌های استعلام QCC شرکت '{audit_res['company_name_en']}': "
            f"شناسه USCC: {audit_res['uscc_code']} | "
            f"سرمایه ثبتی: {audit_res['registration_capital']} | "
            f"تاریخ تأسیس: {audit_res['establishment_date']} | "
            f"نماینده قانونی: {audit_res['legal_representative']} | "
            f"پرونده‌های حقوقی: {audit_res['litigation_count']} | "
            f"تطابق حساب بانکی: {'تایید شد' if audit_res['bank_account_matched'] else 'تایید نشد'}]"
        )
        enriched_prompt = SYSTEM_PROMPT + context
        return await LLMService.generate_response(enriched_prompt, user_message)
