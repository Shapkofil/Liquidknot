import bpy
import bmesh
from bpy.types import Operator

from os.path import join, abspath as ap, dirname
import json
import re


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


# List the Flat Shaded primitives
flats = ["cube", "octahedron", "cylinder"]


# Fetch data
with open(join(dirname(ap(__file__)), "obj_presets.json")) as f:
    data = json.loads(f.read())


def shade_s(obj, mode=True):
    if not obj.data.polygons[0] == mode:
        for poly in obj.data.polygons:
            poly.use_smooth = mode


def OperatorFactory(name):
    snake = re.sub(" ", "_", name.lower())
    camel = '_'.join([x.title() for x in re.sub("_", " ", name).split()])
    CAPS_SNAKE = snake.upper()

    def execute(self, context):
        if not context.mode == "Object":
            mesh = bpy.data.meshes.new('LK_{}'.format(camel))
            obj = bpy.data.objects.new('LK_{}'.format(camel), mesh)

            # Construct the bmesh
            bm = bmesh.new()
            try:
                meshtod = getattr(bmesh.ops, "create_{}".format(snake))
                meshtod(bm)
            except:
                path_to_file = join(dirname(ap(__file__)), "{}.obj".format(snake))
                bpy.ops.import_scene.obj(filepath=path_to_file)
                mesh_host = context.selected_objects[0]
                bm.from_mesh(mesh_host.data)
                bpy.ops.object.delete()
            bm.to_mesh(mesh)
            bm.free()

            # Set location to cursor
            obj.location = context.scene.cursor.location

            # Set Liquidknot props
            obj.liquidknot.active = True
            preset_to_lk(data[CAPS_SNAKE], obj)
            context.scene.collection.objects.link(obj)

            # Finishing touches
            shade_s(obj, snake not in flats)

        else:
            self.report({'WARNING'}, "Liquidknot: Option only valid in Object mode")
            return {'CANCELED'}

        return {'FINISHED'}

    # Load Args
    newcls = type("LK_Add_{}".format(camel), (Operator, ), {"execute": execute})
    setattr(newcls, "bl_idname", "lk.add_{}".format(snake))
    setattr(newcls, "bl_label", "{}".format(re.sub("_", " ", camel)))

    return newcls


classes = [OperatorFactory(key) for key in data.keys()]


if __name__ == "__main__":
    newcls = OperatorFactory("INFINITE_CYLINDER")
    print(newcls.bl_label)
