import sys
from core import render
import json
import re
import cv2
import numpy as np

from glsl_utils.primitives import de_gen_swamp
from glsl_utils import glsl_math as glsl


def parse_scene(scene_path, fragment_code):
    with open(scene_path) as f:
        raw = f.read()
        data = json.loads(raw)

    # Loading Hyper Params
    snippet = ""
    for c_type in data["hyper_params"]:
        for k, v in data["hyper_params"][c_type].items():
            if c_type == "vec4":
                snippet += "\nconst {0} {1} = {2};".format(
                    c_type, k, glsl.vec4(v))
                continue
            if c_type == "vec3":
                snippet += "\nconst {0} {1} = {2};".format(
                    c_type, k, glsl.vec3(v))
                continue
            snippet += "\nconst {0} {1} = {2};".format(c_type, k, v)

    fragment_code = re.sub(r"// pebble hyper_params", snippet, fragment_code)

    # Loading Scene DE

    de = de_gen_swamp(data["entities"])
    fragment_code = re.sub(r"// pebble distance_estimator", de, fragment_code)

    # Loading Camera
    fragment_code = re.sub(r"// pebble camera_position",
                           glsl.vec3(data["camera"]["position"]),
                           fragment_code)
    fragment_code = re.sub(r"pebble camera_rotation",
                           glsl.vec3(data["camera"]["rotation"]),
                           fragment_code)

    # Loading lights
    n = len(data["lights"])
    snippet = "const float light_count = {0};\n".format(n)
    snippet_pos = "const vec3 light_positions[{0}] = ".format(n) + r"{"
    snippet_cl = "const vec4 light_colors[{0}] = ".format(n) + r"{"
    for light in data["lights"]:
        snippet_pos += "{0}, ".format(glsl.vec3(light["position"]))
    for light in data["lights"]:
        snippet_cl += "{0}, ".format(glsl.vec4(light["color"]))
    snippet_pos = snippet_pos[:-2] + r"};" + "\n"
    snippet_cl = snippet_cl[:-2] + r"};" + "\n"
    snippet += snippet_pos + snippet_cl
    fragment_code = re.sub(r"// pebble lights", snippet, fragment_code)

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

    fragment_code = parse_scene("scene.json", fragment_code)
    # print(fragment_code)
    main(fragment_code=fragment_code, accelerated=True)
