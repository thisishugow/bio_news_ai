import re
import time
import streamlit as st
from web_condenser_ai.tools.degest import generate_digestion, read_from_urls
from web_condenser_ai.utils import keys, conf, html_snippets
from web_condenser_ai.prompts.sys import sys_role, resp_lang, default_resp_lang
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
    st.session_state["perf_content_scraping"] = round(t1-t0, 2)
    tmp_perf1 = st.empty()
    tmp_perf2 = st.empty()

    tmp_perf1.success(f"Contents downloaded. (⏱️ {round(t1-t0, 2)}s)", icon="✅")
    with st.spinner("AI is digesting ..."):
        resp = generate_digestion(
            contents=data, 
            tone=st.session_state['tone'],
            use_llm=llm,
            model_name=model_name,
            extra_prompts=st.session_state.get("extra_input", None),
            role=st.session_state.get('sys_role',),
            minutes_to_read=st.session_state.get("minutes_to_read", 1),
            resp_lang=st.session_state.get("resp_lang", default_resp_lang),
        )
    t2 = time.time()

    st.session_state["perf_ai_requesting"] = round(t2-t1, 2)
    tmp_perf2.success(f"Contents condensed. (⏱️ {round(t2-t1, 2)}s)", icon="✅")
    st.session_state["response"] = resp
    tmp_perf1.empty()
    tmp_perf2.empty()

def show_resp():
    if resp:=st.session_state.get("response", None):
        st.toggle("Show raw", key="show_raw_resp",)
        if st.session_state.get("show_raw_resp", False):
            st.code(resp, language='markdown')
        else:
            st.info(resp)

def urls_form():
    with st.form("myform"):
        st.write(f"**Source URLs**")
        if st.session_state.get("enable_extra_prompt", False):
            extra_prompt()
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

def extra_prompt():
    st.text_area(
        label="Extra Prompts", 
        placeholder="(Optional) Add your own extra prompts.", 
        key="extra_input",
        label_visibility="collapsed"
    )


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
        options = conf.LLM
        st.selectbox("LLM", options=options, index=1, key='llm')
        st.selectbox("Tone", options=['casual', 'confident', 'teaching'], index=1, key='tone')
        st.selectbox("System Role", options=sys_role.keys(), index=0, key='sys_role')
        st.slider("Minutes of Reading", min_value=1, max_value=15, value=1, key="minutes_to_read")
        st.multiselect(label='Language', options=resp_lang, default=default_resp_lang, key='resp_lang', )
        st.toggle("Enable Extra Prompts", key="enable_extra_prompt")
        
def footer():
    st.markdown(html_snippets.footer, unsafe_allow_html=True) 

def perf_notification():
    if perf1:=st.session_state.get("perf_content_scraping", 0):
        st.success(f"Contents downloaded. (⏱️ {perf1}s)", icon="✅")

    if perf2:=st.session_state.get("perf_ai_requesting", 0):
        st.success(f"Contents condensed. (⏱️ {perf2}s)", icon="✅")


def main():
    init_page_cnf()
    login()
    if st.session_state.get('password', 0)==PASSWORD:
        side_bar()
        urls_form()
        perf_notification()
        show_resp()

    footer()
    


if __name__ == "__main__":
    main()