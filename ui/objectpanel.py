import bpy


class MATERIAL_UL_matslots_example(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        ob = data
        slot = item
        ma = slot.material
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            if ma:
                layout.prop(ma, "name", text="", emboss=False)
            else:
                layout.label(text="", translate=False, icon_value=icon)
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon_value=icon)


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

        row = layout.row()
        row.prop(obj.liquidknot, "de")

    @classmethod
    def poll(cls, context):
        return context.engine in cls.COMPAT_ENGINES


classes = [MarchingObjectDataPanel, MATERIAL_UL_matslots_example]
