import bpy
from bpy.props import EnumProperty
import nodeitems_utils
from nodeitems_utils import NodeItem

from bpy.types import Node

from os.path import join, abspath, dirname
import json

from ..base import LKShaderTreeNode, LKShaderTreeNode, LKNodeCategory


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
        self.outputs[0].value = '{} + {} * {}'.format(self.inputs[0].value, self.inputs[2].default_value,self.inputs[1].value)    
