# 🚀 راهنمای راه‌اندازی و عملیاتی‌سازی پلتفرم ایجنت‌های هوشمند واردات (ImportAI Pro)

این پروژه پلتفرم کامل عملیاتی برای جذب مشتری، گیمیفیکیشن، اعتبارسنجی ثبتی کارخانجات چین (QCC) و مشاوره سورسینگ بین‌المللی با ایجنت‌های هوش مصنوعی است.

---

## 🛠️ ۱. پیش‌نیازها و نصب سریع (Quick Start)

### گام اول: ورود به دایرکتوری پروژه
```bash
cd /Users/fs525/Desktop/Saeedeh
```

### گام دوم: نصب پیش‌نیازها (در صورت نیاز)
```bash
pip install -r requirements.txt
```

### گام سوم: تنظیم فایل .env
فایل `.env.example` را به `.env` کپی کنید و کلیدهای خود را وارد نمایید:
```bash
cp .env.example .env
```
در فایل `.env`:
- `OPENAI_API_KEY`: کلید API هوش مصنوعی (در صورت عدم ورود، سیستم از موتور پیش‌فرض هوشمند استفاده می‌کند).
- `TELEGRAM_BOT_TOKEN`: توکن ربات تلگرام دریافت‌شده از `BotFather@`.

---

## 💻 ۲. اجرا و تست پلتفرم

### الف) اجرای سرور اصلی (FastAPI + Web Portal):
```bash
python3 main.py
```
یا با uvicorn:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

پس از اجرای سرور:
- 🌐 **پورتال تعاملی وب:** [http://localhost:8000](http://localhost:8000)
- 📑 **مستندات تعاملی API (Swagger):** [http://localhost:8000/docs](http://localhost:8000/docs)

### ب) اجرای ربات تلگرام (به صورت همزمان یا جداگانه):
```bash
python3 services/telegram_bot.py
```

---

## 📁 ۳. ساختار فایل‌های پروژه

- `main.py`: نقطه ورود FastAPI، هندلر APIهای چت، اعتبارسنجی QCC، لیدها و محاسبات گیمیفیکیشن.
- `config.py`: مدیریت تنظیمات مرکزی و فایل `.env`.
- `database.py`: دیتابیس SQLite برای ذخیره لیدها، چت‌ها و گزارش‌های اعتبارسنجی.
- `agents/`:
  - `orchestrator.py`: ارکستریتور مرکزی و مسیریاب هوشمند درخواست‌ها.
  - `edulead.py`: ایجنت آموزشی و مجری گیمیفیکیشن ۵۰ هزار دلاری.
  - `sourcing.py`: ایجنت تعیین کد HS و سورسینگ کالا.
  - `risk_audit.py`: ایجنت اعتبارسنجی حقوقی کارخانجات چین.
  - `logistics.py`: ایجنت حمل، ترخیص و ارز نیما.
  - `sales.py`: ایجنت ثبت درخواست مشاوره و قراردادها.
- `services/`:
  - `telegram_bot.py`: سرویس ربات تلگرام با منوهای اینلاین تعاملی.
  - `qcc_verifier.py`: موتور استعلام رسمی روزنامه ثبتی و پرونده‌های قضایی چین.
  - `hs_database.py`: دیتابیس تعرفه گمرک و کدهای HS ایران.
  - `llm_service.py`: موتور سرویس هوش مصنوعی (OpenAI / Gemini / Fallback).
- `index.html`: پورتال تعاملی وب با ظاهر مدرن Glassmorphism و متصل به APIهای سرور.

---

## 🌐 ۴. استقرار روی سرور واقعی (Production VPS Deployment)

برای اجرای ۲۴/۷ روی سرور لینوکس (Ubuntu):

```bash
# نصب systemd service
sudo nano /etc/systemd/system/importai.service
```

محتوای فایل service:
```ini
[Unit]
Description=ImportAI Pro Agent Platform
After=network.target

[Service]
User=root
WorkingDirectory=/path/to/Saeedeh
ExecStart=/usr/bin/python3 main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

سپس سرویس را فعال کنید:
```bash
sudo systemctl daemon-reload
sudo systemctl start importai
sudo systemctl enable importai
```

---
*توسعه داده شده بر اساس مستر پلن جامع ایجنت‌های هوشمند واردات.*
