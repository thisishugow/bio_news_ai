sys_role:dict[str, dict] = {
    "Social Media Writer": 'social media writer in a industrial analysis firm.',
    "Column Writer": 'column writer of a industrial magazine.', 
    "Textbook Author": 'professor composing a textbook for your master students.', 
}

resp_lang:list = [
    "繁體中文 (Mandarin TW)", 
    "English", 
    "日本語 (Japanese)", 
    "한국어 (Korean)", 
    "Español (Spanish)",
    "Français (French)", 
    "Tiếng Việt (Vietnamese)",
    "แบบไทย (Thai)",
    "Deutsch (German)", 
    "Türkçe (Turkish)", 
    "bahasa Indonesia (Indonesian)", 
    "Русский (Russian)", 
    "Italiano (Italian)",
] 

default_resp_lang:list[str] = [
    "繁體中文 (Mandarin TW)", 
    "English", 
]

__all__ = [
    'sys_role', 
    "resp_lang", 
    "default_resp_lang", 
]