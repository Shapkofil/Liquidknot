from subprocess import call
import sys
from os.path import abspath as ap, dirname, join, isdir


def install_and_import(package):
    import importlib
    try:
        importlib.import_module(package)
    except ImportError:
        import pip
        pip.main(['install', package])
    finally:
        globals()[package] = importlib.import_module(package)


def unpack():
    # Preparations
    genepool = {
        "sudo": ("sudo", ""),
        "mkdir": ("mkdir", "md"),
        "pip": ("bin/pip", "Scripts/pip.exe")
    }
    index = int(sys.platform is 'linux')

    # Worthless cases
    if isdir(join(dirname(ap(__file__)), '../openGL/temp')) and isdir(join(dirname(ap(__file__)), '../openGL/.venv')):
        return

    python_exec = sys.exec_prefix + "/bin/python3.7m"
    venv_path = join(dirname(ap(__file__)), '../openGL/.venv')
    temp_path = join(dirname(ap(__file__)), '../openGL/temp')

    # Fix permitions
    # call(['chmod', '777', '-R', python_exec])

    call([python_exec,
          "{}".format(join(dirname(ap(__file__)), 'get_pip.py'))  # Path to script
          ])

    install_and_import('virtualenv')
    print('''it's not that dumb''')

    call([sys.exec_prefix + "/bin/python3.7m", '-m', 'virtualenv',
          venv_path  # Path to venv
          ])

    call([join(venv_path, genepool["pip"][index]),
          "install", "-r",
          'requirements.txt'
          ])

    call([genepool["mkdir"][index],
          temp_path
          ])


if __name__ == "__main__":
    unpack()
