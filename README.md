# VSCode tasks for NCS

## Requires

Tasks Shell Input Extension

https://marketplace.visualstudio.com/items?itemName=augustocdias.tasks-shell-input

## Installation

* If you don't have `.vscode` directory in you NSC directory yet:

  ```bash
  git clone https://github.com/doki-nordic/vscode_conf_for_ncs.git .vscode
  ```

* If you already have `.vscode` directory with configuration that you want to keep:
  ```bash
  mv .vscode _vscode_tmp
  git clone https://github.com/doki-nordic/vscode_conf_for_ncs.git .vscode
  # Now, try to merge your settings from "_vscode_tmp" into ".vscode".
  # You can use e.g. "meld" tool:
  meld _vscode_tmp .vscode
  # And delete "_vscode_tmp" when you are done.
  rm -Rf _vscode_tmp
  ```

After installation, you should see `.vscode` directory alongside with the `nrf`, `zephyr`, `nrfxlib`, e.t.c. You can now open NCS directory in VSCode and you can start any of the implemented tasks.

> ### Hint
> Add simple keyboard shortcut to show list of tasks. I am using `Pause/Break` key.
> 1. Open `File` -> `Preferences` -> `Keyboard shortcuts`.
> 1. Type `workbench.action.tasks.runTask` to find `Tasks: Run Task` action.
> 1. Double click it.
> 1. Press key that you want to use (e.g. `Pause/Break`). VSCode will show a message if it is already in use by other action.

## Implemented tasks

 * `example:`
    * `change folder` - change folder of current example
        * `From currenly opened CMakeLists.txt` - if folder is not visible on the list, open `CMakeLists.txt` file from the example folder and select this option.
    * `change board` - change current example board
        * `From currenly opened board yaml file` - if board is not visible on the list, open board `yaml` file and select this option.
    * `build` - build current example
    * `rebuild` - rebuild (clean and build) current example
    * `purge` - delete build directory and rebuild current example
    * `flash` - build and flash current example
    * `menuconfig` - start menuconfig for current example
    * `guiconfig` - start guiconfig for current example
    * `change arguments` - add custom west build arguments. ***It has some issues - may not work.***
        * `[[empty]]` - no additional arguments
        * `From terminal` - prompt will be shown on terminal panel to provide the arguments
 * `checkpatch:`
    * `run` - run check patch. You will be asked to select a repository and a branch that will be used as base for git compare.
    * `add git base` - allows you to add new base branch in terminal panel
 * `terminal` - connect to board serial port in the terminal panel
 * `vscode:`
    * `new instance` - create a new independent instance of the Visual Studio Code that is able to open the same folder and select different example.
    * `hide comments` - toggle color of the comment to almost invisible.
 * `doc:`
    * `rebuild` - delete documetation build directory, rectreate it with CMake and build it.
    * `build` - build the NCS documentation (requires that the build directory already exists and CMake was already called).
    * `build current file` - determinate docset that contains currently opened file and build only this docset.
    * `server` - start local HTTP server that serves current build output. Page content will be automatically reloaded if one of the above tasks was executed.
 * `nrf_rpc_gen:regenerate this file` - run nrf_rpc_generator on currenty opened file

## Automatic docs build and preview on file save

1. Install Trigger Task on Save Extension \
   https://marketplace.visualstudio.com/items?itemName=Gruntfuggly.triggertaskonsave

1. Configure it to start docs build of recently saved file, e.g.:
    ```JSON
    "triggerTaskOnSave.tasks": {
        "doc: build current file": [
            "**/*.rst",
            "**/*.h",
            "**/Kconfig*"
        ]
    },
    "triggerTaskOnSave.showStatusBarToggle": true,
    "triggerTaskOnSave.resultIndicator": "statusBar.background",
    "triggerTaskOnSave.failureColour": "#800000",
    "triggerTaskOnSave.successColour": "#008800",
    "triggerTaskOnSave.restart": true,
    ```

1. Disable `Trigger Task on Save` using button on status bar.

1. Rebuild the docuemntatio if you have not already do that with `docs:rebuild` task.

1. Start docs server with the `docs: server` task.

1. Open file and build it with `docs: build current file` task.

1. You can now reenable `Trigger Task on Save` on your status bar.

1. Make some change in the file and save it.

> ### Note
> Bacause of some issue in `Trigger Task on Save` extension, you have to start `docs: build current file`
> at least once before you enable this extension with the button on the status bar.

## Writing new tasks

Tasks:

1. Put Python tasks in a new file in the `.vscode/src` directory.
2. For each task create a new function.
   Function name must be unique, because task will be identified
   using this name.
3. Add special docstring describing the task.
   ```
   '''!
   task label, option 1, option 2, ...
       command line arguments
   '''
   ```
   * `task label` is any label you want
   * `options` are currently:
     * `gcc` - use gcc problem matcher for the task output
     * `icon=xyz` - set task icon, list of icons:
       https://code.visualstudio.com/api/references/icons-in-labels
   * `command line arguments` - arguments passed over command line.
     You can use vscode variables, e.g. `${fileDirname}` or 
     `${input:xyz}`. You can use `argv(n)` from `common` module to access arguments
     (`n` is zero-based and starts at the first argument of `command line arguments`)
   * You can define multiple tasks for one function
4. Run `tasks.py` or run task `vscode: refresh tasks` in vscode to
   refresh `tasks.json`.

Inputs:

1. Input is a function that has special docstring:
   ```
   '''!input'''
   ```
2. It prints possible values one per line.
3. Can be referenced in command line as `${input:your_function_name}`
4. Other types of inputs:
   * User input:
     ```
     def func():
         '''!
         input
             Please type your input:
         '''
         pass
     ```
   * Static list pick:
     ```
     def func():
         '''!
         input
             Please select you number:
             One
             Two
             Three
             Four
         '''
         pass
     ```