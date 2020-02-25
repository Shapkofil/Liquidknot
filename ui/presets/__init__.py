import bpy 
from bpy.types import Menu

from os.path import join, abspath as ap, dirname
import json

from .reflection import classes as preset_ops

# Fetch data
with open(join(dirname(ap(__file__)), "obj_presets.json")) as f:
    data = json.loads(f.read())


class LK_add_Menu(Menu):
    bl_idname = "VIEW3D_MT_lk_mesh_menu_add"
    bl_label = "Liquidknot"

    def draw(self, context):
        self.layout.operator_context = 'INVOKE_REGION_WIN'
        for cls in preset_ops:
            self.layout.operator(cls.bl_idname)


def LK_Add_Menu_func(self, context):
    layout = self.layout
    self.layout.menu("VIEW3D_MT_lk_mesh_menu_add", icon="GROUP")
    layout.separator()


classes = preset_ops + [LK_add_Menu]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.VIEW3D_MT_add.prepend(LK_Add_Menu_func)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    bpy.types.VIEW3D_MT_add.remove(LK_Add_Menu_func)
