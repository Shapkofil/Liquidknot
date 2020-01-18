import numpy as np
import pickle
import subprocess
import os


def venvexec(venv_path, file):
    print("trying to subprocess run")
    venv_path = os.path.join(os.path.dirname(__file__), venv_path)
    file = os.path.join(os.path.dirname(__file__), file)
    subprocess.run(["{0}/bin/python".format(venv_path), file])


def brender(resolution,
            vertex_code=None,
            fragment_code=None):

    venvexec(".venv", "blend_parse.py")

    tmp_path = os.path.join(os.path.dirname(__file__), "temp/temp.pickle")
    with open(tmp_path, "rb") as f:
        raw_render = pickle.load(f)

    refine = np.reshape(raw_render, (resolution[0] * resolution[1], 4))
    return refine.tolist()


if __name__ == "__main__":
    brender((1980, 1080))
