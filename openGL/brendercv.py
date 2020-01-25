from blend_parse import main
import time

if __name__ == "__main__":
    init = time.time()
    main((1920, 1080), accelerated=True)
    print("total execution time {0} sec".format(time.time() - init))
