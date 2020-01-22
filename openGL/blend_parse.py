import sys
from core import render
import json
import re
import cv2
import numpy as np


def parse_entry(scene_path, fragment_code):
    with open(scene_path) as f:
        raw = f.read()
        data = json.loads(raw)

    # Loading Hyper Params
    snippet = ""
    for c_type in data["hyper_params"]:
        for k, v in data["hyper_params"][c_type].items():
            snippet += "\nconst {0} {1} = {2};".format(c_type, k, v)

    fragment_code = re.sub(r"// pebble hyper_params", snippet, fragment_code)
    return fragment_code


def main(resolution=(1920, 1080),
         vertex_code=None,
         fragment_code=None,
         accelerated=False):
    raw_data = render((1920, 1080), fragment_code=fragment_code)

    if accelerated:
        refine = np.asarray(raw_data * 255, dtype=np.uint8)
        refine[:, :, :3] = refine[:, :, :3][:, :, ::-1]
        cv2.imwrite("temp/temp.png", refine)
    else:
        buff = memoryview(raw_data).tobytes()
        sys.stdout.buffer.write(buff)


# ToDo entry point
if __name__ == "__main__":
    with open("fragment.shader") as f:
        fragment_code = f.read()

    fragment_code = parse_entry("structure.json", fragment_code)
    main(fragment_code=fragment_code)
