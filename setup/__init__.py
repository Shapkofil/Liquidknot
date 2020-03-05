from subprocess import call
import sys
from os.path import abspath as ap, dirname, join, isdir
from os import mkdir

import re


def install_and_import(python_exec, package):
    import importlib
    try:
        importlib.import_module(package)
    except ImportError:
        call([python_exec, '-m', 'pip', 'install', package, '--user'])
    finally:
        globals()[package] = importlib.import_module(package)


def unpack():
    # Preparations
    genepool = {
        "mkdir": ("mkdir", "md"),

        "python": ("/bin/python3.7m", "/bin/python.exe"),
        "pip": ("bin/pip", "Scripts/pip.exe")
    }
    index = int(not sys.platform == 'linux')

    python_exec = sys.exec_prefix + genepool["python"][index]
    venv_path = join(dirname(ap(__file__)), '../openGL/.venv')
    temp_path = join(dirname(ap(__file__)), '../openGL/temp')

    # Worthless cases
    if isdir(venv_path) and isdir(temp_path):
        return

    call([python_exec,
          # Path to script
          "{}".format(join(dirname(ap(__file__)), 'get_pip.py'))
          ])

    install_and_import(python_exec, 'virtualenv')

    call([python_exec, '-m', 'virtualenv',
          venv_path  # Path to venv
          ])

    call([join(venv_path, genepool["pip"][index]),
          "install", "-r",
          join(dirname(ap(__file__)), 'requirements.txt')
          ])

    print(temp_path)
    mkdir(temp_path)


if __name__ == "__main__":
    unpack()
