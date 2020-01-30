def fetch_obj_params(obj):
    swamp = obj.liquidknot.params
    fetched = {}
    for param in swamp:
        fetched[param.name] = param.value
    return fetched


def objects_to_json(collection):
    entities = []

    for object in collection:
        entity = {}
        entity["name"] = object.name
        entity["position"] = list(object.location)
        entity["rotation"] = list(object.rotation_euler)
        entity["params"] = fetch_obj_params(object)
        entity["de"] = object.liquidknot.de
        entities.append(entity)

    return entities
