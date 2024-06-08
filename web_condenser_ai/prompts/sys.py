sys_role:dict[str, dict] = {
    "Social Media Writer": 'social media writer in a industrial analysis firm.',
    "Column Writer": 'column writer of a industrial magazine.', 
    "Textbook Author": 'professor composing a textbook for your master students.', 
}

resp_lang:list = [
    "English", 
    "繁體中文", 
    "Japanese", 
    "Korean", 
    "Spanish",
    "French", 
    "Tiếng Việt",
    "แบบไทย (Thai)",
] 

default_resp_lang:list[str] = [
    "English", 
    "繁體中文", 
]

__all__ = [
    'sys_role', 
    "resp_lang", 
    "default_resp_lang", 
]