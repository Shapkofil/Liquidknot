from .object_serialize import objects_to_json
from .camera_serialize import camera_to_json
from .light_serialize import lights_to_json
from .bounds_serialize import bounds_to_json

import json


def scene_to_json(scene, path_to_json=None):

    # Get Bounds List
    resolution, bounds = bounds_to_json(scene)

    # Camera params Fetch
    camera_dict = camera_to_json(scene.camera)

    # Entities params Fetch
    entities = [x for x in scene.objects if str(
        x.data.original).find("Mesh") > -1]
    entities_dict = objects_to_json(entities)

    # Light params Fetch
    lights = [x for x in scene.objects if str(
        x.data.original).find("Light") > -1]
    light_dict = lights_to_json(lights)

    # Combine param fetches
    scene_json = {
        "RESOLUTION": resolution,
        "BOUNDS": bounds,
        "hyper_params": {
            "float": {
                "PLANK": 0.0005,
                "MAX_DISTANCE": 1000.0,
                "EPSILON": 0.001,
                "AMBIENT": 0.1
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

    # Stringify the data
    jsoned = json.dumps(scene_json, indent=4)

    # If Path is given save it there
    if path_to_json is not None:
        with open(path_to_json, "w+") as f:
            f.write(jsoned)
    return jsoned
