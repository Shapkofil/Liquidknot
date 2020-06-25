import json
from os.path import abspath, dirname, join

from bpy.props import EnumProperty
from bpy.types import Node

from ..base import LKShaderTreeNode, complete_exp


def fetch_abstract_data(path, defauth=True):
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


abstract_data = fetch_abstract_data('abstract_presets.json')


def update_type(self, context):
    self.inputs.clear()

    for slot in abstract_data[self.abstract_type]['params'].keys():
        self.inputs.new('NodeSocketFloat', slot)


def load_presets():
    camel = (lambda dat: ''.join("{} ".format(x.title())
                                 for x in dat.split("_"))[:-1])
    return [(key, camel(key), "Load lk_{}".format(key))
            for key in abstract_data.keys()]


class LKAbstractSurfNode(Node, LKShaderTreeNode):
    '''Node for predefined surfaces'''
    bl_idname = 'LKAbstractSurfNode'
    bl_label = "Abstract Surface"
    bl_icon = 'SPHERE'

    abstract_type: EnumProperty(items=load_presets(),
                                name='abstract_type',
                                update=update_type)

    def init(self, context):
        self.outputs.new('NodeSocketSDF', "SDF")

    # Additional buttons displayed on the node.
    def draw_buttons(self, context, layout):
        layout.prop(self, 'abstract_type')

    def draw_label(self):
        camel = (lambda dat: ''.join("{} ".format(x.title())
                                     for x in dat.split("_"))[:-1])
        return camel(str(self.abstract_type))

    def update(self):
        self.outputs[0].value = complete_exp(
            abstract_data[self.abstract_type]['de'], self.inputs)
