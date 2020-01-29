import bpy

from .hyperparams import classes as hp_classes
from .props import register as prop_register, unregister as prop_unregister
from .objectpanel import classes as obj_classes

classes = hp_classes + obj_classes


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    prop_register()


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    prop_unregister()