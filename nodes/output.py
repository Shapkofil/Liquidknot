import nodeitems_utils
from bpy.types import ShaderNodeOutputMaterial, Node
from nodeitems_utils import NodeItem

from .base import LKShaderTreeNode, LKNodeCategory, SDFSocket


class LKShaderOutputNode(Node, LKShaderTreeNode):
    '''Shader Output'''

    bl_idname = 'LKShaderOutputNode'

    bl_label = "Liquidknot Output"

    bl_icon = 'SOUND'

    def init(self, context):
        self.inputs.new('NodeSocketSDF', 'SDF')

    # Optional: custom label
    # Explicit user label overrides this, but here we can define a label dynamically
    def draw_label(self):
        return "Liquidknot Material Output"


node_categories = [
    LKNodeCategory('OUTPUT', "Output", items=[
        NodeItem("LKShaderOutputNode")
    ])]


def register():
    nodeitems_utils.register_node_categories('LIQUIDKNOT_NODES', node_categories)


def unregister():
    nodeitems_utils.unregister_node_categories('LIQUIDKNOT_NODES')
