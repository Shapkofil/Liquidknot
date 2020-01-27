import bpy


class HyperParamsPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Hyper Parameters"
    bl_idname = "RENDER_PT_hyper_params"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"

    def draw(self, context):
        layout = self.layout

        scene = context.scene

        split = layout.split()
        col = split.column(align=True)
        col.prop(scene.liquidknot, "max_marching_steps")
        col.prop(scene.liquidknot, "max_dist")
        col.prop(scene.liquidknot, "plank")

        layout.label(text="Constants: ")
        row = layout.row()
        row.prop(scene.liquidknot, "epsilon")
