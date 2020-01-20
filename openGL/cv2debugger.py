import cv2
import numpy as np
from core import render
import time


def main():
    raw_read = render((1920, 1080))
    refine = np.asarray(raw_read * 255, dtype=np.uint8)
    refine[:, :, :3] = refine[:, :, :3][:, :, ::-1]

    cv2.imwrite("test_render.png", refine)


if __name__ == "__main__":
    init = time.time()
    main()
    print("total exec time {0}".format(time.time() - init))
