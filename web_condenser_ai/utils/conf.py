import os
from dotenv import load_dotenv

if os.path.isfile('./.env'):
    dotenv_file = './.env'
else:
    dotenv_file = None

    
load_dotenv(dotenv_file)

APP_TITLE = os.environ.get("APP_TITLE", 'WebCondenser.ai')
FAVICON = os.environ.get("FAVICON", '')

__all__ = [
    "APP_TITLE",
    "FAVICON",
]