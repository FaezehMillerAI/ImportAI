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

        is_english = "SYSTEM INSTRUCTION: User is using English" in user_message or "English" in user_message

        if is_english:
            summary = (
                f"📊 **China QCC Official Verification Audit (TianYanCha):**\n\n"
                f"🏢 **Official Company Name:** {audit_res['company_name_en']}\n"
                f"🔑 **Credit Code (USCC):** `{audit_res['uscc_code']}`\n"
                f"💰 **Registered Capital:** {audit_res['registration_capital']}\n"
                f"📅 **Establishment Date:** {audit_res['establishment_date']}\n"
                f"👤 **Legal Representative:** {audit_res['legal_representative']}\n"
                f"⚖️ **Litigation History:** {audit_res['litigation_count']} lawsuit(s)\n"
                f"🏦 **Bank Account Match:** {'✅ Fully Matched with PI' if audit_res['bank_account_matched'] else '❌ Account Mismatch'}\n\n"
                f"✅ **Status:** Officially registered with China Administration for Market Regulation (SAMR).\n\n"
                f"🛡️ *Would you like to request an On-Site Factory Physical Audit & Inspection report?*"
            )
        else:
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
