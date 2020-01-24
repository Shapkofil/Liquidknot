def camera_to_json(object):
    entity = {}
    entity["name"] = object.name
    entity["position"] = list(object.location)
    entity["rotation"] = list(object.rotation_euler)
    entity["focal_length"] = 1.0
    entity["field_of_view"] = .5

    return entity
