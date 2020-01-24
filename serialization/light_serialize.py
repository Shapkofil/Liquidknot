def lights_to_json(collection):
    entities = []

    for object in collection:
        entity = {}
        entity["name"] = object.name
        entity["position"] = list(object.location)
        entity["color"] = list(object.color)
        entities.append(entity)

    return entities
