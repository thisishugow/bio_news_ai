import os
from dotenv import load_dotenv

if os.path.isfile('./.env'):
    dotenv_file = './.env'
else:
    dotenv_file = None

    
load_dotenv(dotenv_file)

APP_TITLE = os.environ.get("APP_TITLE", 'WebCondenser.ai')
FAVICON = os.environ.get("FAVICON", '')
LOGO = os.environ.get('LOGO', None)
LLM:list[str] = [
    "Google: gemini-pro",
    "Google: gemini-1.5-pro",
    "Google: gemini-1.5-flash",
    "OpenAI: gpt-3.5-turbo",
    "OpenAI: gpt-4-turbo",
    "OpenAI: gpt-4o"
] 


__all__ = [
    "APP_TITLE",
    "FAVICON",
    "LLM",
    "LOGO", 
]