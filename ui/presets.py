import bpy
from bpy.types import Operator, Menu


def add_props(props, obj):
    for k, v in props.items():
        param = obj.liquidknot.params.add()
        param.name = k
        param.value = v


class LK_add_Sphere(Operator):
    bl_idname = "lk.add_sphere"
    bl_label = "Add_Sphere"

    def execute(self, context):
        obj = bpy.data.objects.new('LK_Sphere', None)

        # Set location to cursor
        obj.location = context.scene.cursor.location

        # Set Liquidknot props
        obj.liquidknot.active = True
        add_props({"width": 1., "height": 1., "depth": 1.}, obj)
        obj.liquidknot.de = "sdEllipsoid(p, vec3(width, height, depth))"
        context.scene.collection.objects.link(obj)

        return {'FINISHED'}


class LK_add_Cube(Operator):
    bl_idname = "lk.add_cube"
    bl_label = "Add_Cube"

    def execute(self, context):
        obj = bpy.data.objects.new('LK_Cube', None)

        # Set location to cursor
        obj.location = context.scene.cursor.location

        # Set Liquidknot props
        obj.liquidknot.active = True
        add_props({"width": 1., "height": 1., "depth": 1.}, obj)
        obj.liquidknot.de = "sdBox(p, vec3(width, height, depth))"
        context.scene.collection.objects.link(obj)

        return {'FINISHED'}


class LK_add_Menu(Menu):
    bl_idname = "VIEW3D_MT_mesh_custom_menu_add"
    bl_label = "Liquidknot"

    # noinspection PyUnusedLocal
    def draw(self, context):
        self.layout.operator_context = 'INVOKE_REGION_WIN'
        self.layout.operator("lk.add_cube", text="Cube")
        self.layout.operator("lk.add_sphere", text="Sphere")


def LK_Add_Menu_func(self, context):
    layout = self.layout
    layout.separator()
    self.layout.menu("VIEW3D_MT_mesh_custom_menu_add", icon="GROUP")


classes = [LK_add_Cube, LK_add_Sphere, LK_add_Menu]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.VIEW3D_MT_mesh_add.append(LK_Add_Menu_func)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    bpy.types.VIEW3D_MT_mesh_add.remove(LK_Add_Menu_func)
