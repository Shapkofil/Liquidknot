import numpy as np
import subprocess
import os
import time


def venvexec(venv_path, file):
    # Execution in virtualenv

    venv_path = os.path.join(os.path.dirname(__file__), venv_path)
    file = os.path.join(os.path.dirname(__file__), file)
    buff = subprocess.run(
        ["{0}/bin/python".format(venv_path), file], capture_output=True)
    out = buff.stdout
    err = buff.stderr
    if err:
        print("SUBSCRIPT ERROR:\n{0}".format(err.decode()))

    file = os.path.join(os.path.dirname(__file__), "temp/output.buffer")
    with open(file, "rb") as f:
        byte = f.read()
    return np.frombuffer(byte, dtype=np.float32)


def brender(resolution=(1920, 1080),
            bounds=None,
            vertex_code=None,
            fragment_code=None):
    raw_render = venvexec(".venv", "blend_parse.py")

    # Full render cases
    if bounds is None:
        bounds = (0, 0, resolution[0], resolution[1])

    if raw_render.size == 0:
        print("No Return Statement")
        return

    # reshape the array
    refine = np.reshape(
        raw_render, ((bounds[2]) * (bounds[3]), 4))
    refine = refine.astype(np.float32)
    refine = refine.tolist()
    return refine


if __name__ == "__main__":
    init = time.time()
    result = brender((1920, 1080))
    print("total execution time {0} sec".format(time.time() - init))
