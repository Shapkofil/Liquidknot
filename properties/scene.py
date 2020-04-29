import json
from os.path import abspath, dirname, join

import bpy


def setup_union_modes(scene, context):
    with open(join(dirname(abspath(__file__)), 'union_presets.json')) as f:
        data = json.loads(f.read())

    camel = (lambda dat: ''.join("{} ".format(x.title())
                                 for x in dat.split("_"))[:-1])
    items = []
    for key in data.keys():
        items.append((key, camel(key), ""))

    return items


class LiquidknotProps(bpy.types.PropertyGroup):
    max_marching_steps: bpy.props.IntProperty(name='Marching Cap',
                                              min=1,
                                              default=256)

    max_dist: bpy.props.FloatProperty(name='Max Distance',
                                      min=1.,
                                      default=1000.)

    plank: bpy.props.FloatProperty(name='Plank',
                                   default=5 / 1000,
                                   subtype='DISTANCE',
                                   unit='LENGTH')

    epsilon: bpy.props.FloatProperty(name='Epsilon',
                                     default=5 / 1000,
                                     subtype='DISTANCE')

    union_mode: bpy.props.EnumProperty(name='Union Mode',
                                       items=setup_union_modes)

    union_smoothness: bpy.props.FloatProperty(name="Smoothness", default=.3)


def register():
    bpy.types.Scene.liquidknot = \
        bpy.props.PointerProperty(type=LiquidknotProps)


def unregister():
    del bpy.types.Scene.liquidknot
