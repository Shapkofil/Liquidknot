def camera_to_json(object, context=None):
    entity = {}
    entity["name"] = object.name
    entity["position"] = list(object.location)
    entity["rotation"] = list(object.rotation_euler.to_quaternion())

    entity["sensor"] = (object.data.sensor_width, object.data.sensor_height)
    entity["focal_length"] = (object.data.lens)

    return entity
