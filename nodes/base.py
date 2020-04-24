import bpy
from bpy.props import StringProperty
from bpy.types import NodeTree, Node, NodeSocket
import nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem

# Implementation of custom nodes from Python


# Derived from the NodeTree base type, similar to Menu, Operator, Panel, etc.
class LKShaderTree(NodeTree):
    # Description string
    '''A custom node tree type that will show up in the editor type list'''
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'LKShaderTree'
    # Label for nice name display
    bl_label = "Liquidknot Shader Node Tree"
    # Icon identifier
    bl_icon = 'NODETREE'

    def update(self):
        for from_socket, to_socket in self.links:
            if hasattr(from_socket, 'value') and hasattr(to_socket, 'value'):
                to_socket.value = from_socket.value

    # @classmethod
    # def poll(context):
    #     return context.scene.render.engine == 'LIQUIDKNOT'


class LKShaderTreeNode:
    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'LKShaderTree'


# Signed Distance Field Socket
class SDFSocket(NodeSocket):
    # Description string
    '''Custom node socket type'''
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'NodeSocketSDF'
    # Label for nice name display
    bl_label = "Signed Distance Field"

    value: StringProperty(name="Value", description="String value of the socket")

    # Optional function for drawing the socket input value
    def draw(self, context, layout, node, text):
        if self.is_output or self.is_linked:
            layout.label(text=text)
        else:
            obj = context.object
            layout.prop(self, "value", text=text)

    # Socket color
    def draw_color(self, context, node):
        # Mild green
        return (41. / 255., 204. / 255., 195. / 255., 1.)


class LKNodeCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.scene.render.engine == 'LIQUIDKNOT'
