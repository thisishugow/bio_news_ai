import os 
import sys
import argparse
from streamlit.web.cli import main
from web_condenser_ai import app
from web_condenser_ai.utils import arg_handler

_TARGET = app.__file__

if __name__ == '__main__':
    arg_handler()
    sys.argv = ["streamlit", "run", _TARGET, "--theme.primaryColor", "#274C77" ,"--theme.secondaryBackgroundColor", "#E7ECEF"]
    sys.exit(main())