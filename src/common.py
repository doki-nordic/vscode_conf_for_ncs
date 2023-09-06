
from pathlib import Path
import sys
import os
import subprocess
import tempfile

vscode_instance_id = os.environ.get('VS_CODE_INSTANCE')
if vscode_instance_id is None:
    vscode_instance_id = ''

scripts_dir = Path(__file__).parent.resolve()
vscode_dir = scripts_dir.parent.resolve()
global_opt_dir = (vscode_dir / 'opt').resolve()
current_opt_dir = (vscode_dir / ('opt' + vscode_instance_id)).resolve()
root_dir = vscode_dir.parent.resolve()

global_opt_dir.mkdir(exist_ok=True)
current_opt_dir.mkdir(exist_ok=True)

def bash_args(args, bash):
    if not bash:
        return args
    with tempfile.NamedTemporaryFile('w+', suffix='.sh', delete=False) as f:
        f.write('#!/bin/sh\n' + args)
        f.close()
        return ['bash', f.name]

def bash_end(args, bash):
    if bash:
        try:
            Path(args[1]).unlink()
        except:
            pass

def exec(args, cwd=None, allow_fail=False, bash=False):
    args = bash_args(args, bash)
    print(f'Run command: {green(" ".join(str(a) for a in args))}\n')
    sub = subprocess.run(args, cwd=cwd)
    bash_end(args, bash)
    if sub.returncode != 0 and not allow_fail:
        sys.exit(sub.returncode)
    return sub.returncode

def get_stdout(args, cwd=None, bash=False):
    args = bash_args(args, bash)
    sub = subprocess.run(args, cwd=cwd, capture_output=True, check=True)
    bash_end(args, bash)
    if len(sub.stderr) > 0:
        print(sub.stderr.decode('utf-8'), file=sys.stderr)
        sys.exit(5)
    return sub.stdout.decode('utf-8')

def argv(index):
    if index + 2 < len(sys.argv):
        return sys.argv[index + 2]
    return None

def mru_list(name):
    file: Path = global_opt_dir / (name + '.mru.txt')
    if not file.exists():
        file.touch()
    return (x.strip() for x in file.read_text().splitlines() if x.strip() != '')

def opt_input(text):
    if text == '[[input]]':
        print('Enter input: ', end='')
        sys.stdout.flush()
        return input()
    elif text == '[[empty]]':
        return ''
    else:
        return text

def mru_update(name, value):
    if value.startswith('[['):
        return value
    file: Path = global_opt_dir / (name + '.mru.txt')
    if not file.exists():
        file.touch()
    out = [value]
    out.extend(x.strip() for x in file.read_text().splitlines() if x.strip() != '' and x.strip() != value.strip())
    out = '\n'.join(out)
    old = file.read_text()
    if old != out:
        file.write_text(out)
    return value

def set_value(name, value, global_opt=False):
    file: Path = (global_opt_dir if global_opt else current_opt_dir) / (name + '.txt')
    file.write_text(value)
    return value

def get_value(name):
    file: Path = current_opt_dir / (name + '.txt')
    if not file.exists():
        return None
    return file.read_text()

def green(text):
    return f'\x1b[1m\x1b[32m{text}\x1b[0m'

def red(text):
    return f'\x1b[1m\x1b[31m{text}\x1b[0m'
