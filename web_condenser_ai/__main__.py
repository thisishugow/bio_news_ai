import subprocess
from web_condenser_ai import app
from web_condenser_ai.utils import arg_handler

_TARGET = app.__file__

if __name__ == '__main__':
    arg_handler()

    cmds = ["streamlit", "run", "--theme.primaryColor", "#274C77" ,"--theme.secondaryBackgroundColor", "#E7ECEF", "--server.enableCORS", "true",  f'{_TARGET}', ]
    try:
        subprocess.run(cmds)
    except KeyboardInterrupt as e:
        print('<crtl+c> detected. Terminated.')
    except Exception as e:
        print(e)