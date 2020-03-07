from os.path import join, abspath, dirname

from . import auto_load
import json
from os.path import abspath, join, dirname

from .setup import unpack

bl_info = {
    'name': 'Liquidknot',
    'description': 'Ray Marcher',
    'author': 'Kiril Iliev (Shapkofil)',
    'license': 'GNUv3 Affero',
    'deps': '',
    'version': (1, 0, 0),
    'blender': (2, 82, 0),
    'warning': '',
    'wiki_url': 'https://github.com/Shapkfil/Liquidknot',
    'tracker_url': 'liquidknot.blender@gmail.com',
    'support': 'COMMUNITY',
    'category': 'Rendering Engine'
}


with open(join(dirname(abspath(__file__)), 'paths.json')) as f:
    global PATHS
    PATHS = json.loads(f.read())

for key in PATHS.keys():
    PATHS[key] = join(dirname(abspath(__file__)), PATHS[key])


def register():
    unpack()
    auto_load.init()
    auto_load.register()


def unregister():
    auto_load.unregister()


if __name__ == "__main__":
    register()
