import re
import json
from . import glsl_math as glsl


def de_gen(entity):
    de = entity["de"]

    # Position sub
    de = re.sub(r"p", "p - {0}".format(glsl.vec3(entity["position"])), de)

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


if __name__ == "__main__":
    with open("../scene.json") as f:
        raw = f.read()
        data = json.loads(raw)
    print(de_gen_swamp(data["entities"]))
