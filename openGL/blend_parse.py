import pickle
import os
import time

from core import render


def main():
    init = time.time()
    numren = render()
    print("render for {0}".format(time.time() - init))
    tmp_path = os.path.join(os.path.dirname(__file__), "temp/temp.pickle")
    with open(tmp_path, "wb") as f:
        pickle.dump(numren, f)
    print("write for {0}".format(time.time() - init))


# ToDo entry point
if __name__ == "__main__":
    main()
