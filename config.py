import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/risk_cession_db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    HMAC_SECRET_KEY = os.getenv("HMAC_SECRET_KEY", "super_secret_default_key")
    FLASK_APP = os.getenv("FLASK_APP", "app.py")
    FLASK_ENV = os.getenv("FLASK_ENV", "development")