import bpy

from .render_settings import classes as ms_classes
from .object_settings import classes as obj_classes

from .props import register as prop_register, unregister as prop_unregister
from .presets import register as preset_register, unregister as preset_unregister

classes = ms_classes + obj_classes


def get_panels():
    exclude_panels = {
        'VIEWLAYER_PT_filter',
        'VIEWLAYER_PT_layer_passes',
        'RENDER_PT_simplify'
    }

    panels = []
    for panel in bpy.types.Panel.__subclasses__():
        if hasattr(panel, 'COMPAT_ENGINES') and {'BLENDER_RENDER', 'LIQUIDKNOT'} & set(panel.COMPAT_ENGINES):
            if panel.__name__ not in exclude_panels:
                panels.append(panel)

    return panels


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    # Special Cases
    prop_register()
    preset_register()

    # Register Builtin panels
    for panel in get_panels():
        panel.COMPAT_ENGINES.add('LIQUIDKNOT')


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    # Special Cases
    prop_unregister()
    preset_unregister()

    # Unregistering the Builtins
    for panel in get_panels():
        if 'LIQUIDKNOT' in panel.COMPAT_ENGINES:
            panel.COMPAT_ENGINES.remove('LIQUIDKNOT')
