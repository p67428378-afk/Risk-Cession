import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """
    Configuration class for the application.
    Loads environment variables and sets default values.
    """
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/cession_db")
    HMAC_SECRET = os.getenv("HMAC_SECRET", "supersecretkey")
    # Define other configuration variables here
