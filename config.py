import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('HMAC_SECRET_KEY') or 'a_default_secret_key_if_not_set'
