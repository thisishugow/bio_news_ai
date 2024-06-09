import argparse
import os

from streamlit.runtime import get_instance
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.runtime.session_manager import SessionClient 

from ._logger import *


def arg_handler():
    parser = argparse.ArgumentParser(
        description="start your web_condenser_ai app",
    )
    parser.add_argument(
        "--data-loader",
        help="The webdriver for selenium. ",
        choices=["chrome", "chromium",], 
        type=str, 
        default="chrome", 
        required=False,
    )
    parser.add_argument(
        "--app-name",
        help="The name of the app. ",
        type=str, 
        required=False,
    )
    parser.add_argument(
        "--layout",
        help="The layout of the app. ",
        choices=["wide", "centered"], 
        type=str, 
        default="centered", 
        required=False,
    )
    parser.add_argument(
        "--logo",
        help="The file path of the logo.",
        type=str, 
        required=False,
    )
    parser.add_argument(
        "--favicon",
        help="The file path of favicon.",
        type=str, 
        required=False,
    )

    parser.add_argument(
        "--log-path",
        help="The file path of logging.",
        type=str, 
        required=False,
    )

    args = parser.parse_args()
    os.environ["SELENIUM_WEB_DRIVER"] = args.data_loader
    os.environ["STREAMLIT_APP_LAYOUT"] = args.layout
   

    if logo:= args.logo:
        os.environ["STREAMLIT_APP_LOGO"] = logo

    if favicon:= args.favicon:
        os.environ["STREAMLIT_APP_FAVICON"] = favicon

    if app_name:= args.app_name:
        os.environ["STREAMLIT_APP_NAME"] = app_name

    if log_path:= args.log_path:
        os.environ["STREAMLIT_LOG_PATH"] = log_path

def get_runtime_ctx()->SessionClient:
    request = (
        get_instance()
        .get_client(
            get_script_run_ctx().session_id
        )
    )

    return request


