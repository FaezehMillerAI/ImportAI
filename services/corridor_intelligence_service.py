"""
Corridor & Border Feasibility Intelligence Service
Comprehensive routing and status feasibility for Sea, Rail, Road, and Air border crossings into Iran.
Supports real-time risk assessment, transit time calculation, customs bottlenecks, and dynamic crisis fallbacks.
"""
from typing import Dict, List, Optional
import asyncio
from services.web_search_service import WebSearchService

# پایگاه جامع اطلاعات مرزها و کریدورهای ورودی به ایران
BORDERS_DATABASE = {
    "sea": [
        {
            "id": "bandar_abbas",
            "name_fa": "بندر شهید رجایی (بندرعباس)",
            "name_en": "Bandar Abbas (Shahid Rajaee Port)",
            "type": "دریایی (Sea Port)",
            "origin_routes": "چین (شنژن، نینگبو، شانگهای)، هند (ناوا شوا)، امارات (جبل علی)",
            "transit_time_days": "۲۲ الی ۳۰ روز از بنادر اصلی چین",
            "capacity": "ظرفیت کانتینری بالا (FCL & LCL)",
            "cost_index": "اقتصادی‌ترین روش برای بارهای سنگین و حجیم (کانتینر ۲۰ و ۴۰ فوت)",
            "customs_type": "گمرک تخصصی واردات ماشین‌آلات، مواد پتروشیمی، خودرو و کالاهای عمومی",
            "current_status": "فعال (Active) - با در نظر گرفتن نوبت ترخیصیه و انبارداری بنادر",
            "fallback_routes": ["بندر چابهار (شهید بهشتی)", "کریدور ریلی سرخس از چین", "حمل ترکیبی دریایی-هوایی از دبی"]
        },
        {
            "id": "chabahar",
            "name_fa": "بندر شهید بهشتی (چابهار)",
            "name_en": "Chabahar Port (Shahid Beheshti)",
            "type": "دریایی اقیانوسی (Ocean Sea Port)",
            "origin_routes": "هند، عمان، جنوب شرق آسیا و چین",
            "transit_time_days": "۱۸ الی ۲۵ روز از هند و چین",
            "capacity": "ترانزیت اقیانوسی بدون محدودیت تنگه هرمز",
            "cost_index": "تخفیف‌های ویژه سود بازرگانی و معافیت‌های ترانزیتی",
            "customs_type": "منطقه آزاد چابهار و گمرک شهید بهشتی",
            "current_status": "فعال (Active) - بدون ترافیک معطلی اسکله",
            "fallback_routes": ["بندرعباس", "بندر بوشهر"]
        },
        {
            "id": "caspian_ports",
            "name_fa": "بنادر شمال (انزلی، امیرآباد، نوشهر)",
            "name_en": "Caspian Sea Ports (Anzali, Amirabad, Nowshahr)",
            "type": "دریایی خزر (Caspian Sea)",
            "origin_routes": "روسیه (آستاراخان)، قزاقستان (آکتائو)، ترکمنستان",
            "transit_time_days": "۳ الی ۷ روز در حوضه خزر",
            "capacity": "فله‌بر، جنرال کارگو و رورو (Ro-Ro)",
            "cost_index": "بسیار مناسب برای غلات، چوب، آهن‌آلات و مواد خام صنعتی",
            "customs_type": "گمرکات تخصصی شمال کشور و مناطق آزاد انزلی و امیرآباد",
            "current_status": "فعال (Active) - تابع شرایط آب‌وهوایی دریای خزر",
            "fallback_routes": ["مرز ریلی آستارا", "مرز جاده‌ای آستارا"]
        }
    ],
    "rail": [
        {
            "id": "china_iran_train",
            "name_fa": "قطار باری مستقیم چین - ایران (مرز ریلی سرخس / اینچه‌برون)",
            "name_en": "China-Kazakhstan-Turkmenistan-Iran Silk Road Railway (Sarakhs / Incheh Borun)",
            "type": "ریلی ترانزیتی (International Freight Rail)",
            "origin_routes": "ایستگاه‌های یی‌وو (Yiwu)، شی‌آن (Xi'an)، چنگدو (Chengdu) چین به تهران",
            "transit_time_days": "۱۴ الی ۱۸ روز (دو برابر سریع‌تر از حمل دریایی!)",
            "capacity": "کانتینری منظم و ایمن در تمام فصول سال",
            "cost_index": "حدود ۳۰٪ گران‌تر از دریایی اما ۵۰٪ سریع‌تر؛ بسیار مناسب قطعات خط تولید و بارهای باارزش",
            "customs_type": "گمرک ریلی سرخس و گمرک غرب / شهید رجایی تهران (ایستگاه آپرین)",
            "current_status": "فعال و عملیاتی (Active Silk Road Route)",
            "fallback_routes": ["حمل دریایی کانتینری بندرعباس", "حمل هوایی فرودگاه امام خمینی"]
        },
        {
            "id": "razi_rail",
            "name_fa": "مرز ریلی رازی (ایران - ترکیه)",
            "name_en": "Razi Rail Border (Iran - Turkey)",
            "type": "ریلی اروپایی (European Rail Link)",
            "origin_routes": "ترکیه، آلمان، ایتالیا و اروپای مرکزی به ایران",
            "transit_time_days": "۷ الی ۱۲ روز از ترکیه و اروپا",
            "capacity": "واگن‌های مسقف و کانتینری",
            "cost_index": "بسیار اقتصادی‌تر از حمل جاده‌ای برای بارهای حجیم از اروپا",
            "customs_type": "گمرک رازی خوی و ترخیص در گمرک سهلان یا تهران",
            "current_status": "فعال (Active)",
            "fallback_routes": ["مرز جاده‌ای بازرگان", "مرز سرو ارومیه"]
        }
    ],
    "road": [
        {
            "id": "bazargan",
            "name_fa": "مرز زمینی بازرگان (ایران - ترکیه / اروپا)",
            "name_en": "Bazargan Land Border (Main Europe-Turkey Gateway)",
            "type": "جاده‌ای و ترانزیت تیر (TIR Road Border)",
            "origin_routes": "ترکیه، بلغارستان، آلمان، ایتالیا و لهستان",
            "transit_time_days": "۵ الی ۱۰ روز از استانبول؛ ۱۰ الی ۱۶ روز از اروپای غربی",
            "capacity": "کامیون‌های چادری، یخچالی، کفی و ترافیکی (بوژی)",
            "cost_index": "هزینه متناسب با سرعت تحویل درب کارخانه (Door to Door)",
            "customs_type": "مهم‌ترین گمرک زمینی تجاری کشور با تجهیزات کامل ایکس‌ری",
            "current_status": "فعال با نوبت‌دهی منظم گمرک بازرگان",
            "fallback_routes": ["مرز سرو (ارومیه)", "مرز پلدشت", "مرز ریلی رازی"]
        },
        {
            "id": "nordooz_jolfa",
            "name_fa": "مرز نوردوز و جلفا (ارمنستان و آذربایجان / اوراسیا)",
            "name_en": "Nordooz & Jolfa Borders (Armenia / Eurasia Economic Union)",
            "type": "جاده‌ای اوراسیا (EAEU Corridor)",
            "origin_routes": "روسیه، گرجستان، ارمنستان و قفقاز",
            "transit_time_days": "۴ الی ۸ روز",
            "capacity": "کامیونی و ترانزیتی",
            "cost_index": "شامل تعرفه‌های ترجیحی موافقت‌نامه تجارت آزاد ایران و اتحادیه اوراسیا",
            "customs_type": "گمرک نوردوز و گمرک منطقه آزاد ارس",
            "current_status": "فعال (Active)",
            "fallback_routes": ["مرز آستارا", "بنادر شمالی انزلی"]
        }
    ],
    "air": [
        {
            "id": "ikac_cargo",
            "name_fa": "گمرک تجاری فرودگاه بین‌المللی امام خمینی (IKAC Cargo)",
            "name_en": "Imam Khomeini Airport Cargo Customs (IKAC)",
            "type": "هوایی سریع (Air Cargo Express)",
            "origin_routes": "چین (گوانگژو، پکن، شنژن)، امارات (دبی)، قطر (دوحه)، ترکیه (استانبول)",
            "transit_time_days": "۳ الی ۵ روز کاری (سریع‌ترین روش ممکن)",
            "capacity": "پالت‌های هوایی، سمپل‌های دارویی، قطعات الکترونیک، تجهیزات حساس آزمایشگاهی و قطعات یدکی فوری",
            "cost_index": "محاسبه بر اساس وزن حجمی (Volumetric Weight)؛ بالاترین هزینه و بالاترین سرعت",
            "customs_type": "ترخیص شبانه‌روزی کالاهای دارویی، پزشکی، قطعات مخابراتی و هوایی",
            "current_status": "فعال و عملیاتی کامل ۲۴/۷",
            "fallback_routes": ["حمل ترکیبی دریایی-هوایی از دبی (Sea-Air)", "قطار باری سریع‌السیر ابریشم"]
        },
        {
            "id": "payam_cargo",
            "name_fa": "گمرک منطقه ویژه اقتصادی و فرودگاه پیام",
            "name_en": "Payam Special Economic Zone & Airport Cargo",
            "type": "هوایی تخصصی IT و صنایع پیشرفته",
            "origin_routes": "امارات، چین و ترکیه",
            "transit_time_days": "۳ الی ۵ روز",
            "capacity": "بارهای فله هوایی، قطعات کامپیوتر و صنایع هوایی",
            "cost_index": "تسهیلات ویژه مناطق ویژه اقتصادی و معافیت‌های ترانزیتی",
            "customs_type": "گمرک تخصصی تجهیزات الکترونیک، مخابرات و سرور",
            "current_status": "فعال (Active)",
            "fallback_routes": ["گمرک فرودگاه امام خمینی (ره)"]
        }
    ]
}

class CorridorIntelligenceService:
    @staticmethod
    async def analyze_corridor_feasibility(origin_country: str, goods_type: str, urgency: str = "normal", budget_priority: str = "economic") -> dict:
        """
        امکان‌سنجی دقیق انتخاب کریدورهای ورود کالا به ایران و پیشنهاد گزینه‌های جایگزین در شرایط بحران
        """
        origin_lower = origin_country.lower().strip()
        goods_lower = goods_type.lower().strip()
        
        # 1. استعلام زنده وضعیت مرزها از وب
        web_search_query = f"وضعیت ترخیص و مرزهای تجاری ایران {origin_country} حمل {goods_type}"
        web_news = await WebSearchService.search(web_search_query, max_results=2)
        live_notes = WebSearchService.format_search_context(web_news)

        recommendations = []
        best_route = None
        alternative_route = None

        # منطق تحلیل هوشمند سورسینگ و لجستیک
        if "چین" in origin_lower or "china" in origin_lower:
            if urgency == "urgent" or "فوری" in urgency:
                best_route = BORDERS_DATABASE["air"][0] # IKAC
                alternative_route = BORDERS_DATABASE["rail"][0] # China Train (Sarakhs)
                rationale_fa = "به دلیل فوریت زمانی، حمل هوایی به گمرک فرودگاه امام خمینی سریع‌ترین راه است (۳ الی ۵ روز). در صورت محدودیت بار حجیم، قطار باری ابریشم سرخس بهترین جایگزین با نصف زمان حمل دریایی است."
            elif "سنگین" in goods_lower or "خط تولید" in goods_lower or "دستگاه" in goods_lower or "پلیمر" in goods_lower:
                best_route = BORDERS_DATABASE["sea"][0] # Bandar Abbas
                alternative_route = BORDERS_DATABASE["rail"][0] # Sarakhs Rail
                rationale_fa = "برای ماشین‌آلات و خطوط تولید سنگین، حمل کانتینری دریایی به بندر شهید رجایی بندرعباس اقتصادی‌ترین گزینه است. در شرایط ترافیک بنادر یا اضطرار، قطار باری ریلی ایستگاه سرخس راهکار جایگزین بدون ریسک طوفان دریایی است."
            else:
                best_route = BORDERS_DATABASE["sea"][0]
                alternative_route = BORDERS_DATABASE["rail"][0]
                rationale_fa = "حمل کانتینری دریایی از بنادر شنژن/نینگبو به بندرعباس گزینه استاندارد است."

        elif "ترکیه" in origin_lower or "turkey" in origin_lower or "اروپا" in origin_lower or "europe" in origin_lower:
            best_route = BORDERS_DATABASE["road"][0] # Bazargan
            alternative_route = BORDERS_DATABASE["rail"][1] # Razi Rail
            rationale_fa = "برای واردات از ترکیه و اروپا، مرز زمینی بازرگان مسیر شماره یک کامیونی است (۵ الی ۱۰ روز). در زمان صف‌های سنگین تریلر در مرز، کریدور ریلی رازی خوی با کمترین تأخیر جایگزین می‌شود."

        elif "روسیه" in origin_lower or "russia" in origin_lower or "قزاقستان" in origin_lower:
            best_route = BORDERS_DATABASE["sea"][2] # Caspian
            alternative_route = BORDERS_DATABASE["road"][1] # Nordooz / Astara
            rationale_fa = "مسیر دریایی خزر (بندر امیرآباد و انزلی) همراه با تعرفه موافقت‌نامه تجارت آزاد اوراسیا بهینه‌ترین گزینه است."

        else:
            best_route = BORDERS_DATABASE["sea"][0]
            alternative_route = BORDERS_DATABASE["air"][0]
            rationale_fa = "حمل استاندارد کانتینری بندرعباس با مسیر اضطراری فرودگاه امام خمینی پیشنهاد می‌شود."

        return {
            "status": "success",
            "origin_country": origin_country,
            "goods_type": goods_type,
            "urgency": urgency,
            "best_primary_route": best_route,
            "contingency_fallback_route": alternative_route,
            "strategic_rationale_fa": rationale_fa,
            "all_borders_matrix": BORDERS_DATABASE,
            "live_intelligence_context": live_notes
        }

    @staticmethod
    def get_all_borders_catalog() -> dict:
        """کاتالوگ کامل تمام مرزها و کریدورهای کشور"""
        return BORDERS_DATABASE
