from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PAYPAL_CLIENT_ID: str
    PAYPAL_CLIENT_SECRET: str
    GEMINI_API_KEY: str
    ZAPIER_WEBHOOK_URL: str = ""
    PAYPAL_BASE_URL: str = "https://api-m.sandbox.paypal.com"
    DATABASE_URL: str = "sqlite:///./ledgerpulse.db"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
