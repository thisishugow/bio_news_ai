from web_condenser_ai.__version__ import __version__

def dict_to_style(style:dict):
    return '; '.join([
        f"{k}: {v}" for k, v in style.items()
    ])

footer_style = {
    "position": "fixed",
    "bottom": "0px",
    "left": "0px",
    "color":"rgb(49, 51, 63)",
    "padding": "10px 0 10px 0",
    "background-color": "#E7ECEF",
    "width": "100%",
    "text-align": "center", 
}

footer = (
    f"""<div style="{dict_to_style(footer_style)}">"""
    f"""<a href="https://github.com/thisishugow/web_condenser_ai" target="_blank">WebCondenser.ai v{__version__}</a> | """
    "Jun 2024 | "
    """<a  href="https://www.linkedin.com/in/thisisyuwang" target="_blank">Hugo Wang</a>"""
    "<div style=\"font-size: 12px\">"
        "<a style=\"color: rgb(49, 51, 63)\" href=\"https://www.colosscious.com/home\" target=\"_blank\">"
            "Copyright © 2024 Colosscious Co., Ltd."
        "</a>"
    "</div>"
    "</div>"
)