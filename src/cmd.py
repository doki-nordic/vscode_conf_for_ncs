from importlib import import_module
from sys import argv
def main():
    if argv[1] == "boards":
        exit(import_module("build").boards())
    elif argv[1] == "set_board":
        exit(import_module("build").set_board())
    elif argv[1] == "samples":
        exit(import_module("build").samples())
    elif argv[1] == "set_sample":
        exit(import_module("build").set_sample())
    elif argv[1] == "build_args":
        exit(import_module("build").build_args())
    elif argv[1] == "set_build_args":
        exit(import_module("build").set_build_args())
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
    elif argv[1] == "some":
        exit(import_module("tasks").some())
    elif argv[1] == "test_cinput":
        exit(import_module("tasks").test_cinput())
    elif argv[1] == "refresh_tasks":
        exit(import_module("tasks").refresh_tasks())
if __name__ == "__main__":
    main()
