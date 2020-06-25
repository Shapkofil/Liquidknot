import bpy
from bpy.props import EnumProperty
import nodeitems_utils
from nodeitems_utils import NodeItem
from bpy.types import Node

from os.path import join, abspath, dirname
import json

from ..base import LKShaderTreeNode, LKShaderTreeNode, LKNodeCategory, complete_exp


def fetch_obj_data(path, defauth=True):
    if defauth:
        path = join(dirname(abspath(__file__)), path)

    with open(path) as f:
        cont = f.read()
        try:
            return json.loads(cont)
        except:
            cont = join(dirname(abspath(__file__)),cont)
            with open(cont) as file:
                return json.loads(file.read())

obj_data = fetch_obj_data('obj_presets.json')

def update_type(self, context):
    self.inputs.clear()

    for slot in obj_data[self.prim_type]['params'].keys():
        self.inputs.new('NodeSocketFloat', slot)

def load_presets():
    camel = (lambda dat: ''.join("{} ".format(x.title()) for x in dat.split("_"))[:-1])
    return [(key, camel(key), "Load lk_{}".format(key))
            for key in obj_data.keys()]

class LKPrimitiveSurfNode(Node, LKShaderTreeNode):
    '''Node for predefined surfaces'''
    bl_idname = 'LKPrimitiveSurfNode'
    bl_label = "Primitive Surface"
    bl_icon = 'CUBE'

    prim_type:EnumProperty(items = load_presets(), name = 'prim_type', update = update_type)

    def init(self, context):
        self.outputs.new('NodeSocketSDF', "SDF")


    # Additional buttons displayed on the node.
    def draw_buttons(self, context, layout):
        layout.prop(self, 'prim_type')

    def draw_label(self):
        camel = (lambda dat: ''.join("{} ".format(x.title()) for x in dat.split("_"))[:-1])
        return camel(str(self.prim_type))

    def update(self):
        self.outputs[0].value = complete_exp(obj_data[self.prim_type]['de'], self.inputs)
