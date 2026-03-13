import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    HMAC_SECRET_KEY = os.getenv("HMAC_SECRET_KEY", "default_secret_key")
    DATABASE_URI = "in_memory"