import re


def fetch_obj_params(obj):
    swamp = obj.liquidknot.params
    fetched = {}
    for param in swamp:
        fetched[param.name] = param.value
    return fetched


def obj_to_preset(obj):
    data = {}
    data["params"] = fetch_obj_params(obj)
    data["de"] = obj.liquidknot.de


def objects_to_json(collection):
    entities = []

    for object in collection:
        entity = {}
        entity["name"] = object.name
        entity["position"] = list(object.location)
        entity["rotation"] = list(object.rotation_euler.to_quaternion())
        entity["params"] = fetch_obj_params(object)
        entity["de"] = object.liquidknot.de
        entity["color"] = [.8, .8, .8, 1.] if object.active_material is None else list(object.active_material.diffuse_color)
        entities.append(entity)

    return entities


# -------------------
# Reverced
# -------------------


