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


def register():
    bpy.types.Scene.liquidknot = \
        bpy.props.PointerProperty(type=LiquidknotProps)
