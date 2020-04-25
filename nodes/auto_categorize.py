from bpy.types import Node
from os.path import dirname, basename
import inspect
import nodeitems_utils

from .base import LKNodeCategory
from .. import auto_load

def register():
    ordered_classes = auto_load.ordered_classes
    ordered_classes = [x for x in ordered_classes if issubclass(x, Node)]
    node_dict = {}
    for cls in ordered_classes:
        package = basename(dirname(inspect.getfile(cls)))
        if not package in node_dict.keys():
            node_dict[package] = []
        node_dict[package].append(cls.bl_idname)

    print(node_dict)

    node_categories = []
    for cat in node_dict.keys():
        node_categories.append(
           LKNodeCategory(cat.upper(), cat.capitalize(),items=[
               nodeitems_utils.NodeItem(x) for x in node_dict[cat]
           ]))

    nodeitems_utils.register_node_categories('LIQUIDKNOT_NODES', node_categories)

def unregister():
    nodeitems_utils.unregister_node_categories('LIQUIDKNOT_NODES')


