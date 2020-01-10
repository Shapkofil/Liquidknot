bl_info = {
    'name': 'Liquidknot',
    'description': 'Ray Marcher',
    'author': 'Kiril Iliev (Shapkofil)',
    'license': 'MIT',
    'deps': '',
    'version': (1, 0, 0),
    'blender': (2, 81, 0),
    'location': 'View3D > Sidebar > Create > Archipack',
    'warning': '',
    'wiki_url': 'https://github.com/Shapkfil/Liquidknot',
    'tracker_url': 'https://github.com/s-leger/archipack/issues',
    'link': 'https://github.com/s-leger/archipack',
    'support': 'COMMUNITY',
    'category': 'Rendering Engine'
}

import os
import bpy
from .engine_wrap import register as register_engine , unregister as unregister_engine

def register():
    register_engine()


def unregister():
    unregister_engine()


if __name__ == "__main__":
    register()
