from importlib import import_module
from sys import argv
def main():
    if argv[1] == "serials":
        exit(import_module("serial").serials())
    elif argv[1] == "term_window":
        exit(import_module("serial").term_window())
    elif argv[1] == "term_inner":
        exit(import_module("serial").term_inner())
    elif argv[1] == "term":
        exit(import_module("serial").term())
    elif argv[1] == "boards":
        exit(import_module("build").boards())
    elif argv[1] == "get_board":
        exit(import_module("build").get_board())
    elif argv[1] == "set_board":
        exit(import_module("build").set_board())
    elif argv[1] == "samples":
        exit(import_module("build").samples())
    elif argv[1] == "get_sample":
        exit(import_module("build").get_sample())
    elif argv[1] == "set_sample":
        exit(import_module("build").set_sample())
    elif argv[1] == "build_args":
        exit(import_module("build").build_args())
    elif argv[1] == "flash_args":
        exit(import_module("build").flash_args())
    elif argv[1] == "set_build_args":
        exit(import_module("build").set_build_args())
    elif argv[1] == "set_flash_args":
        exit(import_module("build").set_flash_args())
    elif argv[1] == "get_build_dir_name":
        exit(import_module("build").get_build_dir_name())
    elif argv[1] == "build":
        exit(import_module("build").build())
    elif argv[1] == "rebuild":
        exit(import_module("build").rebuild())
    elif argv[1] == "purge":
        exit(import_module("build").purge())
    elif argv[1] == "flash":
        exit(import_module("build").flash())
    elif argv[1] == "target":
        exit(import_module("build").target())
    elif argv[1] == "refresh_tasks":
        exit(import_module("tasks").refresh_tasks())
    elif argv[1] == "source_zephyr":
        exit(import_module("vscode").source_zephyr())
    elif argv[1] == "source_zephyr_inner":
        exit(import_module("vscode").source_zephyr_inner())
    elif argv[1] == "instance_title":
        exit(import_module("vscode").instance_title())
    elif argv[1] == "instance":
        exit(import_module("vscode").instance())
if __name__ == "__main__":
    main()
