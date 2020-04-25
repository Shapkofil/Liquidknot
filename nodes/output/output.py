import nodeitems_utils
import bpy
from bpy.types import ShaderNodeOutputMaterial, Node
from nodeitems_utils import NodeItem

from ..base import LKShaderTreeNode, SDFSocket


class LKShaderOutputNode(Node, LKShaderTreeNode):
    '''Shader Output'''

    bl_idname = 'LKShaderOutputNode'

    bl_label = "Output"

    bl_icon = 'SOUND'

    def init(self, context):
        self.inputs.new('NodeSocketSDF', 'SDF')

    # Optional: custom label
    # Explicit user label overrides this, but here we can define a label dynamically
    def draw_label(self):
        return "Output"
    
    def update(self):
        bpy.context.object.liquidknot.enabled = True
        bpy.context.object.liquidknot.de = self.inputs[0].value
