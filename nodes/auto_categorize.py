import inspect
from os.path import basename, dirname

import nodeitems_utils
from bpy.types import Node

from .. import auto_load
from .base import LKNodeCategory


def register():
    ordered_classes = auto_load.ordered_classes
    ordered_classes = [x for x in ordered_classes if issubclass(x, Node)]
    node_dict = {}
    for cls in ordered_classes:
        package = basename(dirname(inspect.getfile(cls)))
        if package not in node_dict.keys():
            node_dict[package] = []
        node_dict[package].append(cls.bl_idname)

    node_categories = []
    for cat in node_dict.keys():
        node_categories.append(
            LKNodeCategory(
                cat.upper(),
                cat.capitalize(),
                items=[nodeitems_utils.NodeItem(x) for x in node_dict[cat]]))

    nodeitems_utils.register_node_categories('LIQUIDKNOT_NODES',
                                             node_categories)


def unregister():
    nodeitems_utils.unregister_node_categories('LIQUIDKNOT_NODES')
