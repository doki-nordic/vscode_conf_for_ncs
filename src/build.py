
'''
[[commands]]
'''

import sys
import re
import json
import shutil
from common import *

def boards():
    '''!input'''
    west_boards = []
    for line in get_stdout(['west', 'boards']).splitlines():
        west_boards.append(line.strip())
    nordic_boards = filter(lambda x: x.lower().startswith('nrf'), west_boards)
    nrf_boards = filter(lambda x: x.lower().find('nrf') > 0, west_boards)
    all = list(mru_list('boards'))
    all.extend(sorted(x for x in nordic_boards if x not in all))
    all.extend(sorted(x for x in nrf_boards if x not in all))
    all.extend(sorted(x for x in west_boards if x not in all))
    all.append('[[input]]')
    print('\n'.join(all))
    return 0

def get_board():
    '''!input, one'''
    print(get_value('board'))
    return 0

def set_board():
    '''!
    example: change board, icon=circuit-board
        "${input:boards}"
    '''
    val = set_value('board', mru_update('boards', opt_input(argv(0))))
    print(f'Current board: {green(val)}')
    return 0

def samples():
    '''!input'''
    all = list(mru_list('samples'))
    for file in root_dir.glob('**/sample.y?ml'):
        file = str(file.relative_to(root_dir).parent)
        if file not in all:
            all.append(file)
    all.append('[[from current CMakeLists.txt]]')
    all.append('[[input]]')
    print('\n'.join(all))
    return 0

def get_sample():
    '''!input, one'''
    print(get_value('sample'))
    return 0

def set_sample():
    '''!
    example: change folder, icon=folder-opened
        "${input:samples}" ${fileDirname}
    '''
    val = opt_input(argv(0))
    if val == '[[from current CMakeLists.txt]]':
        val = argv(1)
    val = str(Path(val).resolve().relative_to(root_dir))
    val = set_value('sample', mru_update('samples', val))
    print(f'Current sample: {green(val)}\n\n')
    return 0

def build_args(name='build_args'):
    '''!input'''
    all = list(mru_list(name))
    all.append('[[empty]]')
    all.append('[[input]]')
    print('\n'.join(x.replace('"', '\\"') for x in all))
    return 0

def flash_args():
    '''!input'''
    return build_args('flash_args')

def set_build_args(name='build_args'):
    '''!
    example: change arguments, icon=ellipsis
        "${input:build_args}"
    '''
    if argv(0) == '[[input]]':
        val = json.dumps(convert_bash_options(opt_input(argv(0))))
    else:
        val = opt_input(argv(0))
    val = set_value(name, mru_update(name, val))
    print(f'Build arguments: {green(val)}\n\n')
    return 0

def set_flash_args():
    '''!
    example: flash arguments, icon=ellipsis
        "${input:flash_args}"
    '''
    return set_build_args('flash_args')

def build_dir_name():
    board = get_value('board')
    return re.sub(r'[^\w_-]', '_', f'build_{board}')

def get_build_dir_name():
    '''!input, one'''
    print(build_dir_name())
    return 0

def get_build_info():
    sample_dir = Path(get_value('sample'))
    board = get_value('board')
    build_dir = build_dir_name()
    print(f'Sample {green(sample_dir.stem)} for {green(board)}\n')
    print(f'Build directory: {green(build_dir)}\n')
    args = ['west', 'build', '-b', board]
    dir_args = ['-d', build_dir]
    cmd = get_value('build_args')
    if cmd and cmd.strip() != '':
        cmd_args = ['--'] + json.loads(cmd)
    else:
        cmd_args = []
    return (args, dir_args, cmd_args, build_dir, sample_dir)

def build():
    '''!
    example: build, gcc, icon=file-binary
    '''
    args, dir_args, cmd_args, build_dir, sample_dir = get_build_info()
    exec(args + dir_args + cmd_args, cwd=sample_dir)
    return 0

def rebuild():
    '''!
    example: rebuild, gcc, icon=library
    '''
    args, dir_args, cmd_args, build_dir, sample_dir = get_build_info()
    exec(args + dir_args + ['-t', 'clean'] + cmd_args, cwd=sample_dir)
    build()

def purge():
    '''!
    example: purge, gcc, icon=symbol-field
    '''
    args, dir_args, cmd_args, build_dir, sample_dir = get_build_info()
    shutil.rmtree(sample_dir / build_dir, ignore_errors=True)
    build()

def flash():
    '''!
    example: flash, gcc, icon=debug-start
    '''
    args, dir_args, cmd_args, build_dir, sample_dir = get_build_info()
    build()
    flash_args = []# TODO: json.loads(get_value('flash_args').strip() or '""')
    exec(['west', 'flash'] + dir_args + flash_args, cwd=sample_dir)

def target():
    '''!
    example: menuconfig, icon=check-all
        menuconfig
    example: guiconfig, icon=check-all
        guiconfig
    example: remote menuconfig, icon=check-all
        remote_menuconfig
    example: remote guiconfig, icon=check-all
        remote_guiconfig
    example: run posix, icon=play
        run
    '''
    args, dir_args, cmd_args, build_dir, sample_dir = get_build_info()
    exec(args + dir_args + ['-t', argv(0)] + cmd_args, cwd=sample_dir)
