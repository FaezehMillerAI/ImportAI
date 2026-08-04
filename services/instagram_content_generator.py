"""
سرویس تولید محتوای هوشمند اینستاگرام (پست، ریلز و استوری)
"""
import random
from services.llm_service import LLMService

TOPICS = [
    {"topic": "۵ اشتباه مهلک واردکنندگان تازه کار در چین", "type": "reels"},
    {"topic": "چگونه اصالت کارخانه چین را با QCC استعلام کنیم؟", "type": "carousel"},
    {"topic": "رازمخفی تخصیص ارز نیما در سامانه جامع تجارت", "type": "reels"},
    {"topic": "شبیه‌سازی واردات ۵۰ هزار دلاری (گیمیفیکیشن)", "type": "story"},
    {"topic": "محاسبه دقیق تعرفه گمرکی و کد HS کالاها", "type": "carousel"},
    {"topic": "تفاوت بازرسی کیفیت PSI با کنترل کیفیت کارخانه", "type": "reels"}
]

class InstagramContentGenerator:
    @staticmethod
    async def generate_daily_content():
        selected = random.sample(TOPICS, 3)
        generated_posts = []

        for item in selected:
            prompt = (
                f"شما سناریونویس ارشد اینستاگرام بازرگانی هستید. برای موضوع '{item['topic']}' "
                f"یک محتوای فوق‌العاده جذاب، آموزشی و ویروسی در قالب {item['type']} تولید کنید.\n"
                f"شامل: ۱. تیتر قلاب (Hook) ۲. متن اصلی یا سناریوی ویدیو ۳. دعوت به اقدام (CTA) برای دایرکت دادن ۴. هشتگ‌های تخصصی."
            )
            content = await LLMService.generate_response(prompt, "تولید محتوای امروز")
            generated_posts.append({
                "topic": item['topic'],
                "content_type": item['type'],
                "script_caption": content,
                "cta": "📲 برای شروع بازی واردات ۵0 هزار دلاری یا استعلام کارخانه، کلمه 'واردات' را دایرکت کنید!"
            })

        return generated_posts

if __name__ == "__main__":
    import asyncio
    res = asyncio.run(InstagramContentGenerator.generate_daily_content())
    print(f"Generated {len(res)} Instagram posts successfully!")
