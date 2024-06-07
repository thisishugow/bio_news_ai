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

def get_openai_llm(model:Literal["gpt-3.5-turbo", "gpt-4-turbo"]="gpt-3.5-turbo",)->ChatOpenAI:
    llm = ChatOpenAI(model_name=model, openai_api_key=keys.OPENAI_API_KEY)
    return llm


def generate_digestion(
    contents: list[str] | str, 
    tone:Literal['casual', 'confident', 'professor', ]='casual',
    use_llm:Literal['google', 'openai', 'gemini']='gemini',
    model_name:str=None, 
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
    resp =  chain.invoke({
        "content": content_divider.join(contents),
        "tone": tone, 
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

    browser = 'chrome'
    if os.environ.get('USE_CHROMIUM', False)=='yes':
        browser = 'chromium'
        loader = SeleniumURLLoader(urls=urls, browser=browser, executable_path='/usr/bin/chromedriver')
    else:
        loader = SeleniumURLLoader(urls=urls, browser=browser)
    data = loader.load()
    return (
        d.page_content 
        for d in data
    )

