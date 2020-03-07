import sys
from core import render
import numpy as np
import json
import cv2
import re
from os.path import join, abspath, dirname

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
        with open(PATHS['RAW_BUFFER'], "wb") as f:
            f.write(buff)


with open(join(dirname(abspath(__file__)), '../paths.json')) as f:
    # GET PATHS
    global PATHS
    PATHS = json.loads(f.read())
    for key in PATHS.keys():
        PATHS[key] = join(dirname(abspath(__file__)), join('..', PATHS[key]))

if __name__ == "__main__":
    # Load Shader Code
    with open(PATHS['FRAG_SHADER']) as f:
        fragment_code = f.read()

    # Load Scene and Modify Shader Code
    resolution, bounds, fragment_code = parse_scene(PATHS['SCENE'], fragment_code)
    # print(bounds)

    # Log The Shader Code
    with open(PATHS['LOG_SHADER'], "w+") as f:
        f.write(fragment_code)

    # Execute Core
    main(resolution=resolution,
         bounds=bounds,
         fragment_code=fragment_code,
         filepath=(sys.argv[1] if re.match(r"^(.+)\.exr$", sys.argv[1]) else None))
