import sys
from core import render
import numpy as np
import os
import cv2
import re

from parse_scene import parse_scene


def saveimg(source, filepath):
    source[:, :, :3] = source[:, :, :3][:, :, ::-1]
    if not re.match(r"^(.+)\.exr$", filepath):
        source = np.asarray(source * 255, dtype=np.uint8)
    print("Saving image in {}....".format(filepath))
    cv2.imwrite(filepath, source[:, :, :3])
    print("Saved!")


def main(resolution=(1920, 1080),
         bounds=(0, 0, 1920, 1080),
         vertex_code=None,
         fragment_code=None,
         filepath=None):
    raw_data = render(resolution, bounds, fragment_code=fragment_code)

    if filepath is None:
        buff = memoryview(raw_data).tobytes()
        sys.stdout.buffer.write(buff)
        sys.stdout.buffer.flush()
        quit()

    if not re.match(r"^(.+)\.buffer$", filepath):
        saveimg(raw_data, filepath)
    else:
        buff = memoryview(raw_data).tobytes()
        file = os.path.join(os.path.dirname(__file__), "temp/output.buffer")
        with open(file, "wb") as f:
            f.write(buff)


# ToDo entry point
if __name__ == "__main__":

    # ToDo get File Paths Externally

    # Load Shader Code
    file = os.path.join(os.path.dirname(__file__), "fragment.shader")
    with open(file) as f:
        fragment_code = f.read()

    # Load Scene and Modify Shader Code
    file = os.path.join(os.path.dirname(__file__), "temp/scene.json")
    resolution, bounds, fragment_code = parse_scene(file, fragment_code)
    # print(bounds)

    # Log The Shader Code
    file = os.path.join(os.path.dirname(__file__), "temp/log.shader")
    with open(file, "w+") as f:
        f.write(fragment_code)

    # Execute Core
    main(resolution=resolution,
         bounds=bounds,
         fragment_code=fragment_code,
         filepath=(sys.argv[1] if re.match(r"^(.+)\.exr$", sys.argv[1]) else None))
