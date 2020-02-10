import bpy
import re


class MainSettingsPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Liquidknot Settings"
    bl_idname = "RENDER_PT_lk_main_setting"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"
    COMPAT_ENGINES = {'LIQUIDKNOT'}

    def draw(self, context):
        layout = self.layout

        scene = context.scene

        layout.label(text="Hyper Parameters:")
        split = layout.split()
        col = split.column(align=True)
        col.prop(scene.liquidknot, "max_marching_steps")
        col.prop(scene.liquidknot, "max_dist")
        col.prop(scene.liquidknot, "plank")
        col.prop(scene.liquidknot, "epsilon")

        layout.separator(factor=.3)
        layout.label(text="Union Settings:")
        layout.prop(scene.liquidknot, "union_mode", text='Mode')
        if re.match(r"^SMOOTH(.+)$", scene.liquidknot.union_mode):
            layout.prop(scene.liquidknot, "union_smoothness")

    @classmethod
    def poll(cls, context):
        return context.engine in cls.COMPAT_ENGINES


classes = [MainSettingsPanel]
