
'''
[[commands]]
'''

import sys
import re
import json
import pyjson5
import shutil
import importlib
import inspect
from textwrap import dedent
from common import *

INPUT_PREFIX = '_helper_'

GCC_PROBLEM_MATCHER = json.loads('''
    {
        "owner": "cpp",
        "source": "gcc",
        "fileLocation": [
            "autoDetect",
            "${input:_helper_get_sample}/build_${input:_helper_get_build_dir_name}"
        ],
        "pattern": {
            "regexp": "^(.*?):([0-9]+)(:([0-9]+))?:(\\\\s*([a-zA-Z]+):)?\\\\s*(.*)$",
            "severity": 6,
            "message": 7,
            "file": 1,
            "line": 2,
            "column": 4,
            "code": 6
        }
    }
    ''')

tasks = []
inputs = []
args_replace = {}
locations = {}

def split_options(options):
    return re.split(r'\s*,\s*', options)

def add_input(func_name, options, args):
    input_id = INPUT_PREFIX + func_name
    args_replace['{input:' + func_name + '}'] = '{input:' + input_id + '}'
    use_first = False
    for option in options:
        if option.strip() == 'one':
            use_first = True
        elif option.strip() == '':
            pass
        else:
            print('Unknown option', option, file=sys.stderr)
            exit(5)
    if len(args) == 0:
        inputs.append({
            'id': input_id,
            'type': 'command',
            'command': 'shellCommand.execute',
            'args': {
                'command': '${workspaceFolder}/.vscode/cmd ' + func_name
            }
        })
        if use_first:
            inputs[-1]['args']['useFirstResult'] = True
    elif len(args) == 1:
        inputs.append({
            'id': input_id,
            'type': 'promptString',
            'description': args[0],
        })
    else:
        inputs.append({
            'id': input_id,
            'type': 'pickString',
            'description': args[0],
            'options': args[1:],
            'default': args[1],
        })

def add_task(func_name, options, args):
    command_line = args[0] if len(args) > 0 else ''
    task = {}
    if len(args) > 1:
        task = json.loads('\n'.join(args[1:]))
    label = options[0]
    is_gcc = False
    is_hidden = False
    icon = None
    for option in options[1:]:
        if option.strip() == 'gcc':
            is_gcc = True
        elif option.strip() == 'hide':
            is_hidden = True
        elif option.strip().startswith('icon='):
            icon = option.strip()[5:]
        elif option.strip() == '':
            pass
        else:
            print('Unknown option', option, file=sys.stderr)
            exit(5)
    for from_str, to_str in args_replace.items():
        command_line = command_line.replace(from_str, to_str)
    task['label'] = label
    task['type'] = 'shell'
    task['command'] = '${workspaceFolder}/.vscode/cmd ' + func_name + ' ' + command_line
    if is_gcc:
        task['problemMatcher'] = GCC_PROBLEM_MATCHER
        task['group'] = 'build'
    else:
        task['problemMatcher'] = []
    if icon:
        task['icon'] = { 'id': icon, 'color': 'terminal.ansiBlue' }
    if is_hidden:
        task['__HIDE__'] = True
    tasks.append(task)

def add_entry(mod_name, func_name, text):
    text = dedent(text).strip()
    locations[func_name] = mod_name
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        first_line = lines[i]
        i += 1
        if first_line.strip() == '':
            continue
        args = []
        while i < len(lines) and lines[i].startswith(' '):
            line = lines[i].strip()
            i += 1
            if line != '':
                args.append(line)
        if first_line == 'input' or first_line.startswith('input ') or first_line.startswith('input,'):
            add_input(func_name, split_options(first_line[6:]), args)
        else:
            add_task(func_name, split_options(first_line), args)

def generate_cmd_script():
    with open(scripts_dir / 'cmd.py', 'w') as f:
        f.write('from importlib import import_module\n')
        f.write('from sys import argv\n')
        f.write('def main():\n')
        arr = []
        for func_name, file in locations.items():
            arr.append(f'if argv[1] == "{func_name}":\n        exit(import_module("{file}").{func_name}())\n')
        f.write('    ' + '    el'.join(arr))
        f.write('if __name__ == "__main__":\n')
        f.write('    main()\n')

def replace_array(arr, new_items, is_our, is_the_same):
    pass
    for old_item in arr:
        if is_our(old_item):
            old_item['__DELETE__'] = True
    for new_item in new_items:
        if '__HIDE__' not in new_item:
            new_item['__NEW__'] = True
    for i, old_item in list(enumerate(arr)):
        for new_item in new_items:
            if '__NEW__' in new_item and is_the_same(old_item, new_item):
                arr[i] = new_item
                del new_item['__NEW__']
                break
    for new_item in new_items:
        if '__NEW__' in new_item:
            arr.append(new_item)
            del new_item['__NEW__']
    tmp = list(x for x in arr if '__DELETE__' not in x)
    arr.clear()
    arr.extend(tmp)

def update_tasks_json():
    with open(vscode_dir / 'tasks.json', 'rb') as f:
        root = pyjson5.decode_io(f)

    def is_our_input(a):
        return ('id' in a) and (a['id'].startswith(INPUT_PREFIX))
    def is_the_same_input(a, b):
        return ('id' in a) and ('id' in b) and (a['id'] == b['id'])
    replace_array(root['inputs'], inputs, is_our_input, is_the_same_input)

    def is_our_task(a):
        return ('command' in a) and a['command'].startswith('${workspaceFolder}/.vscode/cmd ')
    def is_the_same_task(a, b):
        return (is_our_task(a)
                and is_our_task(b)
                and a['command'].split(' ')[1] == b['command'].split(' ')[1]
                and (a['command'] == b['command'] or a['label'] == b['label']))
    replace_array(root['tasks'], tasks, is_our_task, is_the_same_task)

    with open(vscode_dir / 'tasks.json', 'w') as f:
        json.dump(root, f, indent='\t')

def refresh_tasks():
    '''!
    vscode: refresh tasks, icon=extensions-sync-enabled
    '''
    for file in scripts_dir.glob('*.py'):
        file = file.resolve()
        try:
            mod = importlib.import_module(file.stem)
        except:
            print(f'Skipping {file.name} due to import error')
            continue
        if (mod.__doc__ or '').find('[[commands]]') < 0:
            continue
        for name, value in mod.__dict__.items():
            if (callable(value) and value.__doc__ and value.__doc__.strip().startswith('!') and
                    Path(inspect.getfile(value)).resolve() == file):
                add_entry(file.stem, name, value.__doc__.strip()[1:])
    generate_cmd_script()
    update_tasks_json()

if __name__ == '__main__':
    refresh_tasks()
    print(json.dumps(tasks, indent='\t'))
