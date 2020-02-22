import bpy

import json
from os.path import abspath as ap, join, dirname

from ..std_extensions import print
from ..serialization.object_serialize import preset_to_lk


def setup_union_modes(scene, context):
    items = [
        ('UNION', "Union", ""),
        ('SUBTRACTION', "Subtraction", ""),
        ('INTERSECTION', "Intersection", ""),
        ('SMOOTH_UNION', "Smooth Union", ""),
        ('SMOOTH_SUBTRACTION', "Smooth Subtraction", ""),
        ('SMOOTH_INTERSECTION', "Smooth Intersection", ""),
    ]
    return items


class LiquidknotProps(bpy.types.PropertyGroup):
    max_marching_steps: bpy.props.IntProperty(
        name='Max Marching Steps',
        min=1,
        default=256)

    max_dist: bpy.props.FloatProperty(
        name='Max Distance',
        min=1.,
        default=1000.)

    plank: bpy.props.FloatProperty(
        name='Plank Distance',
        default=.005,
        min=.00005,
        precision=5)

    epsilon: bpy.props.FloatProperty(
        name='Epsilon Constant',
        default=.005,
        min=.00005,
        precision=5)

    union_mode: bpy.props.EnumProperty(
        name='Union Mode',
        items=setup_union_modes)

    union_smoothness: bpy.props.FloatProperty(
        name="Smoothness",
        default=.3)


class LiquidknotObjParams(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Name")

    value: bpy.props.FloatProperty(name="Value")


# -----------------
# Object Props
# -----------------

def update_enum_presets(self, context):
    print("Load pre-made {} data".format(self.presets))
    obj = context.object

    # Fetch data
    with open(join(dirname(ap(__file__)), "obj_presets.json")) as f:
        data = json.loads(f.read())[self.presets]

    obj.liquidknot.params.clear()
    preset_to_lk(data, obj)


def load_presets():
    with open(join(dirname(ap(__file__)), "obj_presets.json")) as f:
        data = json.loads(f.read())
        return [(key, key.casefold().capitalize(), "Load lk_{}".format(key.casefold().capitalize()))
                for key in data.keys()]


class LiquidknotObjProps(bpy.types.PropertyGroup):
    active: bpy.props.BoolProperty(
        name="IsActive")

    de: bpy.props.StringProperty(
        name='Distance Estimator',
        default="lenght(p) - radius")

    active_param: bpy.props.IntProperty(
        name="Active Parameter")

    params: bpy.props.CollectionProperty(
        type=LiquidknotObjParams,
        name="Parameters")

    presets: bpy.props.EnumProperty(
        name="Presets",
        description="Pre-made Distance Estimators",
        items=load_presets(),
        update=update_enum_presets
    )


classes = [LiquidknotProps, LiquidknotObjParams, LiquidknotObjProps]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.liquidknot = \
        bpy.props.PointerProperty(type=LiquidknotProps)

    bpy.types.Object.liquidknot = \
        bpy.props.PointerProperty(type=LiquidknotObjProps)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.liquidknot

    del bpy.types.Object.liquidknot
