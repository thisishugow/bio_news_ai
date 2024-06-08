import os 
import sys
import argparse
from streamlit.web.cli import main
from web_condenser_ai import app

_TARGET = app.__file__

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="start your ",
    )
    parser.add_argument(
        "--data-loader",
        choices=["chrome", "chromium",], 
        default="chrome", 
        required=False,
    )
    args = parser.parse_args()
    os.environ["SELENIUM_WEB_DRIVER"] = args.data_loader

    sys.argv = ["streamlit", "run", _TARGET]
    sys.exit(main())