import re
import time
import streamlit as st
from web_condenser_ai.tools.degest import generate_digestion, read_from_urls
from web_condenser_ai.utils import keys, conf
from web_condenser_ai.__version__ import __version__ as VERSION

PASSWORD:str = keys.PASSWORD
APP_TITLE = conf.APP_TITLE
FAVICON = conf.FAVICON
refresh_url_input = 0

if st.session_state.get("urls_num", None) is None:
    st.session_state["urls_num"] = 1

def login():
    login_form = st.empty()
    with login_form.form("login"):
        st.write("### Login")
        st.text_input("Password", type="password", key="password", label_visibility='collapsed')
        st.form_submit_button("Login", )

    input_login_pswd = st.session_state.get("password", '')
    if input_login_pswd==PASSWORD:
        login_form.empty()
    elif len(input_login_pswd)==0:
        st.info('Login with the password.')
    else:
        st.error((
            "Invalid password. Please try again.\n "
            "Contact [admin](mailto:bd.info@colosscious.com) (bd.info@colosscious.com) "
            "for more."
         ))
            
def _clean_url(url):
    return re.sub(r'^[\'\"\s]+|[\'\"\s]+$', '', url)


def run_ai():
    content_urls:list[str] = []
    for i in range(st.session_state["urls_num"]):
        _key = f"url_{i+1}"
        if _url:=st.session_state[_key]:
            content_urls.append(_clean_url(_url))

    llm, model_name = tuple(st.session_state['llm'].split(': '))
    t0 = time.time()
    with st.spinner("Scraping contents from urls ..."):
        data = read_from_urls(content_urls)
    t1 = time.time()
    st.success(f"Contents downloaded. (⏱️ {round(t1-t0, 2)}s)", icon="✅")
    with st.spinner("AI is digesting ..."):
        resp = generate_digestion(
            contents=data, 
            tone=st.session_state['tone'],
            use_llm=llm,
            model_name=model_name,
        )
    t2 = time.time()
    st.success(f"Contents condensed. (⏱️ {round(t2-t1, 2)}s)", icon="✅")
    
    st.divider()
    st.info(resp)
    st.code(resp, language='markdown')

def urls_form():
    for i in range(st.session_state["urls_num"]):
        _i = i +1
        _ = st.text_input(
            label=f"News URL {_i}", 
            placeholder=f"Please input URL {_i}", 
            label_visibility='collapsed', 
            key=f"url_{_i}"
        ) 
    submitted = st.form_submit_button("Submit", )
    
    if submitted:
        run_ai()


def init_page_cnf():
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon=FAVICON,  # 使用 Emoji 作为图标
    )
    st.title("🐋💬 "+APP_TITLE)
    
def side_bar():
    with st.sidebar:
        st.header('Configure')
        cnt = st.number_input(label="Number of News", min_value=1, max_value=10, step=1, key='number_input', )
        cnt = int(cnt)
        st.session_state["urls_num"] = cnt
        options = [
            "Google: gemini-pro",
            "Google: gemini-1.5-pro",
            "Google: gemini-1.5-flash",
            "OpenAI: gpt-3.5-turbo",
            "OpenAI: gpt-4-turbo",
        ]
        st.selectbox("LLM", options=options, index=1, key='llm')
        st.selectbox("Tone", options=['casual', 'confident', 'professor'], index=1, key='tone')
        

def footer():
    styles = {
        "position": "fixed",
        "bottom": "0px",
        "left": "0px",
        "color":"rgb(49, 51, 63)",
        "padding": "10px 0 10px 0",
        "background-color": "rgb(240, 242, 246)",
        "width": "100%",
        "text-align": "center"
    }
    style_to_str = '; '.join([
        f"{k}: {v}" for k, v in styles.items()
    ])
    footer_snippet = (
        f"""<div style="{style_to_str}">"""
        f"""<a href="https://github.com/thisishugow/web_condenser_ai" target="_blank">WebCondenser v{VERSION}</a> | """
        "Jun 2024 | "
        """<a  href="https://www.linkedin.com/in/thisisyuwang" target="_blank">Hugo Wang</a>"""
        "<div style=\"font-size: 12px\">"
            "<a style=\"color: rgb(49, 51, 63)\" href=\"https://www.colosscious.com/home\" target=\"_blank\">"
                "Copyright © 2024 Colosscious Co., Ltd."
            "</a>"
        "</div>"
        "</div>"
    )
    st.markdown(footer_snippet, unsafe_allow_html=True) 


def main():
    init_page_cnf()
    login()
    if st.session_state.get('password', 0)==PASSWORD:
        side_bar()
        with st.form("myform"):
            st.write(f"**Source URLs**")
            urls_form()

    footer()
    


if __name__ == "__main__":
    main()