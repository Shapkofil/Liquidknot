def camera_to_json(object, context=None):
    entity = {}
    entity["name"] = object.name
    if context is None:
        entity["position"] = list(object.location)
        entity["rotation"] = list(object.rotation_quaternion)
    else:
        entity["position"] = list(context.region_data.view_location)
        entity["rotation"] = list(context.region_data.view_rotation)

    entity["sensor"] = (object.data.sensor_width, object.data.sensor_height)
    entity["focal_length"] = (object.data.lens)

    return entity
