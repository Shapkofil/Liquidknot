import bpy


class LK_UL_deparamsList(bpy.types.UIList):

    def draw_item(self, context, layout, data,
                  item, icon, active_data, active_propname):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            if item:
                row = layout.row(align=True)
                row.prop(item, "name", text="")
                row.prop(item, "value", text="")
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
        curr.name = "param_{0}".format(len(params))
        return {'FINISHED'}


class LKParamDeleteOperator(bpy.types.Operator):
    bl_idname = "lk.param_delete"
    bl_label = "Obj Parameter Delete"

    def execute(self, context):
        params = context.object.liquidknot.params
        active_index = context.object.liquidknot.active_param
        params.remove(active_index)
        return {'FINISHED'}


class MarchingObjectDataPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_idname = "OBJECT_PT_march_data"
    bl_label = "Object Data (liquidknot)"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
    COMPAT_ENGINES = {'LIQUIDKNOT'}

    def draw_header(self, context):
        layout = self.layout.row(align=True)
        obj = context.object
        layout.prop(obj.liquidknot, "active", text="")

    def draw(self, context):
        layout = self.layout

        obj = context.object

        col = layout.grid_flow(columns=2, align=True)
        col.template_list("LK_UL_deparamsList",
                          "",
                          obj.liquidknot,
                          "params",
                          obj.liquidknot,
                          "active_param")

        box = col.column()

        box.operator("lk.param_insert",
                     icon='PLUS',
                     text="")

        # ToDo make a delete operator
        box.operator("lk.param_delete",
                     icon='X',
                     text="")

        col = layout.column()
        col.template_list("LK_UL_deparamsList",
                          "compact",
                          obj.liquidknot,
                          "params",
                          obj.liquidknot,
                          "active_param",
                          type='COMPACT')
        col.prop(obj.liquidknot, "de")

    @classmethod
    def poll(cls, context):
        return context.engine in cls.COMPAT_ENGINES


classes = [MarchingObjectDataPanel,
           LKParamInsertOperator,
           LKParamDeleteOperator,
           LK_UL_deparamsList]
