from OpenGL.GL import *
from OpenGL.GLU import *

import pygame
from pygame.locals import *

from . import gl_utils as glcu

import numpy as np
import ctypes

import os


def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)


def buildBuffers(data, program):
    buff = glGenBuffers(1)

    glBindBuffer(GL_ARRAY_BUFFER, buff)
    glBufferData(GL_ARRAY_BUFFER, data.nbytes, data, GL_DYNAMIC_DRAW)

    stride = data.strides[0]

    offset = ctypes.c_void_p(None)
    loc = glGetAttribLocation(program, "position")
    glEnableVertexAttribArray(loc)
    glBindBuffer(GL_ARRAY_BUFFER, buff)
    glVertexAttribPointer(loc, 2, GL_FLOAT, False, stride, offset)


def render(resolution=(1920, 1080),
           bounds=(0, 0, 1920, 1080),
           vertex_code=None,
           fragment_code=None):

    # Default shader code
    if vertex_code is None:
        vertex_code = open(os.path.join(
            os.path.dirname(__file__), "vertex.shader")).read()

    if fragment_code is None:
        fragment_code = open(os.path.join(
            os.path.dirname(__file__), "fragment.shader")).read()

    # Hyper Params
    # ToDo Get hyper Params externaly
    WIDTH = resolution[0]
    HEIGHT = resolution[1]

    pygame.init()
    pygame.display.set_mode(resolution, DOUBLEBUF | OPENGL)

    data = np.zeros(4, [("position", np.float32, 2)])
    data["position"] = [(-1, 1), (-1, -1), (+1, +1), (1, -1)]

    program = glcu.compileProgram(vertex_code, fragment_code)
    buildBuffers(data, program)
    loc = glGetUniformLocation(program, "resolution")
    glUniform2f(loc, WIDTH, HEIGHT)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    display()

    pixels = glcu.readPixels(bounds[0], bounds[1], bounds[2], bounds[3])

    pygame.quit()

    return pixels
