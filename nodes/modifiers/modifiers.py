import bpy
from bpy.props import EnumProperty
from bpy.types import Node

from os.path import join, abspath, dirname
import json

from ..base import LKShaderTreeNode, LKShaderTreeNode, LKNodeCategory, complete_exp


def fetch_data(path, defauth=True):
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

mod_data = fetch_data('mod_presets.json')

def update_type(self, context):
    self.inputs.clear()

    for slot in mod_data[self.mod_type]['params']:
        self.inputs.new('NodeSocketSDF', slot)

def load_presets():
    camel = (lambda dat: ''.join("{} ".format(x.title()) for x in dat.split("_"))[:-1])
    return [(key, camel(key), "Load lk_{}".format(key))
            for key in mod_data.keys()]

class LKModifierNode(Node, LKShaderTreeNode):
    '''Node for predefined modifiers'''
    bl_idname = 'LKModifierNode'
    bl_label = "Modifier"
    bl_icon = 'CUBE'

    mod_type:EnumProperty(items = load_presets(), name = 'mod_type', update = update_type)

    def init(self, context):
        self.outputs.new('NodeSocketSDF', "SDF")


    # Additional buttons displayed on the node.
    def draw_buttons(self, context, layout):
        layout.prop(self, 'mod_type', text = "")

    def draw_label(self):
        camel = (lambda dat: ''.join("{} ".format(x.title()) for x in dat.split("_"))[:-1])
        return camel(str(self.mod_type))

    def update(self):
        try:
            self.outputs[0].value = mod_data[self.mod_type]['exp'].format(*[x.value for x in self.inputs])
        except:
            pass
