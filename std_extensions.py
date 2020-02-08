import sys
import re
import builtins as __builtin__


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
            color = bcolors.OKBLUE = bcolors.BOLD
        kwargs.pop("log")
    else:
        color = bcolors.BOLD

    sys.stdout.write("{}[Liquidknot] {}".format(color, bcolors.ENDC))
    args = tuple([re.sub("\n", "{}\n[Liquidknot] {}".format(color, bcolors.ENDC), args[0])]) + args[1:]
    __builtin__.print(*args, **kwargs)


if __name__ == "__main__":
	print("shit, \n")