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

from .engine_wrap import register as engine_register, unregister as engine_unregister
from .ui import register as ui_register, unregister as ui_unregister, classes as ui_classes


def register():
    ui_register()
    engine_register()


def unregister():
    ui_unregister()
    engine_unregister()


if __name__ == "__main__":
    register()
