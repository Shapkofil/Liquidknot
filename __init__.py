bl_info = {
    'name': 'Liquidknot',
    'description': 'Ray Marcher',
    'author': 'Kiril Iliev (Shapkofil)',
    'license': 'GNUv3 Affero',
    'deps': '',
    'version': (1, 0, 0),
    'blender': (2, 81, 0),
    'warning': '',
    'wiki_url': 'https://github.com/Shapkfil/Liquidknot',
    'tracker_url': 'liquidknot.blender@gmail.com',
    'support': 'COMMUNITY',
    'category': 'Rendering Engine'
}

from .engine_wrap import register as engine_register, unregister as engine_unregister
from .ui import register as ui_register, unregister as ui_unregister, classes as ui_classes

from .setup import unpack


def register():
    unpack()
    ui_register()
    engine_register()


def unregister():
    ui_unregister()
    engine_unregister()


if __name__ == "__main__":
    register()
