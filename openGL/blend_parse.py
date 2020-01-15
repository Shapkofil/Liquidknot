from .render import render
import numpy as np


def render_blend(resolution,
                 vertex_code=None,
                 fragment_code=None):
    refine = np.reshape(render(resolution, vertex_code, fragment_code),
                        (resolution[0] * resolution[1], 4))
    return refine.tolist()
