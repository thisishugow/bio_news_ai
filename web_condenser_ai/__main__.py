import sys
from streamlit.web.cli import main
from web_condenser_ai import app

_TARGET = app.__file__

if __name__ == '__main__':
    sys.argv = ["streamlit", "run", _TARGET]
    sys.exit(main())