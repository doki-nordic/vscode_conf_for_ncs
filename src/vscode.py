
'''
[[commands]]
'''

import sys
import re
import json
import shutil
import time
import tempfile
from common import *
import textwrap

def source_zephyr():
    '''!
    vscode: source this zephyr environment, icon=server-process
    '''
    exec(['gnome-terminal', '--no-environment', '--', vscode_dir / 'cmd', 'source_zephyr_inner', root_dir / 'zephyr/zephyr-env.sh'])

def source_zephyr_inner():
    '''!
    source_zephyr_inner, hide
    '''
    for i in range(10):
        out = get_stdout(['wmctrl', '-l', '-x'])
        if out.find('code.Code') < 0:
            break
        exec(['wmctrl', '-x', '-c', 'code.Code'], allow_fail=True)
        time.sleep(0.5)
    else:
        print('Failed to clode VSCode window', file=sys.stderr)
    exec(textwrap.dedent(f'''
        source {argv(0)} || true
        source {root_dir}/.venv/bin/activate || true
        unset GNOME_TERMINAL_SCREEN
        code
        '''), bash=True)
