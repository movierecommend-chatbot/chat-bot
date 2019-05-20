#!C:\Users\anyin\PycharmProjects\chat\venv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'ngrok==0.0.1','console_scripts','frp.py'
__requires__ = 'ngrok==0.0.1'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('ngrok==0.0.1', 'console_scripts', 'frp.py')()
    )
