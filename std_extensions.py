import builtins as __builtin__
import platform
import re
import sys


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print(*args, **kwargs):
    # Manage colors
    if kwargs:
        if re.match(r"[E,e]rror", kwargs["log"]):
            color = bcolors.FAIL + bcolors.BOLD
        else:
            color = bcolors.OKBLUE + bcolors.BOLD
        kwargs.pop("log")
    else:
        color = bcolors.BOLD

    # Fix windows lack of flavor
    default = bcolors.ENDC
    if platform.system() == 'Windows':
        color = ''
        default = ''

    # Place a tag at the start of every line
    sys.stdout.write("{}[Liquidknot] {}".format(color, default))
    args = tuple([
        re.sub("\n", "{}\n[Liquidknot] {}".format(color, default), str(
            args[0]))
    ]) + args[1:]

    # Pass the args to the builtin print
    __builtin__.print(*args, **kwargs)
