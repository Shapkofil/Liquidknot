import bpy

import json
from os.path import abspath as ap, join, dirname

from ..std_extensions import print
from ..ui.presets.reflection import preset_to_lk, data as preset_data


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
        name='Marching Cap',
        min=1,
        default=256)

    max_dist: bpy.props.FloatProperty(
        name='Max Distance',
        min=1.,
        default=1000.)

    plank: bpy.props.FloatProperty(
        name='Plank',
        default=5 / 1000,
        subtype='DISTANCE',
        unit='LENGTH')

    epsilon: bpy.props.FloatProperty(
        name='Epsilon',
        default=5 / 1000,
        subtype='DISTANCE')

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

    obj.liquidknot.params.clear()
    preset_to_lk(preset_data[self.presets], obj)


def load_presets():
    camel = (lambda dat: ''.join("{} ".format(x.title()) for x in dat.split("_"))[:-1])
    return [(key, camel(key), "Load lk_{}".format(key))
            for key in preset_data.keys()]


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


def register():
    bpy.types.Scene.liquidknot = \
        bpy.props.PointerProperty(type=LiquidknotProps)

    bpy.types.Object.liquidknot = \
        bpy.props.PointerProperty(type=LiquidknotObjProps)


def unregister():
    del bpy.types.Scene.liquidknot

    del bpy.types.Object.liquidknot
