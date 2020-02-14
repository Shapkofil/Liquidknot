import bpy
import bmesh
from bpy.types import Operator, Menu

from ..serialization.object_serialize import add_driver, add_params


class LK_add_Sphere(Operator):
    bl_idname = "lk.add_sphere"
    bl_label = "Add_Sphere"

    def execute(self, context):
        if not context.mode == "Object":
            mesh = bpy.data.meshes.new('LK_Sphere')
            obj = bpy.data.objects.new('LK_Sphere', mesh)

            # Construct the bmesh
            bm = bmesh.new()
            bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, diameter=1)
            bm.to_mesh(mesh)
            bm.free()

            # Set location to cursor
            obj.location = context.scene.cursor.location

            # Set Liquidknot props
            obj.liquidknot.active = True
            add_params({"width": 2., "height": 2., "depth": 2.}, obj)
            add_driver(obj.liquidknot.params[0], 'value', -1, obj, 'SCALE_X', '')
            add_driver(obj.liquidknot.params[1], 'value', -1, obj, 'SCALE_Y', '')
            add_driver(obj.liquidknot.params[2], 'value', -1, obj, 'SCALE_Z', '')
            obj.liquidknot.de = "sdEllipsoid(p, vec3(width, height, depth))"
            context.scene.collection.objects.link(obj)

            # Finishing touches
            obj.select_set(True)
            context.view_layer.objects.active = obj
            bpy.ops.object.shade_smooth()

        else:
            self.report({'WARNING'}, "Liquidknot: Option only valid in Object mode")
            return {'CANCELED'}

        return {'FINISHED'}


class LK_add_Cube(Operator):
    bl_idname = "lk.add_cube"
    bl_label = "Add_Cube"

    def execute(self, context):
        if not context.mode == "Object":
            mesh = bpy.data.meshes.new('LK_Cube')
            obj = bpy.data.objects.new('LK_Cube', mesh)

            # Construct the bmesh
            bm = bmesh.new()
            bmesh.ops.create_cube(bm, size=2, calc_uvs=True)
            bm.to_mesh(mesh)
            bm.free()

            # Set location to cursor
            obj.location = context.scene.cursor.location

            # Set Liquidknot props
            obj.liquidknot.active = True
            add_params({"width": 2., "height": 2., "depth": 2.}, obj)
            add_driver(obj.liquidknot.params[0], 'value', -1, obj, 'SCALE_X', '')
            add_driver(obj.liquidknot.params[1], 'value', -1, obj, 'SCALE_Y', '')
            add_driver(obj.liquidknot.params[2], 'value', -1, obj, 'SCALE_Z', '')
            obj.liquidknot.de = "sdBox(p, vec3(width, height, depth))"
            context.scene.collection.objects.link(obj)

        else:
            self.report({'WARNING'}, "Liquidknot: Option only valid in Object mode")
            return {'CANCELED'}

        return {'FINISHED'}


class LK_add_Torus(Operator):
    bl_idname = "lk.add_torus"
    bl_label = "Add_Torus"

    def execute(self, context):
        if not context.mode == "Object":
            obj = bpy.data.objects.new('LK_Torus', None)

            # Set location to cursor
            obj.location = context.scene.cursor.location

            # Set Liquidknot props
            obj.liquidknot.active = True
            add_params({"outer_radius": 1., "inner_radius": .25}, obj)
            add_driver(obj.liquidknot.params[0], 'value', -1, obj, 'SCALE_X', '')
            obj.liquidknot.de = "sdTorus(p, vec2(outer_radius, inner_radius))"
            context.scene.collection.objects.link(obj)

        else:
            self.report({'WARNING'}, "Liquidknot: Option only valid in Object mode")
            return {'CANCELED'}

        return {'FINISHED'}


class LK_add_Octahedron(Operator):
    bl_idname = "lk.add_octahedron"
    bl_label = "Add_Octahedton"

    def execute(self, context):
        if not context.mode == "Object":
            obj = bpy.data.objects.new('LK_Octahedron', None)

            # Set location to cursor
            obj.location = context.scene.cursor.location

            # Set Liquidknot props
            obj.liquidknot.active = True
            add_params({"radius": 1.}, obj)
            add_driver(obj.liquidknot.params[0], 'value', -1, obj, 'SCALE_AVG', '')
            obj.liquidknot.de = "sdOctahedton(p, radius)"
            context.scene.collection.objects.link(obj)

        else:
            self.report({'WARNING'}, "Liquidknot: Option only valid in Object mode")
            return {'CANCELED'}

        return {'FINISHED'}


class LK_add_Capsule(Operator):
    bl_idname = "lk.add_capsule"
    bl_label = "Add_Capsule"

    def execute(self, context):
        if not context.mode == "Object":
            obj = bpy.data.objects.new('LK_Capsule', None)

            # Set location to cursor
            obj.location = context.scene.cursor.location

            # Set Liquidknot props
            obj.liquidknot.active = True
            add_params({"height": 1., "radius": .2}, obj)
            add_driver(obj.liquidknot.params[0], 'value', -1, obj, 'SCALE_Z', ' * 2')
            add_driver(obj.liquidknot.params[1], 'value', -1, obj, 'SCALE_X', ' * 0.5')
            obj.liquidknot.de = "sdVerticalCapsule(p, height, radius)"
            context.scene.collection.objects.link(obj)

        else:
            self.report({'WARNING'}, "Liquidknot: Option only valid in Object mode")
            return {'CANCELED'}

        return {'FINISHED'}


class LK_add_Menu(Menu):
    bl_idname = "VIEW3D_MT_mesh_custom_menu_add"
    bl_label = "Liquidknot"

    # noinspection PyUnusedLocal
    def draw(self, context):
        self.layout.operator_context = 'INVOKE_REGION_WIN'
        self.layout.operator("lk.add_cube", text="Cube", icon="CUBE")
        self.layout.operator("lk.add_sphere", text="Sphere", icon="SPHERE")
        self.layout.operator("lk.add_torus", text="Torus", icon="MESH_TORUS")
        self.layout.operator("lk.add_capsule", text="Capsule")


def LK_Add_Menu_func(self, context):
    layout = self.layout
    layout.separator()
    self.layout.menu("VIEW3D_MT_mesh_custom_menu_add", icon="GROUP")


classes = [LK_add_Cube,
           LK_add_Sphere,
           LK_add_Torus,
           LK_add_Capsule,
           LK_add_Menu]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.VIEW3D_MT_mesh_add.append(LK_Add_Menu_func)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    bpy.types.VIEW3D_MT_mesh_add.remove(LK_Add_Menu_func)
