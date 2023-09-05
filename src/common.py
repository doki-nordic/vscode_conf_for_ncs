
from pathlib import Path
import sys
import subprocess

scripts_dir = Path(__file__).parent.resolve()
vscode_dir = scripts_dir.parent.resolve()
opt_dir = (vscode_dir / 'opt').resolve()
root_dir = vscode_dir.parent.resolve()
opt_dir.mkdir(exist_ok=True)

def exec(args, cwd=None):
    print(f'Run command: {green(" ".join(str(a) for a in args))}\n')
    sub = subprocess.run(args, cwd=cwd)
    if sub.returncode != 0:
        sys.exit(sub.returncode)

def get_stdout(args, cwd=None):
    sub = subprocess.run(args, cwd=cwd, capture_output=True, check=True)
    if len(sub.stderr) > 0:
        print(sub.stderr.decode('utf-8'), file=sys.stderr)
        sys.exit(5)
    return sub.stdout.decode('utf-8')

def argv(index):
    if index + 2 < len(sys.argv):
        return sys.argv[index + 2]
    return None

def mru_list(name):
    file: Path = opt_dir / (name + '.mru.txt')
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
    file: Path = opt_dir / (name + '.mru.txt')
    out = [value]
    out.extend(x.strip() for x in file.read_text().splitlines() if x.strip() != '' and x.strip() != value.strip())
    out = '\n'.join(out)
    old = file.read_text()
    if old != out:
        file.write_text(out)
    return value

def set_value(name, value):
    file: Path = opt_dir / (name + '.txt')
    file.write_text(value)
    return value

def get_value(name):
    file: Path = opt_dir / (name + '.txt')
    if not file.exists():
        return None
    return file.read_text()

def green(text):
    return f'\x1b[1m\x1b[32m{text}\x1b[0m'

def red(text):
    return f'\x1b[1m\x1b[31m{text}\x1b[0m'
