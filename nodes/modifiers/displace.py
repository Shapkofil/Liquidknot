from bpy.types import Node

from ..base import LKShaderTreeNode


class LKDisplaceNode(Node, LKShaderTreeNode):
    '''Node for predefined surfaces'''
    bl_idname = 'LKDisplaceNode'
    bl_label = "Displace"
    # search for a suitable icon
    bl_icon = 'CUBE'

    def init(self, context):
        self.outputs.new('NodeSocketSDF', "SDF")

        self.inputs.new('NodeSocketSDF', "Base")
        self.inputs.new('NodeSocketSDF', "Displacement")
        self.inputs.new('NodeSocketFloat', "Fac")

    def draw_label(self):
        return 'Displace'

    def update(self):
        self.outputs[0].value = '{} + {} * {}'.format(
            self.inputs[0].value, self.inputs[2].default_value,
            self.inputs[1].value)
