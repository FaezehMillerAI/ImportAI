import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float, JSON
from sqlalchemy.orm import declarative_base, sessionmaker
from config import settings

engine = create_engine(
    settings.DATABASE_URL, 
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=False, index=True)
    company_name = Column(String(255), nullable=True)
    target_goods = Column(Text, nullable=True)
    capital_usd = Column(Float, default=50000.0)
    industry = Column(String(100), default="machinery")
    source = Column(String(50), default="web") # web, telegram, instagram, whatsapp
    status = Column(String(50), default="new") # new, contacted, in_sourcing, contracted
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class AuditRecord(Base):
    __tablename__ = "audit_records"

    id = Column(Integer, primary_key=True, index=True)
    company_name_en = Column(String(255), index=True)
    uscc_code = Column(String(100), index=True)
    registration_capital = Column(String(100))
    establishment_date = Column(String(50))
    litigation_count = Column(Integer, default=0)
    risk_score = Column(String(50), default="LOW")
    raw_data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class ChatLog(Base):
    __tablename__ = "chat_logs"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), index=True)
    agent_name = Column(String(50))
    user_message = Column(Text)
    agent_response = Column(Text)
    channel = Column(String(50), default="web")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
