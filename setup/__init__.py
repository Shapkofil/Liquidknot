import platform

from os import getcwd
from os.path import join
from subprocess import call


def unpack():
    if platform.system() == 'Linux':
        try:
            with open(join(getcwd(), 'linux_setup.sh'), 'r') as f:
                old = f.read()

            file = join(getcwd(), 'linux_exec.sh')
            with open(file, 'w') as f:
                f.write('cd {}\n'.format(getcwd()) + old)
            call(['sh', file])
        except RuntimeError:
            print('Virtualenv not installed')


if __name__ == "__main__":
    unpack()
