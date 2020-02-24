import json
import re

from glsl_lib import glsl_math as glsl, lib_code


union_dict = {
    "UNION": "opUnion",
    "SUBTRACTION": "opSubtraction",
    "INTERSECTION": "opIntersection",
    "SMOOTH_UNION": "opSmoothUnion",
    "SMOOTH_SUBTRACTION": "opSmoothSubtraction",
    "SMOOTH_INTERSECTION": "opSmoothIntersection",
}


def name_gen(name):
    return re.sub(r"\.", "_", name)


def de_gen(entity):
    de = entity["de"]
    for k, v in entity["params"].items():
        print("{} {}".format(k, v))
        de = re.sub(k, str(v), de)
    snippet = "{} {}( vec3 p )\n{{\n".format("float", name_gen(entity["name"]))

    # Adjust for position
    snippet += "    p -= {};\n".format(glsl.vec(entity["position"]))

    # Adjust for rotation
    snippet += "    p = rotate_ray(p, {1});\n".format(glsl.vec(entity["position"]), glsl.vec(entity["rotation"]))

    # Main de addition
    snippet += "    return {};\n}}\n\n".format(de)
    return snippet


def de_gen_swamp(swamp, union):
    de = de_gen(swamp[0])
    de_line = "{0}(p)".format(name_gen(swamp[0]["name"]))
    color_line = "csdf({0}(p), {1}, {2})" \
        .format(name_gen(swamp[0]["name"]), glsl.vec(swamp[0]["color"]), union["value"])
    for entity in swamp[1:]:
        de += de_gen(entity)
        de_line = "{0}({1}(p) , {2}{3})"\
            .format(union_dict[union["mode"]], name_gen(entity["name"]), de_line,
                    ", {}".format(union["value"]) if re.match(r"^SMOOTH(.+)$", union["mode"]) else " ")
        color_line += " + " + "csdf({0}(p), {1}, {2})"\
            .format(name_gen(entity["name"]), glsl.vec(entity["color"]), union["value"] / 2)
    de_line = "return {0};".format(de_line)
    color_line = "return normalize({0});".format(color_line)
    return de, de_line, color_line


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

    # Loading Camera
    snippet += "\n\nconst vec3 camera_position = {0};\n".format(glsl.vec(data["camera"]["position"]))
    snippet += "const vec4 camera_rotation = {0};\n".format(glsl.vec(data["camera"]["rotation"]))
    snippet += "const float focal_length = {0};\n\n".format(data["camera"]["focal_length"])
    snippet += "const vec2 sensor = {0};\n\n".format(glsl.vec(data["camera"]["sensor"]))

    # Loading lights
    n = len(data["lights"])
    snippet += "const float light_count = {0};\n".format(n)

    # Light position
    snippet_pos = "const vec3 light_positions[{0}] = ".format(n) + r"{"
    for light in data["lights"]:
        snippet_pos += "{0}, ".format(glsl.vec(light["position"]))
    snippet_pos = snippet_pos[:-2] + r"};" + "\n"

    # Light color
    snippet_cl = "const vec4 light_colors[{0}] = ".format(n) + r"{"
    for light in data["lights"]:
        snippet_cl += "{0}, ".format(glsl.vec(light["color"]))
    snippet_cl = snippet_cl[:-2] + r"};" + "\n"

    # Combine Light passes
    snippet += snippet_pos + snippet_cl + "\n"

    # Loading Scene DE and Color
    de_snippet, de, color = de_gen_swamp(data["entities"], data["default_union"])
    snippet += de_snippet
    fragment_code = re.sub(r"// pebble distance_estimator", de, fragment_code)
    fragment_code = re.sub(r"// pebble scene_color", color, fragment_code)

    # Assemble the fragment_code segment
    fragment_code = lib_code + snippet + fragment_code
    return resolution, bounds, fragment_code


if __name__ == "__main__":
    import time
    start = time.time()
    with open("fragment.shader", "r") as f:
        parse_scene("scene.json", f.read())
    print("parsed for {} sec".format(time.time() - start))
