import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file if present
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

class Settings:
    PROJECT_NAME: str = "ImportAI Pro - Smart Sourcing & Agent Ecosystem"
    VERSION: str = "1.0.0"
    ENV: str = os.getenv("ENV", "development")
    PORT: int = int(os.getenv("PORT", 8000))
    HOST: str = os.getenv("HOST", "0.0.0.0")

    # AI Keys
    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

    # Telegram Bot Token
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")

    # QCC China Audit API
    QCC_API_KEY: str = os.getenv("QCC_API_KEY", "")
    QCC_SECRET: str = os.getenv("QCC_SECRET", "")

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./import_agents.db")

settings = Settings()
