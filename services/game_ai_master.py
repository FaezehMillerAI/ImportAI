"""
DeepSeek AI Dynamic Gamification & Trade RPG Dungeon Master
Powers real-time arbitrary scenarios, custom negotiations, boss fights, and trade simulations.
"""
import json
import re
from typing import Dict, Any, List
from config import settings
from services.llm_service import LLMService

GAME_MASTER_SYSTEM_PROMPT = """
تو «استاد بازی هوشمند تجارت بین‌الملل (DeepSeek Trade Dungeon Master)» هستی.
کاربر یک تاجر، بازرگان یا کارآفرین ایرانی است که می‌خواهد کالایی را از چین، ترکیه یا امارات سورس کند و به ایران وارد کند.

وظیفه تو این است که بر اساس اقدام دلخواه و آزادانه کاربر، یک ماجراجویی تعاملی، هیجان‌انگیز و کاملاً واقعی تجاری شبیه‌سازی کنی.
شخصیت‌هایی که بازی می‌کنی:
- مدیر فروش کارخانه چینی (Mr. Zhang یا Ms. Chen) در گوانگژو/شنزن/نینگبو
- مدیر صرافی و حواله‌دار ارزی در دبی/تهران
- فورواردر خطوط کشتیرانی کانتینری و ریلی سرخس
- ارزیاب و کارشناس رسمی گمرک شهید رجایی یا غرب تهران
- ایجنت هوش مصنوعی تحلیل ریسک QCC

قوانین بازی:
۱. کاربر ممکن است هر نوع استراتژی بنویسد (مثلاً چانه‌زنی تهاجمی، تقلب، بازرسی صوری، تغییر مسیر، پرداخت یوان نقدی و...).
۲. تو باید عواقب دقیق بازرگانی، مالیاتی، گمرکی و امنیتی این حرکت را محاسبه کنی.
۳. پاسخ را حتماً و فقط در قالب یک شیء معتبر JSON با ساختار زیر خروجی بده (بدون هیچ متن اضافی قبل یا بعد از JSON):

{
  "actor_name": "نام شخصیتی که الان با کاربر صحبت می‌کند (مثلاً: مدیر کارخانه آقای چانگ)",
  "actor_role": "Factory Boss / Customs Officer / Exchange Broker / Logistics / Risk Auditor",
  "dialogue": "دیالوگ واقع‌گرایانه، جذاب و حرفه‌ای شخصیت در پاسخ به حرکت کاربر به فارسی روان (با تکه‌کلام‌های انگلیسی یا چینی تجاری مثل FOB, EXW, LC, TT)",
  "narrative": "توضیح کوتاه ۱ تا ۲ خطی اتفاقی که در صحنه بازی رخ داد و پیامد تاکتیک کاربر.",
  "gold_delta": عدد تغییرات سرمایه (مثلاً +15000 یا -8000 یا 0),
  "hp_delta": عدد تغییر سلامت معامله بین -50 تا +20 (مثلاً -15 در صورت ریسک، یا +10 در صورت تصمیم امن),
  "rep_delta": عدد تغییر اعتبار تجاری بین -20 تا +20,
  "sound_effect": "coin_gain" | "damage" | "alert" | "victory" | "neutral",
  "game_status": "PLAYING" | "VICTORY" | "BANKRUPT" | "SEIZED",
  "dilemma_prompt": "سوال یا چالش اصلی بعدی که کاربر باید برایش تصمیم بگیرد چیست؟",
  "suggested_actions": [
    "پیشنهاد تاکتیکی ۱ برای حرکت بعدی",
    "پیشنهاد تاکتیکی ۲ برای حرکت بعدی",
    "پیشنهاد تاکتیکی ۳ برای حرکت بعدی"
  ]
}
"""

class GameAIMaster:

    @classmethod
    async def process_turn(
        cls,
        user_action: str,
        character_name: str,
        target_product: str,
        capital_gold: int,
        deal_health: int,
        reputation: int,
        turn_count: int,
        history: List[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Processes an arbitrary user move using DeepSeek AI and returns the next dynamic RPG turn.
        """
        user_context = f"""
وضعیت فعلی بازی (راند {turn_count}):
- شخصیت بازیکن: {character_name}
- کالای هدف: {target_product}
- موجودی فعلی سرمایه: {capital_gold:,} دلار
- درصد سلامت معامله (Deal HP): {deal_health}%
- اعتبار بازار: {reputation}/100

اقدام و تصمیم بازیکن:
«{user_action}»
"""

        raw_response = await LLMService.generate_response(
            system_prompt=GAME_MASTER_SYSTEM_PROMPT,
            user_message=user_context,
            chat_history=history or [],
            model_name="deepseek-chat",
            enable_web_search=False
        )

        # Parse JSON from response
        parsed = cls._extract_json(raw_response)
        if not parsed:
            # Fallback robust parser
            parsed = {
                "actor_name": "مدیر فروش کارخانه گوانگژو (Mr. Zhang)",
                "actor_role": "Factory Boss",
                "dialogue": f"پیشنهاد شما را بررسی کردیم! در مورد «{target_product}»، اگر سفارش نقدی و با تیراژ بالا باشد می‌توانیم با شرایط FOB شنزن ۵٪ تخفیف اعمال کنیم.",
                "narrative": "کارخانه چینی به پیشنهاد شما پاسخ داد و خواستار صدور پروفرما رسمی شد.",
                "gold_delta": 0,
                "hp_delta": 0,
                "rep_delta": 5,
                "sound_effect": "coin_gain",
                "game_status": "PLAYING",
                "dilemma_prompt": "آیا پیش‌فاکتور را برای اعتبارسنجی QCC ارسال می‌کنید یا مستقیماً پیش‌پرداخت را واریز می‌نمایید؟",
                "suggested_actions": [
                    "درخواست استعلام رسمی QCC و انطباق حساب شرکتی",
                    "چانه‌زنی برای تحویل در دبی یا اضافه کردن بازرسی PSI",
                    "واریز ۳۰٪ پیش‌پرداخت با حواله رسمی بانکی"
                ]
            }

        # Calculate new dynamic totals
        new_gold = max(0, capital_gold + parsed.get("gold_delta", 0))
        new_hp = max(0, min(100, deal_health + parsed.get("hp_delta", 0)))
        new_rep = max(0, min(100, reputation + parsed.get("rep_delta", 0)))

        if new_hp <= 0 or new_gold <= 0:
            parsed["game_status"] = "BANKRUPT"
        elif turn_count >= 5 and new_hp > 50:
            parsed["game_status"] = "VICTORY"

        parsed["new_gold"] = new_gold
        parsed["new_hp"] = new_hp
        parsed["new_rep"] = new_rep
        parsed["turn_count"] = turn_count + 1

        return parsed

    @classmethod
    def _extract_json(cls, text: str) -> Dict[str, Any]:
        try:
            # Clean markdown codeblocks
            cleaned = text.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            elif cleaned.startswith("```"):
                cleaned = cleaned[3:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            cleaned = cleaned.strip()

            return json.loads(cleaned)
        except Exception:
            # Try regex match
            match = re.search(r'\{.*\}', text, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(0))
                except Exception:
                    pass
        return None
