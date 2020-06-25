import bpy
from bpy.types import Menu

from os.path import join, abspath as ap, dirname
import json

from .reflection import classes as preset_ops

def fetch_data(path, defauth=True):
    if defauth:
        path = join(dirname(ap(__file__)), path)

    with open(path) as f:
        cont = f.read()
        try:
            return json.loads(cont)
        except:
            cont = join(dirname(ap(__file__)),cont)
            with open(cont) as file:
                return json.loads(file.read())

data = fetch_data('obj_presets.json')


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
    bpy.types.VIEW3D_MT_add.prepend(LK_Add_Menu_func)


def unregister():
    bpy.types.VIEW3D_MT_add.remove(LK_Add_Menu_func)
