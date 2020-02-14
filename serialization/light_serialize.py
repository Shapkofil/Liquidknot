def lights_to_json(collection):
    entities = []

    for object in collection:
        entity = {}
        entity["name"] = object.name
        entity["position"] = list(object.location)
        entity["color"] = [3., 3., 3.]
        entity["color"].append(1.)
        entities.append(entity)

    return entities
