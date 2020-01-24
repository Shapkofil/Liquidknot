from .object_serialize import objects_to_json
from .camera_serialize import camera_to_json
from .light_serialize import lights_to_json

import json


def scene_to_json(scene, path_to_json=None):
    camera_dict = camera_to_json(scene.camera)

    entities = [x for x in scene.objects if str(
        x.data.original).find("Mesh") > -1]
    print(entities)
    entities_dict = objects_to_json(entities)

    lights = [x for x in scene.objects if str(
        x.data.original).find("Light") > -1]
    print(lights)
    light_dict = lights_to_json(lights)

    scene_json = {
        "hyper_params": {
            "float": {
                "PLANK": 0.0005,
                "MAX_DISTANCE": 1000.0,
                "EPSILON": 0.001,
                "AMBIENT": 0.2
            },
            "int": {
                "MAX_STEP": 1024
            },
            "vec4": {
                "WORLD_COLOR": [0.0, 0.0, 0.0, 1.0]
            }
        },
        "camera": camera_dict,
        "entities": entities_dict,
        "lights": light_dict
    }

    jsoned = json.dumps(scene_json, indent=4)

    if path_to_json is None:
        return jsoned

    with open(path_to_json, "w+") as f:
        f.write(jsoned)

    return jsoned
