import os 
import sys
import argparse
from streamlit.web.cli import main
from web_condenser_ai import app

_TARGET = app.__file__

def arg_handler():
    parser = argparse.ArgumentParser(
        description="start your web_condenser_app",
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
    args = parser.parse_args()
    os.environ["SELENIUM_WEB_DRIVER"] = args.data_loader
    os.environ["STREAMLIT_APP_LAYOUT"] = args.layout

    if logo:= args.logo:
        os.environ["STREAMLIT_APP_LOGO"] = logo

    if favicon:= args.favicon:
        os.environ["STREAMLIT_APP_FAVICON"] = favicon

    if app_name:= args.app_name:
        os.environ["STREAMLIT_APP_NAME"] = app_name

if __name__ == '__main__':
    arg_handler()
    sys.argv = ["streamlit", "run", _TARGET, "--theme.primaryColor", "#274C77" ,"--theme.secondaryBackgroundColor", "#E7ECEF"]
    sys.exit(main())