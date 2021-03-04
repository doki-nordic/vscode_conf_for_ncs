# vscode_conf_for_ncs

# Requires

Tasks Shell Input

https://marketplace.visualstudio.com/items?itemName=augustocdias.tasks-shell-input

# Implemented tasks

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
    * `change arguments` - add custom west build arguments
        * `[[empty]]` - no additional arguments
        * `From terminal` - prompt will be shown on terminal panel to provide the arguments
 * `checkpatch:`
    * `run` - run check patch. You will be asked to select a repository and a branch that will be used as base for git compare.
    * `add git base` - allows you to add new base branch in terminal panel
 * `terminal` - connect to board serial port in the terminal panel
 * `vscode:`
    * `new instance` - create a new independent instance of the Visual Studio Code that is able to open the same folder and select different example.
    * `hide comments` - toggle color of the comment to almost invisible.
 * `nrf_rpc_gen:regenerate this file` - run nrf_rpc_generator on currenty opened file
