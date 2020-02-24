from .object_serialize import objects_to_json
from .camera_serialize import camera_to_json
from .light_serialize import lights_to_json
from .bounds_serialize import bounds_to_json

import json


def fetch_hyper_params(scene):
    swamp = scene.liquidknot
    return {
        "float": {
            "PLANK": swamp.plank,
            "MAX_DISTANCE": swamp.max_dist,
            "EPSILON": swamp.epsilon,
            "AMBIENT": 0.1
        },
        "int": {
            "MAX_STEP": swamp.max_marching_steps
        },
        "vec4": {
            "WORLD_COLOR": [.0, .0, .0, 1.]
        }
    }


def fetch_union_pros(scene):
    lk = scene.liquidknot
    return {
        "mode": lk.union_mode,
        "value": lk.union_smoothness
    }


def scene_to_json(scene, resolution=None, bounds=None, context=None, path_to_json=None):

    # Fetch Hyperparams
    hyper_params = fetch_hyper_params(scene)

    # Get Bounds List
    resolution, bounds = bounds_to_json(scene, resolution, bounds, context)

    # Camera params Fetch
    camera_dict = camera_to_json(scene.camera, context)

    # Entities params Fetch
    entities = [x for x in scene.objects if x.liquidknot.active]
    entities_dict = objects_to_json(entities)

    # Light params Fetch
    lights = [x for x in scene.objects if str(x.data).find("Light(") > -1]
    light_dict = lights_to_json(lights)

    # Combine param fetches
    scene_json = {
        "RESOLUTION": resolution,
        "BOUNDS": bounds,
        "hyper_params": hyper_params,
        "camera": camera_dict,
        "entities": entities_dict,
        "default_union": fetch_union_pros(scene),
        "lights": light_dict
    }

    # Stringify the data
    jsoned = json.dumps(scene_json, indent=4)

    # If Path is given save it there
    if path_to_json is not None:
        with open(path_to_json, "w+") as f:
            f.write(jsoned)
    return jsoned
