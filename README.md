# VSCode tasks for NCS

## Requires

Tasks Shell Input Extension

https://marketplace.visualstudio.com/items?itemName=augustocdias.tasks-shell-input

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