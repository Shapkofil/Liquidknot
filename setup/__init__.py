from subprocess import call
import sys
from os.path import abspath as ap, dirname, join, isdir
from os import mkdir


def unpack():
    # Preparations
    genepool = {
        "mkdir": ("mkdir", "md"),

        "python": ("/bin/python3.7m", "/bin/python.exe"),
        "pip": ("bin/pip", "Scripts/pip.exe")
    }
    index = int(not sys.platform == 'linux')

    python_exec = sys.exec_prefix + genepool["python"][index]
    venv_path = join(dirname(ap(__file__)), '../liquidknot/.venv')
    temp_path = join(dirname(ap(__file__)), '../liquidknot/temp')

    # Worthless cases
    if isdir(venv_path) and isdir(temp_path):
        return

    call([python_exec,
          # Path to script
          "{}".format(join(dirname(ap(__file__)), 'get_pip.py'))
          ])

    call([python_exec, '-m', 'pip', 'install', 'virtualenv', '--user'])

    call([python_exec, '-m', 'virtualenv', venv_path])

    call([join(venv_path, genepool["pip"][index]),
          "install", "-r",
          join(dirname(ap(__file__)), 'requirements.txt')
          ])

    print(temp_path)
    mkdir(temp_path)


if __name__ == "__main__":
    unpack()
