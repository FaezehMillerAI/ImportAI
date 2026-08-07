"""
Unified Ultra-Smart LLM Service for Multi-Agent AI System
Supports DeepSeek V3/R1, OpenAI GPT-4o, Google Gemini, and Conversational Context Memory
"""
import httpx
from config import settings

class LLMService:
    @staticmethod
    async def generate_response(system_prompt: str, user_message: str, chat_history: list = None, model_name: str = "deepseek-chat") -> str:
        messages = [{"role": "system", "content": system_prompt}]

        if chat_history:
            for item in chat_history[-6:]:
                messages.append(item)
        
        messages.append({"role": "user", "content": user_message})

        # 1. Try DeepSeek API (V3 / R1) if DEEPSEEK_API_KEY is present
        if settings.DEEPSEEK_API_KEY:
            try:
                async with httpx.AsyncClient(timeout=45.0) as client:
                    resp = await client.post(
                        "https://api.deepseek.com/chat/completions",
                        headers={"Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}"},
                        json={
                            "model": model_name,
                            "messages": messages,
                            "temperature": 0.7
                        }
                    )
                    if resp.status_code == 200:
                        return resp.json()["choices"][0]["message"]["content"]
                    else:
                        print(f"[DeepSeek Status] {resp.status_code}: {resp.text[:150]}")
            except Exception as e:
                print(f"[LLM Error] DeepSeek API call failed: {e}")

        # 2. Try Google Gemini API if GEMINI_API_KEY is present
        if settings.GEMINI_API_KEY:
            try:
                async with httpx.AsyncClient(timeout=45.0) as client:
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={settings.GEMINI_API_KEY}"
                    contents = [{"role": "user", "parts": [{"text": f"{system_prompt}\n\nUser Question: {user_message}"}]}]
                    resp = await client.post(url, json={"contents": contents})
                    if resp.status_code == 200:
                        return resp.json()["candidates"][0]["content"]["parts"][0]["text"]
            except Exception as e:
                print(f"[LLM Error] Gemini API call failed: {e}")

        # 3. Try OpenAI GPT-4o / GPT-4o-mini if API Key is present
        if settings.OPENAI_API_KEY:
            try:
                async with httpx.AsyncClient(timeout=45.0) as client:
                    resp = await client.post(
                        "https://api.openai.com/v1/chat/completions",
                        headers={"Authorization": f"Bearer {settings.OPENAI_API_KEY}"},
                        json={
                            "model": "gpt-4o-mini",
                            "messages": messages,
                            "temperature": 0.7
                        }
                    )
                    if resp.status_code == 200:
                        return resp.json()["choices"][0]["message"]["content"]
            except Exception as e:
                print(f"[LLM Error] OpenAI API call failed: {e}")

        # 4. Domain Expert Fallback Engine
        return LLMService._expert_domain_fallback(system_prompt, user_message)

    @staticmethod
    def _expert_domain_fallback(system_prompt: str, user_message: str) -> str:
        msg = user_message.lower().strip()

        if any(w in msg for w in ["بله", "اره", "آره", "لطفا", "لطفاً", "میخوام", "می‌خوام", "بفرست"]):
            return (
                "بسیار عالی! 🎯\n\n"
                "جهت استعلام دقیق قیمت واقعی FOB، دریافت پیش‌فاکتور و معرفی ۲ تامین‌کننده برتر در چین، لطفاً موارد زیر را ارسال کنید:\n\n"
                "۱. **حجم سفارش مورد نیاز** (مثلاً: ۵ دستگاه / ۱ کانتینر)\n"
                "۲. **شماره تماس / واتساپ** شما جهت ارسال گزارش رسمی سورسینگ\n\n"
                "📞 *تیم سورسینگ بین‌المللی ما در کمتر از ۲ ساعت گزارش کامل را برای شما ارسال خواهد کرد.*"
            )

        if "لاستیک" in msg or "تایر" in msg:
            return (
                "📦 **اطلاعات تخصصی واردات لاستیک:**\n"
                "• **کد HS:** 4011.10.00\n"
                "• **حقوق گمرکی:** ۳۲٪\n"
                "• **مبنای ارز:** ارز نیما (تالار دوم مرکز مبادله)\n"
                "• **مجوزها:** تاییدیه دفتر صنایع خودرو صمت + سازمان ملی استاندارد\n\n"
                "💡 *جهت استعلام دقیق قیمت FOB از کارخانجات معتبر شاندونگ چین، حجم سفارش و شماره تماس خود را بفرستید.*"
            )
        elif "اعتبار" in msg or "چین" in msg or "کارخانه" in msg or "ltd" in msg or "co." in msg:
            return (
                "📊 **گزارش اعتبارسنجی ثبتی QCC چین:**\n"
                "ما شرکت‌های صادرکننده را در سامانه رسمی QCC (企查查) بررسی می‌کنیم:\n"
                "۱. سابقه ثبتی و میزان سرمایه ثبتی واقعی\n"
                "۲. بررسی پرونده‌های شاکی و دادگاهی مدیران\n"
                "۳. انطباق حساب بانکی شرکت با فاکتور صادرشده (PI).\n\n"
                "نام انگلیسی شرکت مورد نظرتان را ارسال کنید تا استعلام شود."
            )
        elif "ارز" in msg or "نیما" in msg or "صادرات" in msg:
            return (
                "🏛️ **راهنمای تخصیص ارز نیما و صادراتی:**\n"
                "برای واردات کالاهای گروه ۲۱ و ۲۲، امکان ثبت سفارش با ارز نیما در سامانه جامع تجارت وجود دارد.\n"
                "صف تخصیص ارز معمولاً بین ۳۰ تا ۶۰ روز کاری زمان می‌برد."
            )
        elif "مراحل" in msg or "چگونه" in msg or "شروع" in msg:
            return (
                "مراحل اصلی واردات شامل ۱۱ گام کلیدی است:\n"
                "۱. تعیین مشخصات کالا و کد HS\n"
                "۲. سورسینگ و یافتن تولیدکنندگان اصلی در چین/ترکیه\n"
                "۳. اعتبارسنجی حقوقی شرکت صادرکننده در QCC\n"
                "۴. دریافت و بررسی نمونه کالا (Sample)\n"
                "۵. مذاکره اینکوترمز (FOB/EXW)\n"
                "۶. بازرسی کیفیت قبل از حمل (PSI)\n"
                "۷. مدیریت حمل و ترخیص گمرکی با تخصیص ارز نیما."
            )
        else:
            return (
                "سلام! من ایجنت هوشمند ارشد مشاوره و سورسینگ واردات هستم.\n\n"
                "من می‌توانم به هر سوال شما در زمینه‌های زیر پاسخ دهم:\n"
                "• استخراج کد HS و تعرفه گمرک تمام کالاها\n"
                "• اعتبارسنجی ثبتی کارخانجات چین در QCC\n"
                "• محاسبه هزینه حمل، تخصیص ارز نیما و ترخیص\n"
                "• استعلام قیمت واقعی FOB از تولیدکنندگان دست اول\n\n"
                "لطفاً سوال یا نام کالای مورد نظر خود را بنویسید!"
            )
