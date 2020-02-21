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
        entity["rotation"] = list(object.rotation_quaternion)
        entity["params"] = fetch_obj_params(object)
        entity["de"] = object.liquidknot.de
        entity["color"] = [.8, .8, .8, 1.] if object.active_material is None else list(object.active_material.diffuse_color)
        entities.append(entity)

    return entities


# -------------------
# Reverced
# -------------------

def add_driver(obj, prop, index, source, source_prop, expression=''):
    drv = obj.driver_add(prop, index)
    var = drv.driver.variables.new()

    # Proper Name
    var.name = prop + "_var"
    var.type = 'TRANSFORMS'

    # Set up source
    target = var.targets[0]
    target.id = source
    target.transform_type = source_prop
    target.transform_space = "WORLD_SPACE"

    # Set up Expression if nessesary
    drv.driver.expression = var.name + expression


def add_params(props, obj):
    for i, (k, v) in enumerate(props.items()):
        param = obj.liquidknot.params.add()
        param.name = k
        param.value = v if type(v) == float else 1.
        if type(v) is not float:
            exp = re.search(r"([A-Z]+_[A-Z]{1,3}) ?(.*)", v).groups()
            add_driver(obj.liquidknot.params[i], 'value', -1, obj, exp[0], exp[1])


def preset_to_lk(data, obj):
    add_params(data["params"], obj)
    obj.liquidknot.de = data["de"]
