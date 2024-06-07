import os
from dotenv import load_dotenv

if os.path.isfile('./.env'):
    dotenv_file = './.env'
else:
    dotenv_file = None

    
load_dotenv(dotenv_file)

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", None)
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", None)
PASSWORD = os.environ.get("PASSWORD", None)

__all__ = [
    "GOOGLE_API_KEY",
    "OPENAI_API_KEY", 
    "PASSWORD",
]