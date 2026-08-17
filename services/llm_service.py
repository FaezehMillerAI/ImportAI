"""
Unified Ultra-Smart LLM Service with Live Web Search & Dynamic Intelligence
Supports DeepSeek V3/R1 with Live Web Augmentation (RAG), OpenAI, Gemini, and Domain Reasoning
"""
import httpx
from config import settings
from services.web_search_service import WebSearchService
import asyncio

class LLMService:
    @staticmethod
    async def generate_response(
        system_prompt: str, 
        user_message: str, 
        chat_history: list = None, 
        model_name: str = "deepseek-chat",
        enable_web_search: bool = True
    ) -> str:
        """
        تولید پاسخ هوشمند و زنده با اتصال به جستجوی وب (Live Web Augmentation) و تحلیل عمیق
        """
        web_context = ""
        
        # 1. اجرای خودکار جستجوی وب برای سوالات استعلام شرکت، قیمت، قوانین، کالاها یا اخبار روز
        if enable_web_search:
            try:
                # تشخیص کلمات کلیدی نیازمند جستجوی زنده
                search_triggers = [
                    "شرکت", "کارخانه", "قیمت", "اعتبار", "استعلام", "قانون", "تعرفه", "چین", 
                    "company", "factory", "price", "audit", "verify", "supplier", "hs", "customs",
                    "co.", "ltd", "inc", "shenzhen", "guangzhou", "shanghai", "ningbo"
                ]
                msg_lower = user_message.lower()
                if any(t in msg_lower for t in search_triggers) or len(user_message.split()) >= 3:
                    web_results = await WebSearchService.search(user_message, max_results=3)
                    web_context = WebSearchService.format_search_context(web_results)
            except Exception as e:
                print(f"[LLM Web Search Error] {e}")

        # ترکیب پرامپت با داده‌های زنده وب
        enhanced_system_prompt = system_prompt
        if web_context:
            enhanced_system_prompt += f"\n\n{web_context}"

        messages = [{"role": "system", "content": enhanced_system_prompt}]

        if chat_history:
            for item in chat_history[-6:]:
                messages.append(item)
        
        messages.append({"role": "user", "content": user_message})

        # 2. ارسال به DeepSeek API (V3 / R1)
        if settings.DEEPSEEK_API_KEY:
            try:
                async with httpx.AsyncClient(timeout=45.0) as client:
                    resp = await client.post(
                        "https://api.deepseek.com/chat/completions",
                        headers={"Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}"},
                        json={
                            "model": model_name,
                            "messages": messages,
                            "temperature": 0.6
                        }
                    )
                    if resp.status_code == 200:
                        return resp.json()["choices"][0]["message"]["content"]
                    else:
                        print(f"[DeepSeek Status] {resp.status_code}: {resp.text[:150]}")
            except Exception as e:
                print(f"[LLM Error] DeepSeek API call failed: {e}")

        # 3. پشتیبان Gemini API
        if settings.GEMINI_API_KEY:
            try:
                async with httpx.AsyncClient(timeout=45.0) as client:
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={settings.GEMINI_API_KEY}"
                    contents = [{"role": "user", "parts": [{"text": f"{enhanced_system_prompt}\n\nUser Question: {user_message}"}]}]
                    resp = await client.post(url, json={"contents": contents})
                    if resp.status_code == 200:
                        return resp.json()["candidates"][0]["content"]["parts"][0]["text"]
            except Exception as e:
                print(f"[LLM Error] Gemini API call failed: {e}")

        # 4. پشتیبان OpenAI GPT-4o
        if settings.OPENAI_API_KEY:
            try:
                async with httpx.AsyncClient(timeout=45.0) as client:
                    resp = await client.post(
                        "https://api.openai.com/v1/chat/completions",
                        headers={"Authorization": f"Bearer {settings.OPENAI_API_KEY}"},
                        json={
                            "model": "gpt-4o-mini",
                            "messages": messages,
                            "temperature": 0.6
                        }
                    )
                    if resp.status_code == 200:
                        return resp.json()["choices"][0]["message"]["content"]
            except Exception as e:
                print(f"[LLM Error] OpenAI API call failed: {e}")

        # 5. موتور تحلیل هوشمند داخلی (Fallback)
        return LLMService._expert_domain_fallback(enhanced_system_prompt, user_message)

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
