"""
دیتابیس دامنه‌ای HS Code، تعرفه‌های گمرکی و شرایط واردات در ایران
"""

HS_DATABASE = [
    {
        "hs_code": "4011.10.00",
        "title_fa": "لاستیک و تایرهای بادی جدید از کائوچو (سواری و باری)",
        "category": "rubber_tires",
        "keywords": ["لاستیک", "تایر", "کائوچو", "rubber", "tire", "tires"],
        "customs_duty_percent": 32.0,
        "nima_eligible": True,
        "import_permit": "دفتر صنایع خودرو و حمل و نقل صمت + استاندارد اجباری",
        "priority_group": "گروه ۲۲ (ارز نیما / تالار دوم)",
        "recommended_origin": "چین (Shandong / Qingdao), ویتنام, تایلند"
    },
    {
        "hs_code": "9018.49.00",
        "title_fa": "تجهیزات، ابزارها و دستگاه‌های دندان‌پزشکی و پزشکی",
        "category": "medical",
        "keywords": ["دندانپزشکی", "پزشکی", "یونیت", "سی تی اسکن", "medical"],
        "customs_duty_percent": 5.0,
        "nima_eligible": True,
        "import_permit": "اداره کل تجهیزات و ملزومات پزشکی (آیمد IMED)",
        "priority_group": "گروه ۲۱ (اولویتی)",
        "recommended_origin": "چین (Shenzhen / Shanghai), آلمان, کره جنوبی"
    },
    {
        "hs_code": "8479.89.90",
        "title_fa": "ماشین‌آلات صنعتی، خطوط تولید و دستگاه‌های مکانیکی",
        "category": "machinery",
        "keywords": ["خط تولید", "ماشین آلات", "دستگاه", "صنعتی", "مکانیکی", "machinery"],
        "customs_duty_percent": 5.0,
        "nima_eligible": True,
        "import_permit": "دفتر ماشین‌آلات و تجهیزات صمت",
        "priority_group": "گروه ۲۲",
        "recommended_origin": "چین (Guangdong / Jiangsu), ترکیه, آلمان"
    },
    {
        "hs_code": "3901.10.00",
        "title_fa": "پلی‌اتیلن، مواد اولیه پلاستیک، پلیمر و مواد شیمیایی",
        "category": "raw_materials",
        "keywords": ["پلی اتیلن", "پلیمر", "شیمیایی", "مواد اولیه", "پلاستیک", "polymer"],
        "customs_duty_percent": 10.0,
        "nima_eligible": True,
        "import_permit": "دفتر صنایع شیمیایی و پلیمری صمت",
        "priority_group": "گروه ۲۲",
        "recommended_origin": "چین, امارات, کره جنوبی"
    },
    {
        "hs_code": "8517.79.00",
        "title_fa": "قطعات، مدارات و لوازم جانبی محصولات دیجیتال و موبایل",
        "category": "electronics",
        "keywords": ["موبایل", "دیجیتال", "لوازم جانبی", "الکترونیک", "قطعات", "electronics"],
        "customs_duty_percent": 15.0,
        "nima_eligible": False,
        "import_permit": "دفتر صنایع برق و الکترونیک صمت",
        "priority_group": "گروه ۲۳ (ارز حاصل از صادرات)",
        "recommended_origin": "چین (Shenzhen / Guangzhou)"
    }
]

def search_hs_code(query: str):
    query_lower = query.lower().strip()
    results = []
    for item in HS_DATABASE:
        # Check in keywords or title or hs_code
        if (any(kw in query_lower for kw in item.get("keywords", [])) or 
            query_lower in item["title_fa"].lower() or 
            query_lower in item["hs_code"]):
            results.append(item)
    return results
