import bpy

from ..std_extensions import print
from ..ui.presets.reflection import data as preset_data
from ..ui.presets.reflection import preset_to_lk


def update_enum_presets(self, context):
    print("Load pre-made {} data".format(self.presets))
    obj = context.object

    obj.liquidknot.params.clear()
    preset_to_lk(preset_data[self.presets], obj)


def load_presets():
    camel = (lambda dat: ''.join("{} ".format(x.title())
                                 for x in dat.split("_"))[:-1])
    return [(key, camel(key), "Load lk_{}".format(key))
            for key in preset_data.keys()]


class LiquidknotObjParams(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Name")

    value: bpy.props.FloatProperty(name="Value")


class LiquidknotObjProps(bpy.types.PropertyGroup):
    active: bpy.props.BoolProperty(name="IsActive")

    de: bpy.props.StringProperty(name='Distance Estimator',
                                 default="lenght(p) - radius")

    active_param: bpy.props.IntProperty(name="Active Parameter")

    params: bpy.props.CollectionProperty(type=LiquidknotObjParams,
                                         name="Parameters")

    presets: bpy.props.EnumProperty(name="Presets",
                                    description="Pre-made Distance Estimators",
                                    items=load_presets(),
                                    update=update_enum_presets)


def register():
    bpy.types.Object.liquidknot = \
        bpy.props.PointerProperty(type=LiquidknotObjProps)


def unregister():
    del bpy.types.Object.liquidknot
