import platform

from os import getcwd
from os.path import join
from subprocess import call


def unpack():
    if platform.system() == 'Linux':
        try:
            call(['sh', join(getcwd(), 'linux_setup.sh')])
        except RuntimeError:
            print('Virtualenv not installed')


if __name__ == "__main__":
    unpack()
