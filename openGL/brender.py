import numpy as np
import subprocess
import os
import time
import re

try:
    from ..std_extentions import *
except ImportError:
    print("Stand alone mode")


def venvexec(venv_path, file, output_path=None):
    # Execution in virtualenv

    output_path = "None" if output_path is None else output_path

    venv_path = os.path.join(os.path.dirname(__file__), venv_path)
    file = os.path.join(os.path.dirname(__file__), file)
    buff = subprocess.run(
        ["{0}/bin/python".format(venv_path), file, output_path], capture_output=True)
    err = buff.stderr

    if err:
        print("SUBSCRIPT ERROR:\n{0}".format(err.decode()))

    # Stdout Cases
    byte = buff.stdout

    # Exr Cases
    if re.match(r"^(.+)\.exr", output_path):
        print(output_path)
        return None
    # Buffer Cases
    elif not output_path == "None":
        file = os.path.join(os.path.dirname(__file__), output_path)
        with open(file, "rb") as f:
            byte = f.read()

    return np.frombuffer(byte, dtype=np.float32)


def brender(resolution=(1920, 1080),
            bounds=None,
            vertex_code=None,
            fragment_code=None,
            filepath=None):
    raw_render = venvexec(".venv", "blend_parse.py", filepath)

    # Full render cases
    if bounds is None:
        bounds = (0, 0, resolution[0], resolution[1])

    # Exr Cases
    if filepath is not None:
        print("Saved result at {} !".format(filepath))
        return None

    # Buffer Cases and Direct Stdout cases
    refine = np.reshape(raw_render, ((bounds[2]) * (bounds[3]), 4))
    refine = refine.astype(np.float32)
    return refine


if __name__ == "__main__":
    init = time.time() 
    result = brender((1920, 1080), filepath="temp/temp.exr")
    print("total execution time {0} sec".format(time.time() - init))
