import bpy
from bpy.props import StringProperty
from bpy.types import NodeTree, Node, NodeSocket
import nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem

import time

# Implementation of custom nodes from Python


# Derived from the NodeTree base type, similar to Menu, Operator, Panel, etc.
class LKNodeTree(NodeTree):
    # Description string
    '''A custom node tree type that will show up in the editor type list'''
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'LKShaderTree'
    # Label for nice name display
    bl_label = "Liquidknot Shader Node Tree"
    # Icon identifier
    bl_icon = 'NODETREE'


    def update(self):
        for _ in self.links:
            for link in self.links:
                if hasattr(link.from_socket, 'value') and hasattr(link.to_socket, 'value'):
                    link.from_node.update()
                    link.to_socket.value = link.from_socket.value
                    link.to_node.update()

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
        if self.is_output:
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
