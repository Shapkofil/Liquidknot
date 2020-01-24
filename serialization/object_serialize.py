def objects_to_json(collection):
    entities = []

    for object in collection:
        entity = {}
        entity["name"] = object.name
        entity["position"] = list(object.location)
        entity["rotation"] = list(object.rotation_euler)
        entity["params"] = {"radius": .8}
        entity["de"] = "length(p) - radius"
        entities.append(entity)

    return entities
