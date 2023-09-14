
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
        export LD_LIBRARY_PATH={root_dir}/.venv/bin:{root_dir}/.venv/lib:$LD_LIBRARY_PATH
        unset GNOME_TERMINAL_SCREEN
        code
        '''), bash=True)

def instance_title():
    '''!input'''
    all = list(mru_list('instanceTitles'))
    all.append('[[input]]')
    print('\n'.join(all))
    return 0

def instance():
    '''!
    vscode: new instance, icon=empty-window
        "${input:instance_title}"
    '''
    title = mru_update('instanceTitles', opt_input(argv(0)))
    for instance in range(10):
        print(f'Cheking instance slot {instance}')
        dir = Path.home() / 'vscode_instances' / str(instance)
        dir.mkdir(parents=True, exist_ok=True)
        out = get_stdout(['code', '-s', '--user-data-dir', dir])
        if out.find('Please run it again') >= 0:
            print(f'Slot {green(instance)} is free.')
            break
    else:
        print(f'All slots are busy.')
        return 1
    settings: Path = dir / 'User/settings.json'
    print(f'Copying settings to {settings}')
    shutil.copy(Path.home() / '.config/Code/User/settings.json', settings)
    text = settings.read_text()
    new_text = re.sub(r'("window.title"\s*:\s*"[^"]*)MAIN', r'\1' + title, text, flags=re.IGNORECASE)
    if new_text == text:
        print(textwrap.dedent(f'''
            {red("WARNING !!!!")}
            Set "window.title" setting in main VS Code instance and restart all instances to correctly show window title!!!
            Go to File - Preferences - Settings, search for "window.title" and add "{green("MAIN")}" title anywhere.
            '''))
    settings.write_text(new_text)
    exec(f'''
        export VS_CODE_INSTANCE={instance}
        export export LD_LIBRARY_PATH={root_dir}/.venv/bin:{root_dir}/.venv/lib:$LD_LIBRARY_PATH
        code --user-data-dir {dir}
        ''', bash=True)
