import bpy


def camera_to_json(object):
    entity = {}
    entity["name"] = object.name
    entity["position"] = list(object.location)
    entity["rotation"] = list(object.rotation_quaternion)
    print(entity["rotation"])
    entity["focal_length"] = (bpy.data.cameras[object.name].lens /
                              bpy.data.cameras[object.name].sensor_height) * 2.
    entity["field_of_view"] = .5

    return entity
