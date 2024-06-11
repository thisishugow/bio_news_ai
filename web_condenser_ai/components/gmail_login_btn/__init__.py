import os 

import streamlit.components.v1 as components

__PUBLUC = os.path.join(os.path.dirname(__file__), "public")

gmail_login_btn = (
    components.declare_component(
        "gmail_login_btn_comp",
        path=__PUBLUC,
    )
)