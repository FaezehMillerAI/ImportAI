"""
FastAPI Server Entry Point for ImportAI Pro Platform
Unified single-process execution for Web Portal, REST APIs, Telegram Bot & Social Webhooks
"""
import uvicorn
import asyncio
from fastapi import FastAPI, Depends, HTTPException, Query, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import Optional, List
import os

from config import settings
from database import init_db, get_db, Lead, AuditRecord, ChatLog
from agents.orchestrator import MasterOrchestrator
from services.qcc_verifier import verify_china_company
from services.hs_database import search_hs_code
from services.pi_scanner_service import PIScannerService
from services.instagram_content_generator import InstagramContentGenerator
from services.instagram_dm_agent import InstagramDMAgent
from services.linkedin_content_generator import LinkedInContentGenerator
from services.linkedin_messaging_agent import LinkedInMessagingAgent
from services.telegram_bot import start_telegram_bot_async
from services.currency_rate_service import CurrencyRateService
from services.game_ai_master import GameAIMaster

# Initialize DB tables
init_db()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="پلتفرم هوشمند مشاوره، اعتبارسنجی و سورسینگ واردات با ایجنت‌های هوش مصنوعی"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup lifecycle: Launch Telegram bot automatically in unified single process
@app.on_event("startup")
async def startup_event():
    print("🚀 [System Startup] Initializing unified background services...")
    asyncio.create_task(start_telegram_bot_async())

# Request Models
class ChatRequest(BaseModel):
    message: str
    agent_id: Optional[str] = "auto"
    session_id: Optional[str] = "default_session"
    lang: Optional[str] = "fa"

class LeadCreateRequest(BaseModel):
    full_name: str
    phone: str
    company_name: Optional[str] = None
    target_goods: Optional[str] = None
    capital_usd: Optional[float] = 50000.0
    industry: Optional[str] = "machinery"
    source: Optional[str] = "web"

class CompanyAuditRequest(BaseModel):
    company_name: str
    uscc_code: Optional[str] = None

class SimCalcRequest(BaseModel):
    capital_usd: float = 50000.0
    industry: str = "medical"
    supplier_type: str = "verified"
    qc_requested: bool = True
    currency_type: str = "nima"

class InstagramDMWebhookRequest(BaseModel):
    user_id: str
    username: str
    message: str

class LinkedInMessageWebhookRequest(BaseModel):
    profile_id: str
    full_name: str
    company: str
    message: str

class PIScanTextRequest(BaseModel):
    raw_text: str
    filename: Optional[str] = "Proforma.txt"

# Request Models for Advanced Superpower Modules
class WarRoomRequest(BaseModel):
    target_product: str
    target_country: Optional[str] = "China"
    capital_usd: Optional[float] = 50000.0
    lang: Optional[str] = "fa"

class CorridorFeasibilityRequest(BaseModel):
    origin_country: str
    goods_type: str
    urgency: Optional[str] = "normal"

class CreateInvoiceRequest(BaseModel):
    service_id: str
    client_name: str
    client_phone: str
    payment_method: Optional[str] = "shetab"

class CurrencyConvertRequest(BaseModel):
    amount: float
    from_currency: Optional[str] = "USD"
    to_currency: Optional[str] = "TOMAN"

class VerifyPaymentRequest(BaseModel):
    invoice_number: str
    tracking_code: str
    method: Optional[str] = "shetab"

class GameAITurnRequest(BaseModel):
    user_action: str
    character_name: Optional[str] = "تاجر کارکشته سنتی"
    target_product: Optional[str] = "خط تولید صنعتی"
    capital_gold: Optional[int] = 100000
    deal_health: Optional[int] = 100
    reputation: Optional[int] = 50
    turn_count: Optional[int] = 1
    history: Optional[List[Dict[str, str]]] = None

# API Endpoints
@app.get("/api/health")
def health_check():
    return {"status": "online", "version": settings.VERSION, "project": settings.PROJECT_NAME}

@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="پیام نمی‌تواند خالی باشد")

    result = await MasterOrchestrator.route_request(req.message, req.agent_id, req.lang)
    return result

@app.post("/api/war-room")
async def trade_war_room_endpoint(req: WarRoomRequest):
    if not req.target_product.strip():
        raise HTTPException(status_code=400, detail="نام کالا نمی‌تواند خالی باشد")
    from services.warroom_orchestrator import TradeWarRoomEngine
    result = await TradeWarRoomEngine.run_war_room_session(req.target_product, req.target_country, req.capital_usd, req.lang)
    return result

@app.get("/api/corridors/catalog")
def get_corridors_catalog():
    from services.corridor_intelligence_service import CorridorIntelligenceService
    return CorridorIntelligenceService.get_all_borders_catalog()

@app.post("/api/corridors/feasibility")
async def analyze_corridor_feasibility(req: CorridorFeasibilityRequest):
    if not req.goods_type.strip():
        raise HTTPException(status_code=400, detail="نوع کالا الزامی است")
    from services.corridor_intelligence_service import CorridorIntelligenceService
    result = await CorridorIntelligenceService.analyze_corridor_feasibility(req.origin_country, req.goods_type, req.urgency)
    return result

@app.get("/api/payment/packages")
def get_payment_packages():
    from services.payment_service import PaymentService
    return PaymentService.get_service_packages()

@app.post("/api/payment/create-invoice")
def create_payment_invoice(req: CreateInvoiceRequest):
    if not req.client_phone.strip():
        raise HTTPException(status_code=400, detail="شماره تماس الزامی است")
    from services.payment_service import PaymentService
    result = PaymentService.create_invoice(req.service_id, req.client_name, req.client_phone, req.payment_method)
    return result

@app.post("/api/payment/verify")
def verify_payment_endpoint(req: VerifyPaymentRequest):
    from services.payment_service import PaymentService
    result = PaymentService.verify_payment(req.invoice_number, req.tracking_code, req.method)
    return result

@app.post("/api/audit")
async def audit_company(req: CompanyAuditRequest):
    if not req.company_name.strip():
        raise HTTPException(status_code=400, detail="نام شرکت نمی‌تواند خالی باشد")
    
    from services.qcc_verifier import verify_china_company_async
    result = await verify_china_company_async(req.company_name, req.uscc_code)
    return result

@app.post("/api/scan-pi")
async def scan_pi_text_endpoint(req: PIScanTextRequest):
    if not req.raw_text.strip():
        raise HTTPException(status_code=400, detail="متن پیش‌فاکتور نمی‌تواند خالی باشد")
    
    result = await PIScannerService.analyze_proforma(req.raw_text, req.filename)
    return result

@app.post("/api/scan-pi-upload")
async def scan_pi_upload_endpoint(file: UploadFile = File(...)):
    content = await file.read()
    filename = file.filename or "Uploaded_Document.pdf"
    
    raw_text = ""
    if filename.lower().endswith(".pdf"):
        raw_text = PIScannerService.extract_text_from_pdf(content)
    else:
        # Image or text file
        try:
            raw_text = content.decode("utf-8", errors="ignore")
        except Exception:
            raw_text = f"Scanned Commercial Invoice image {filename}"

    if not raw_text.strip():
        raw_text = f"Scanned Commercial Proforma Invoice {filename}"

    result = await PIScannerService.analyze_proforma(raw_text, filename)
    return result

@app.get("/api/hs-search")
def hs_code_search(q: str = Query(..., description="عنوان کالا یا کد HS")):
    results = search_hs_code(q)
    return {"query": q, "results": results}

@app.post("/api/leads")
def create_lead(req: LeadCreateRequest):
    db_gen = get_db()
    db = next(db_gen)
    try:
        new_lead = Lead(
            full_name=req.full_name,
            phone=req.phone,
            company_name=req.company_name,
            target_goods=req.target_goods,
            capital_usd=req.capital_usd,
            industry=req.industry,
            source=req.source
        )
        db.add(new_lead)
        db.commit()
        db.refresh(new_lead)
        return {"status": "success", "lead_id": new_lead.id, "message": "درخواست مشاوره با موفقیت ثبت شد"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/gamification/calculate")
def calculate_sim(req: SimCalcRequest):
    capital = req.capital_usd
    fob = capital * 0.83
    freight = 3200.0
    qc = 450.0 if req.qc_requested else 0.0
    customs = capital * 0.097
    
    profit = capital * 0.248
    risk_level = "LOW"
    advice = "✅ انتخاب هوشمندانه! اعتبارسنجی ثبتی QCC و بازرسی کیفیت PSI، ریسک کلاه‌برداری را خنثی کرد."

    if req.supplier_type == "cheap":
        risk_level = "HIGH"
        profit = capital * 0.08
        advice = "⚠️ هشدار ریسک بالا: انتخاب تامین‌کننده ثبت‌نشده بدون اعتبارسنجی QCC، ممکن است منجر به خسارت سنگین مالی شود!"
    elif not req.qc_requested:
        risk_level = "MEDIUM"
        advice = "💡 توصیه: با حذف بازرسی کیفیت PSI، احتمال دریافت ۱۰٪ تا ۳۰٪ کالای دارای نقص فنی وجود دارد."

    return {
        "capital_usd": capital,
        "fob_cost": fob,
        "freight_cost": freight,
        "qc_cost": qc,
        "customs_cost": customs,
        "profit_usd": profit,
        "profit_percent": (profit / capital) * 100,
        "risk_level": risk_level,
        "advice": advice
    }

# Instagram Automation Endpoints
@app.get("/api/instagram/generate-daily-posts")
async def generate_instagram_posts():
    posts = await InstagramContentGenerator.generate_daily_content()
    return {"status": "success", "count": len(posts), "posts": posts}

@app.post("/api/instagram/webhook/dm")
async def instagram_dm_webhook(req: InstagramDMWebhookRequest):
    reply = await InstagramDMAgent.handle_incoming_dm(req.user_id, req.username, req.message)
    return {"user_id": req.user_id, "reply": reply}

# LinkedIn B2B Automation Endpoints
@app.get("/api/linkedin/generate-daily-posts")
async def generate_linkedin_posts():
    posts = await LinkedInContentGenerator.generate_daily_b2b_posts()
    return {"status": "success", "count": len(posts), "posts": posts}

@app.post("/api/linkedin/webhook/message")
async def linkedin_message_webhook(req: LinkedInMessageWebhookRequest):
    reply = await LinkedInMessagingAgent.handle_incoming_linkedin_message(req.profile_id, req.full_name, req.company, req.message)
    return {"profile_id": req.profile_id, "reply": reply}

# Live Iranian Currency & Exchange Rates Endpoints
@app.get("/api/currency/rates")
async def get_live_currency_rates():
    """
    Returns real-time currency exchange rates from Nobitex / Wallex / Iranian Market
    """
    rates = await CurrencyRateService.get_live_rates()
    return rates

@app.post("/api/currency/convert")
async def convert_currency_rate(req: CurrencyConvertRequest):
    """
    Convert any trade amount using real-time Iranian exchange rates
    """
    res = await CurrencyRateService.convert_currency(req.amount, req.from_currency, req.to_currency)
    return res

# DeepSeek Dynamic AI Gamification & RPG Dungeon Master
@app.post("/api/game/ai-turn")
async def game_ai_turn_endpoint(req: GameAITurnRequest):
    """
    Simulates real-time arbitrary trade decisions, negotiations, customs dilemmas and boss fights via DeepSeek.
    """
    result = await GameAIMaster.process_turn(
        user_action=req.user_action,
        character_name=req.character_name,
        target_product=req.target_product,
        capital_gold=req.capital_gold,
        deal_health=req.deal_health,
        reputation=req.reputation,
        turn_count=req.turn_count,
        history=req.history
    )
    return result

# Serve Index Page with Anti-Cache Headers
@app.get("/")
def read_root():
    index_path = os.path.join(os.path.dirname(__file__), "index.html")
    if os.path.exists(index_path):
        return FileResponse(
            index_path,
            headers={
                "Cache-Control": "no-cache, no-store, must-revalidate, max-age=0",
                "Pragma": "no-cache",
                "Expires": "0"
            }
        )
    return {"message": "Welcome to ImportAI Pro API"}

if __name__ == "__main__":
    print(f"🚀 Starting ImportAI Pro FastAPI server on http://{settings.HOST}:{settings.PORT}")
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)
