import platform

from os.path import join, dirname, abspath as ap, isdir
from subprocess import call


def unpack():
    if isdir(join(dirname(ap(__file__)), '../openGL/temp')) and isdir(join(dirname(ap(__file__)), '../openGL/.venv')):
        return

    if platform.system() == 'Linux':
        try:
            with open(join(dirname(ap(__file__)), 'linux_setup.sh'), 'r') as f:
                old = f.read()

            file = join(dirname(ap(__file__)), 'linux_exec.sh')
            with open(file, 'w') as f:
                f.write('cd {}\n'.format(dirname(ap(__file__))) + old)
            call(['sh', file])
        except RuntimeError:
            print('Virtualenv might not installed')

    if platform.system() == 'Windows':
        try:
            with open(join(dirname(ap(__file__)), 'win_setup.bat'), 'r') as f:
                old = f.read()

            file = join(dirname(ap(__file__)), 'win_exec.bat')
            with open(file, 'w') as f:
                f.write('cd {}\n'.format(dirname(ap(__file__))) + old)
            call(['bat.exe', file])
        except RuntimeError:
            print('Virtualenv might not installed')


if __name__ == "__main__":
    unpack()
