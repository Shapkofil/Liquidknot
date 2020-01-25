def camera_to_json(object):
    entity = {}
    entity["name"] = object.name
    entity["position"] = list(object.location)
    entity["rotation"] = list(object.rotation_quaternion)
    print(entity["rotation"])
    entity["focal_length"] = (object.data.lens /
                              object.data.sensor_height) * 2.

    return entity
