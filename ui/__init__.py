import bpy

from .hyperparams import classes as hp_classes
from .props import register as prop_register, unregister as prop_unregister
from .objectpanel import classes as obj_classes
from .presets import register as preset_register, unregister as preset_unregister

classes = hp_classes + obj_classes


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    # Special Cases
    prop_register()
    preset_register()


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    # Special Cases
    prop_unregister()
    preset_unregister()
