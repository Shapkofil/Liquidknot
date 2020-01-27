import bpy

from .hyperparams import HyperParamsPanel as hp_panel
from .props import register as prop_register, LiquidknotProps as props

classes = [props, hp_panel]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    prop_register()


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
