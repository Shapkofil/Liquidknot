import bpy


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


class LiquidknotObjParams(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Name")

    value: bpy.props.FloatProperty(name="Value")


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
