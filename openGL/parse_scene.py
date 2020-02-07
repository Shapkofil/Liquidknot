import json
import re

from glsl_lib import glsl_math as glsl


def de_gen(entity):
    de = entity["de"]

    # Position sub
    de = re.sub(r"p", "p - {0}".format(glsl.vec(entity["position"])), de)

    # To Do Rotaion Sub

    # Params sub
    for name, param in entity["params"].items():
        de = re.sub(name, str(param), de)

    return de


def de_gen_swamp(swamp):
    de = de_gen(swamp[0])
    for entity in swamp[1:]:
        de = "smin ({0}, {1}, .1)".format(de_gen(entity), de)
    de = "return {0};".format(de)
    return de


def parse_scene(scene_path, fragment_code):
    with open(scene_path) as f:
        raw = f.read()
        data = json.loads(raw)

    # Load Bounds And Resolution
    resolution = tuple(data["RESOLUTION"])
    bounds = tuple(data["BOUNDS"])

    # Loading Hyper Params
    snippet = ""
    for c_type in data["hyper_params"]:
        for k, v in data["hyper_params"][c_type].items():
            snippet += "\nconst {0} {1} = {2};".format(c_type, k,
                                                       glsl.vec(v) if re.match(r"^vec", c_type) else v)

    fragment_code = re.sub(r"// pebble hyper_params", snippet, fragment_code)

    # Loading Scene DE

    de = de_gen_swamp(data["entities"])
    fragment_code = re.sub(r"// pebble distance_estimator", de, fragment_code)

    # Loading Camera
    fragment_code = re.sub(r"pebble camera_position",
                           glsl.vec(data["camera"]["position"]),
                           fragment_code)
    fragment_code = re.sub(r"pebble camera_rotation",
                           glsl.vec(data["camera"]["rotation"]),
                           fragment_code)

    fragment_code = re.sub(r"pebble focal_lenght",
                           str(data["camera"]["focal_length"]),
                           fragment_code)

    # Loading lights
    n = len(data["lights"])
    snippet = "const float light_count = {0};\n".format(n)
    snippet_pos = "const vec3 light_positions[{0}] = ".format(n) + r"{"
    snippet_cl = "const vec4 light_colors[{0}] = ".format(n) + r"{"
    for light in data["lights"]:
        snippet_pos += "{0}, ".format(glsl.vec(light["position"]))
    for light in data["lights"]:
        snippet_cl += "{0}, ".format(glsl.vec(light["color"]))
    snippet_pos = snippet_pos[:-2] + r"};" + "\n"
    snippet_cl = snippet_cl[:-2] + r"};" + "\n"
    snippet += snippet_pos + snippet_cl
    fragment_code = re.sub(r"// pebble lights", snippet, fragment_code)

    return resolution, bounds, fragment_code
