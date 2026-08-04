"""
سرویس تولید خودکار محتوای B2B لینکدین (LinkedIn Content Generator)
ویژه مدیران کارخانجات، مدیران تأمین و سرمایه‌گذاران
"""
import random
from services.llm_service import LLMService

B2B_TOPICS = [
    {"topic": "مدیریت ریسک زنجیره تأمین در صنایع تولیدی و کارخانجات", "format": "article_thought_leadership"},
    {"topic": "تحلیل هزینه فایده اعتبارسنجی حقوقی کارخانجات چین (QCC & TianYanCha)", "format": "case_study"},
    {"topic": "کاهش هزینه تمام‌شده مواد اولیه پلیمری و شیمیایی از مبدأ", "format": "b2b_post"},
    {"topic": "چگونه صف تخصیص ارز نیما را برای واردات ماشین‌آلات مدیریت کنیم؟", "format": "b2b_post"},
    {"topic": "مطالعه موردی: جلوگیری از کلاهبرداری ۳۰۰ هزار دلاری در واردات قطعات صنعتی", "format": "case_study"}
]

class LinkedInContentGenerator:
    @staticmethod
    async def generate_daily_b2b_posts():
        selected = random.sample(B2B_TOPICS, 2)
        generated_posts = []

        for item in selected:
            prompt = (
                f"شما استراتژیست ارشد بازاریابی B2B و تجارت بین‌الملل در لینکدین هستید. "
                f"برای مخاطبان سطح C-Level (مدیران عامل، مدیران خرید کارخانجات، سرمایه‌گذاران) "
                f"یک محتوای فوق‌العاده تخصصی، حرفه‌ای و تحلیلی در قالب {item['format']} برای موضوع '{item['topic']}' تولید کنید.\n"
                f"لحن: بسیار محترمانه، تخصصی، تحلیلی همراه با آمار و دیتا.\n"
                f"شامل: ۱. تیتر تحلیلی ۲. بدنه اصلی ۳. راهکار اجرایی ۴. دعوت به ارتباط در InMail/پیام."
            )
            content = await LLMService.generate_response(prompt, "تولید پست لینکدین")
            generated_posts.append({
                "topic": item['topic'],
                "content_format": item['format'],
                "post_text": content,
                "target_audience": "CEOs, Procurement Directors, Factory Owners, Trading Managers",
                "cta": "💼 برای دریافت مشاوره اختصاصی زنجیره تأمین و اعتبارسنجی کارخانجات، در پیام خصوصی لینکدین ارتباط برقرار کنید."
            })

        return generated_posts

if __name__ == "__main__":
    import asyncio
    res = asyncio.run(LinkedInContentGenerator.generate_daily_b2b_posts())
    print(f"Generated {len(res)} LinkedIn B2B posts successfully!")
