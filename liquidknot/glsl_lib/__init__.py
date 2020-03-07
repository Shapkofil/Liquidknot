from .glsl_math import *

import os

# Get glsl custom library
f = open(os.path.join(os.path.dirname(__file__), "lib.shader"))
lib_code = f.read()
f.close()
