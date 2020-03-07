# -------------------------
# INIT + INHERIT PANELS
# -------------------------

import bpy


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
    # Register Builtin panels
    for panel in get_panels():
        panel.COMPAT_ENGINES.add('LIQUIDKNOT')


def unregister():
    # Unregistering the Builtins
    for panel in get_panels():
        if 'LIQUIDKNOT' in panel.COMPAT_ENGINES:
            panel.COMPAT_ENGINES.remove('LIQUIDKNOT')
