import sys
import builtins as __builtin__


def print(*args, **kwargs):
    sys.stdout.write("[Liquidknot] ")
    __builtin__.print(*args, **kwargs)
