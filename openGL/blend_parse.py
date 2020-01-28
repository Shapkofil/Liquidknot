import sys
from core import render
import cv2
import numpy as np
import os
from .parse_scene import parse_scene


def main(resolution=(1920, 1080),
         bounds=(0, 0, 1920, 1080),
         vertex_code=None,
         fragment_code=None,
         accelerated=False):
    raw_data = render(resolution, bounds, fragment_code=fragment_code)

    if accelerated:
        refine = np.asarray(raw_data * 255, dtype=np.uint8)
        refine[:, :, :3] = refine[:, :, :3][:, :, ::-1]
        cv2.imwrite("temp/temp.png", refine)
    else:
        buff = memoryview(raw_data).tobytes()
        sys.stdout.buffer.write(buff)


# ToDo entry point
if __name__ == "__main__":

    # ToDo get File Paths Externally

    file = os.path.join(os.path.dirname(__file__), "fragment.shader")
    with open(file) as f:
        fragment_code = f.read()
    file = os.path.join(os.path.dirname(__file__), "scene.json")

    resolution, bounds, fragment_code = parse_scene(file, fragment_code)
    # print(bounds)
    main(resolution=resolution, bounds=bounds,
         fragment_code=fragment_code)
