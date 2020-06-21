import json
from os.path import abspath, dirname, join

from bpy.props import EnumProperty
from bpy.types import Node

from ..base import LKShaderTreeNode


def fetch_boolean_data(path, defauth=True):
    if defauth:
        path = join(dirname(abspath(__file__)), path)

    with open(path) as f:
        return json.loads(f.read())


boolean_data = fetch_boolean_data('boolean_presets.json')


def update_type(self, context):
    self.inputs[2].hide = not boolean_data[self.boolean_type][0]
    self.inputs[2].default_value = boolean_data[self.boolean_type][1]


def load_presets():
    camel = (lambda dat: ''.join("{} ".format(x.title())
                                 for x in dat.split("_"))[:-1])
    return [(key, camel(key), "Load lk_{}".format(key))
            for key in boolean_data.keys()]


class LKBooleanNode(Node, LKShaderTreeNode):
    '''Node for predefined surfaces'''
    bl_idname = 'LKBooleanNode'
    bl_label = "Boolean"
    # search for a suitable icon
    bl_icon = 'CUBE'

    boolean_type: EnumProperty(items=load_presets(),
                             name='boolean_type',
                             update=update_type)

    def init(self, context):
        self.outputs.new('NodeSocketSDF', "SDF")

        self.inputs.new('NodeSocketSDF', "SDF")
        self.inputs.new('NodeSocketSDF', "SDF")
        self.inputs.new('NodeSocketFloat', "value")
        update_type(self, context)

    def draw_buttons(self, context, layout):
        layout.prop(self, 'boolean_type', text='type')

    def draw_label(self):
        camel = (lambda dat: ''.join("{} ".format(x.title())
                                     for x in dat.split("_"))[:-1])
        return camel(str(self.boolean_type))

    def update(self):
        # Makes Camel Case without space
        camel = (lambda dat: ''.join(x.title() for x in dat.split("_")))

        args = [self.inputs[0].value, self.inputs[1].value]
        if boolean_data[self.boolean_type]:
            args.append(self.inputs[2].default_value)

        self.outputs[0].value = 'op{}({})'.format(
            camel(self.boolean_type), ', '.join(str(x) for x in args))
