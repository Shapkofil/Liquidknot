from bl_ui.properties_material import MaterialButtonsPanel
from bpy.types import Panel, Menu
from ..ui import icons


class LIQUIDKNOT_PT_context_material(MaterialButtonsPanel, Panel):
    """
    Material UI Panel
    """
    COMPAT_ENGINES = {"LIQUIDKNOT"}
    bl_label = ""
    bl_options = {"HIDE_HEADER"}
    bl_order = 1

    @classmethod
    def poll(cls, context):
        engine = context.scene.render.engine
        return (context.material or context.object) and (engine == "LIQUIDKNOT")

    def draw(self, context):
        layout = self.layout

        mat = context.material
        obj = context.object
        slot = context.material_slot
        space = context.space_data

        # Re-create the Blender material UI, but without the surface/wire/volume/halo buttons
        if obj:
            is_sortable = len(obj.material_slots) > 1
            rows = 1
            if (is_sortable):
                rows = 4

            row = layout.row()

            row.template_list("MATERIAL_UL_matslots", "", obj, "material_slots", obj, "active_material_index", rows=rows)

            col = row.column(align=True)
            col.operator("object.material_slot_add", icon='ADD', text="")
            col.operator("object.material_slot_remove", icon='REMOVE', text="")

            col.menu("MATERIAL_MT_context_menu", icon='DOWNARROW_HLT', text="")

            if is_sortable:
                col.separator()

                col.operator("object.material_slot_move", icon='TRIA_UP', text="").direction = 'UP'
                col.operator("object.material_slot_move", icon='TRIA_DOWN', text="").direction = 'DOWN'

            if obj.mode == 'EDIT':
                row = layout.row(align=True)
                row.operator("object.material_slot_assign", text="Assign")
                row.operator("object.material_slot_select", text="Select")
                row.operator("object.material_slot_deselect", text="Deselect")

        if obj:
            # Note that we don't use layout.template_ID() because we can't
            # control the copy operator in that template.
            # So we mimic our own template_ID.

            row = layout.row(align=True)
            row.operator("luxcore.material_select", icon=icons.MATERIAL, text="")

            if obj.active_material:
                row.prop(obj.active_material, "name", text="")
                if obj.active_material.users > 1:
                    # TODO this thing is too wide
                    row.operator("luxcore.material_copy", text=str(obj.active_material.users))
                row.prop(obj.active_material, "use_fake_user", text="")
                row.operator("luxcore.material_copy", text="", icon=icons.DUPLICATE)
                row.operator("luxcore.material_unlink", text="", icon=icons.CLEAR)
            else:
                row.operator("luxcore.material_new", text="New", icon=icons.ADD)

            if slot:
                row = row.row()
                row.prop(slot, "link", text="")
            else:
                row.label()
        elif mat:
            layout.template_ID(space, "pin_id")
            layout.separator()

        if mat:
            if mat.luxcore.node_tree or (mat.use_nodes and mat.node_tree and mat.luxcore.use_cycles_nodes):
                layout.operator("luxcore.material_show_nodetree", icon=icons.SHOW_NODETREE)

            if mat.use_nodes and mat.node_tree:
                layout.prop(mat.luxcore, "use_cycles_nodes")
                layout.operator("luxcore.use_cycles_nodes_everywhere")

            if not mat.luxcore.node_tree and not mat.luxcore.use_cycles_nodes:
                layout.operator("luxcore.mat_nodetree_new", icon="NODETREE", text="Use LuxCore Material Nodes")


class LIQUIDKNOT_PT_material_presets(MaterialButtonsPanel, Panel):
    COMPAT_ENGINES = {"LIQUIDKNOT"}
    bl_label = "Node Tree Presets"
    bl_order = 2

    @classmethod
    def poll(cls, context):
        engine = context.scene.render.engine
        return engine == "LIQUIDKNOT" and (context.material and not context.material.luxcore.use_cycles_nodes)

    def draw(self, context):
        layout = self.layout

        row = layout.row()

        # for category, presets in LIQUIDKNOT_OT_preset_material.categories.items():
        #     col = row.column()
        #     col.label(text=category)

        #     for preset in presets:
        #         op = col.operator("luxcore.preset_material", text=preset)
        #         op.preset = preset


# class LIQUIDKNOT_PT_settings(MaterialButtonsPanel, Panel):
##    bl_label = "Settings"
##    bl_context = "material"
##    bl_options = {'DEFAULT_CLOSED'}
##
# @classmethod
# def poll(cls, context):
##        engine = context.scene.render.engine
# return context.material and engine == "LIQUIDKNOT"
##
# def draw(self, context):
##        layout = self.layout
##        mat = context.material
##
# if mat.luxcore.auto_vp_color:
##            split = layout.split(factor=0.8)
##            split.prop(mat.luxcore, "auto_vp_color")
##            row = split.row()
##            row.enabled = not mat.luxcore.auto_vp_color
##            row.prop(mat, "diffuse_color", text="")
# else:
##            layout.prop(mat.luxcore, "auto_vp_color")
##            layout.prop(mat, "diffuse_color", text="Viewport Color")


class LIQUIDKNOT_PT_material_preview(MaterialButtonsPanel, Panel):
    COMPAT_ENGINES = {"LIQUIDKNOT"}
    bl_label = "Preview"
    bl_options = {"DEFAULT_CLOSED"}
    bl_order = 3

    @classmethod
    def poll(cls, context):
        engine = context.scene.render.engine
        return context.material and (engine == "LIQUIDKNOT")

    def draw(self, context):
        layout = self.layout
        layout.template_preview(context.material)
        row = layout.row(align=True)
        preview = context.material.luxcore.preview
        row.prop(preview, "zoom")
        row.prop(preview, "size")


classes = [LIQUIDKNOT_PT_context_material,
           LIQUIDKNOT_PT_material_presets,
           LIQUIDKNOT_PT_material_preview]
