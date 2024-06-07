# web-condenser-ai

A generative AI app creates condensed buzz, powered by [Langchain](https://www.langchain.com) and [Streamlit](https://streamlit.io). Paste web links and condense them!

## Quickstart

### Setup
**Option 1 (Run from scratch)**
```bash
git clone https://github.com/thisishugow/web_condenser_ai.git
cd web_condenser_ai 
poetry install; # install the dependencies. 
touch .env
```
**Option 2 (Simple install)**  
Download the distribution from [releases](https://github.com/thisishugow/web_condenser_ai/releases)
```bash
pip install web_condenser_ai.whl
touch .env
```


Then you should add the API Key of OpenAI and Gemini, and your password for login into `.env` file. Example: 

```
OPENAI_API_KEY=sk-wewifo4woivm48jiome***1i3co23iFJ3imomcu81ecke2cN
GOOGLE_API_KEY=AIeic8cuemYuemvo28vh316s0a9HW72kdwopwet
PASSWORD=mypassword

# You can add the app title and favicon by setting following variables
APP_TITLE=BioNews.ai
FAVICON=favicon.ico
```


**Start app**
```bash
python -m web_condenser_ai
```

Then visit http://localhost:8501 to see your app. 

## Usage
1. Login. Then open sidebar and set how many article sources you need. 
2. Select model and tone. 
3. Paste urls and submit! 
> Notes:  
> You might be billed by the model provider. Make sure you have enough deposits. 

## Developers 

- Customize prompts  
  - Prompts are stored in `web_condenser_ai/prompts`. 
  - Prompts are grouped by **System role**.
  - To customize the prompts, you will need the basic concepts of [LCEL](https://python.langchain.com/v0.2/docs/concepts/#langchain-expression-language-lcel)
  - Edit your own chain in `web_condenser_ai/tools/digest.py`
- Streamlit UI locates in `web_condenser_ai/app.py`. 


## Powered by
- [Langchain](https://www.langchain.com)
- [Streamlit](https://streamlit.io)

**Follow us on [Linkedin](https://www.linkedin.com/company/colosscious) and [Facebook](https://www.facebook.com/people/Colosscious/61556549523278) for updates!**
