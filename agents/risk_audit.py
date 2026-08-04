"""
Risk & Audit Analyst Agent: اعتبارسنجی ثبتی، دادگاهی و حقوقی کارخانجات چین
"""
from services.llm_service import LLMService
from services.qcc_verifier import verify_china_company

SYSTEM_PROMPT = """
شما ایجنت تخصصی تحلیل ریسک و اعتبارسنجی حقوقی (Risk & Audit Analyst) هستید.
وظیفه شما بررسی اصالت تامین‌کنندگان خارجی، سرمایه ثبتی، پرونده‌های دادگاهی و انطباق شماره حساب با فاکتور صادرشده (PI) است.
"""

class RiskAuditAgent:
    @staticmethod
    async def process_chat(user_message: str) -> str:
        # Verify company via QCC Engine
        audit_res = verify_china_company(user_message)
        summary = (
            f"📊 **گزارش اعتبارسنجی ثبتی QCC چین (TianYanCha Audit):**\n\n"
            f"🏢 **نام رسمی شرکت:** {audit_res['company_name_en']}\n"
            f"🔑 **شناسه ثبتی اعتباری (USCC):** `{audit_res['uscc_code']}`\n"
            f"💰 **سرمایه ثبتی واقعی:** {audit_res['registration_capital']}\n"
            f"📅 **تاریخ تأسیس و سابقه:** {audit_res['establishment_date']}\n"
            f"👤 **نماینده قانونی (Legal Rep):** {audit_res['legal_representative']}\n"
            f"⚖️ **سابقه پرونده‌های قضایی/شاکی:** {audit_res['litigation_count']} پرونده\n"
            f"🏦 **تطابق حساب بانکی با PI:** {'✅ منطبق' if audit_res['bank_account_matched'] else '❌ عدم انطباق'}\n\n"
            f"{audit_res['risk_details']}\n\n"
            f"🛡️ *جهت دریافت گزارش بازرسی حضوری کارخانه (Factory Physical Audit)، درخواست مشاوره ثبت کنید.*"
        )
        return summary
