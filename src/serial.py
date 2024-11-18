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

# On Ubuntu, see: /etc/sysctl.d/10-kernel-hardening.conf
# https://unix.stackexchange.com/a/390187

def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)

def serials():
    '''!input'''
    out = get_stdout(['dmesg'])
    devs = set()
    for m in re.findall(r'(tty[a-zA-Z_0-9]+)', out):
        if Path(f'/dev/{m}').exists():
            devs.add(m)
    with_serial = []
    without_serial = []
    for dev in devs:
        try:
            out = get_stdout(['/bin/udevadm', 'info', f'--name=/dev/{dev}'])
        except:
            out = ''
        s = re.search(r'ID_SERIAL_SHORT\s*=\s*([^\n]*)', out)
        if s:
            serial = s.group(1).lstrip('0 ')
            with_serial.append(f'{dev} - {serial}')
        else:
            without_serial.append(dev)
    for dev in natural_sort(with_serial):
        print(dev)
    for dev in natural_sort(without_serial):
        print(dev)

def term_window():
    '''!
    input
        Where place the terminal
        VSCode panel
        New window
    '''
    pass

def term_inner():
    '''!
    term_inner, hide
    '''
    exec(['minicom', '-b', '115200', '-c', 'on', '-D', '/dev/' + argv(0)], allow_fail=True)
    print('Press ENTER to continue')
    input()

def term():
    '''!
    terminal, icon=terminal-powershell
        "${input:term_window}" ${input:serials}
        { "runOptions": { "instanceLimit": 100 }, "presentation": { "close": true } }
    '''
    if argv(0) == 'New window':
        exec(['gnome-terminal', '--no-environment', '-t', argv(1), '--', vscode_dir / 'cmd', 'term_inner', argv(1)])
    else:
        exec(['minicom', '-b', '115200', '-c', 'on', '-D', '/dev/' + argv(1)], allow_fail=True)
