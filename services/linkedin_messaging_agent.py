"""
سرویس پاسخگویی خودکار به پیام‌ها و InMailهای لینکدین (LinkedIn Messaging Agent)
"""
from agents.orchestrator import MasterOrchestrator

class LinkedInMessagingAgent:
    @staticmethod
    async def handle_incoming_linkedin_message(profile_id: str, full_name: str, company: str, message_text: str):
        """
        پردازش پیام دریافت شده در پیام خصوصی یا InMail لینکدین با لحن B2B حرفه‌ای
        """
        msg = message_text.strip()

        # Route request via Master Orchestrator
        result = await MasterOrchestrator.route_request(msg, target_agent="auto")

        reply = (
            f"جناب آقای/خانم {full_name} گرامی ({company})\n"
            f"با سلام و احترام،\n\n"
            f"🤖 {result['agent_name']}:\n"
            f"{result['response']}\n\n"
            f"🤝 در صورت تمایل جهت بررسی پروفرما، استعلام ثبتی کارخانه چین (QCC Audit) یا تنظیم قرارداد سالانه مدیریت زنجیره تأمین، "
            f"خوشحال خواهیم شد زمانی را برای جلسه آنلاین یا حضوری هماهنگ نماییم.\n\n"
            f"با احترام،\n"
            f"تیم ارشد مشاوره و سورسینگ بین‌المللی"
        )
        return reply
