import pickle
import os
import sys
import time

from core import render


def main():
    raw_data = render()
    buff = memoryview(raw_data).tobytes()
    sys.stdout.buffer.write(buff)


# ToDo entry point
if __name__ == "__main__":
    main()
