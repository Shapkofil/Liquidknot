import bpy
import re


class SamplingPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Sampling"
    bl_idname = "RENDER_PT_lk_sampling"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"
    COMPAT_ENGINES = {'LIQUIDKNOT'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        scene = context.scene

        split = layout.split()
        col = split.column(align=True)
        col.prop(scene.liquidknot, "max_marching_steps")
        col.prop(scene.liquidknot, "max_dist")
        col.prop(scene.liquidknot, "plank")
        col.prop(scene.liquidknot, "epsilon")

    @classmethod
    def poll(cls, context):
        return context.engine in cls.COMPAT_ENGINES


class UnionPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Sampling"
    bl_idname = "RENDER_PT_lk_union"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"
    COMPAT_ENGINES = {'LIQUIDKNOT'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        scene = context.scene

        layout.prop(scene.liquidknot, "union_mode", text='Mode')
        if re.match(r"^SMOOTH(.+)$", scene.liquidknot.union_mode):
            layout.prop(scene.liquidknot, "union_smoothness")

    @classmethod
    def poll(cls, context):
        return context.engine in cls.COMPAT_ENGINES


classes = [SamplingPanel,
           UnionPanel]
