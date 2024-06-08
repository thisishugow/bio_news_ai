import os
from typing import Literal
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import GoogleGenerativeAI, HarmBlockThreshold, HarmCategory
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from web_condenser_ai.tools.selenium_url_loader import SeleniumURLLoader
from web_condenser_ai.utils import keys
from web_condenser_ai.prompts.industrial_analyst import (
    content_divider,
    prompt_system_role, 
    prompt_user_task
)
from web_condenser_ai.prompts.sys import sys_role

__all__ = [
    "generate_digestion", 
    "read_from_urls",
]

class LLMNotSupportedError(Exception):
    pass

def get_gemini_llm(model_name:str="gemini-pro")->GoogleGenerativeAI:
    llm = GoogleGenerativeAI(
        model=model_name,
        google_api_key=keys.GOOGLE_API_KEY,
        safety_settings={
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        },
    )
    return llm

def get_openai_llm(model_name:Literal["gpt-3.5-turbo", "gpt-4-turbo"]="gpt-3.5-turbo",)->ChatOpenAI:
    llm = ChatOpenAI(model_name=model_name, openai_api_key=keys.OPENAI_API_KEY)
    return llm


def generate_digestion(
    contents: list[str] | str, 
    tone:Literal['casual', 'confident', 'professor', ]='casual',
    use_llm:Literal['google', 'openai', 'gemini']='gemini',
    model_name:str=None, 
    minutes_to_read:int=1, 
    extra_prompts:str=None,
    role:str='Social Media Writer',
    resp_lang: list[str] | str = ["english", "繁體中文 (台灣)"], 
)->str:
    """
    Generate a digestion from a list of content strings or a single content string.
    
    Args:
        contents (list[str] | str): A list of content strings or a single content string.
        tone (Literal['casual', 'confident', 'professor']): The tone of the generated digest. 
                                                            Can be 'casual', 'confident', or 'professor'. to 'casual'.
        use_llm (Literal['google', 'openai', 'gemini']): the llm to use. Default='gemini'.
        model_name (str): use a specific model from the llm provider. Default gemini/google is "gemini-pro", and openai is "gpt-3.5-turbo"
    
    Returns:
        str: The generated weekly digest.
    """
    if use_llm.lower() in ['google','gemini']:
        if model_name is None:
            model_name = "gemini-1.5-pro"
        llm = get_gemini_llm(model_name)
    elif use_llm.lower() == 'openai':
        if model_name is None:
            model_name = "gpt-3.5-turbo"
        llm = get_openai_llm(model_name)
    else:
        raise LLMNotSupportedError(f'"{use_llm}" is not supported. ')
    prompt_template = ChatPromptTemplate.from_messages([
        ('system', prompt_system_role),
        ('user', prompt_user_task)
    ])
    parser = StrOutputParser()
    chain = prompt_template | llm | parser
    
    if isinstance(contents, str):
        contents = [contents, ]

    if isinstance(resp_lang, list):
        resp_lang = ', '.join(resp_lang)

    resp =  chain.invoke({
        "content": content_divider.join(contents),
        "tone": tone, 
        "extra_prompts": extra_prompts,
        "minutes_to_read": minutes_to_read, 
        "sys_role": sys_role.get(role, 'social media writer in a industrial analysis firm.'), 
        "resp_lang": resp_lang, 
    })
    return resp

def read_from_urls(urls:list[str]|str):
    """
    Reads content from a list of URLs or a single URL.
    
    Args:
        urls (list[str] | str): A list of URLs or a single URL to read content from.
        
    Returns:
        generator: A generator that yields the page content from each URL.
    """
    if isinstance(urls, str):
        urls = [urls,]

    browser = os.environ.get("SELENIUM_WEB_DRIVER", 'chrome')
    if browser=='chromium':
        loader = SeleniumURLLoader(urls=urls, browser=browser, executable_path='/usr/bin/chromedriver')
    else:
        loader = SeleniumURLLoader(urls=urls, browser=browser)
    data = loader.load()
    return (
        d.page_content 
        for d in data
    )

