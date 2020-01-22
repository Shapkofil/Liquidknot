import numpy as np
import subprocess
import os
import time
import cv2


def venvexec(venv_path, file):
    venv_path = os.path.join(os.path.dirname(__file__), venv_path)
    file = os.path.join(os.path.dirname(__file__), file)
    subprocess.run(["{0}/bin/python".format(venv_path), file])


def brender(resolution,
            vertex_code=None,
            fragment_code=None):

    venvexec(".venv", "cv2debugger.py")

    # Load the rendered data
    file = os.path.join(os.path.dirname(__file__), "temp/temp.png")
    raw_data = cv2.imread(file, cv2.IMREAD_UNCHANGED)
    print(raw_data.shape)

    refine = raw_data.astype(np.float32) / 255.
    refine = np.reshape(refine, (resolution[0] * resolution[1], 4))
    return refine


if __name__ == "__main__":
    init = time.time()
    print(brender((1920, 1080)))
    print("total execution time {0} sec".format(time.time() - init))
