import bpy


class MATERIAL_UL_matslots_example(bpy.types.UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            if item:
                row = layout.row(align=True)
                row.prop(item, "name", text="")
                row.prop(item, "value")
            else:
                layout.label(text="", translate=False, icon_value=icon)
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon_value=icon)

class LKParamInsertOperator(bpy.types.Operator):
    bl_idname = "lk.param_insert"
    bl_label = "Obj Parameter Insert"

    def execute(self, context):
        params = context.object.liquidknot.params
        curr = params.add()
        return {'FINISHED'}

class MarchingObjectDataPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "March data (Liquidknot)"
    bl_idname = "OBJECT_PT_march_data"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
    COMPAT_ENGINES = {'LIQUIDKNOT'}
        

    def draw(self, context):
        layout = self.layout

        obj = context.object

        split = layout.split()
        col = split.column()
        col.template_list("MATERIAL_UL_matslots_example", "",
                          obj.liquidknot, "params", obj.liquidknot, "params")

        col = split.column()
        col.operator("lk.param_insert", icon='PLUS')
        # ToDo make a delete operator
        col.operator("lk.param_insert", icon='X')

        row = layout.row()
        row.prop(obj.liquidknot, "de")

    @classmethod
    def poll(cls, context):
        return context.engine in cls.COMPAT_ENGINES


classes = [MarchingObjectDataPanel, LKParamInsertOperator, MATERIAL_UL_matslots_example]
