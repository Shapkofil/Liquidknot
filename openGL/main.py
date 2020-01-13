from OpenGL.GL import *
from OpenGL.GLU import *
import glfw

import cv2
import gl_utils as glcu

import sys
import numpy as np
import ctypes


vertex_code = open("vertex.shader").read()

fragment_code = open("fragment.shader").read()


def reshape(width, height):
    glViewport(0, 0, width, height)


def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glDrawArrays(GL_TRIANGLE_STRIP, 0, 3)


def keyboard(key, x, y):
    if key == 'q':
        sys.exit()


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

    offset = ctypes.c_void_p(data.dtype["position"].itemsize)
    loc = glGetAttribLocation(program, "color")
    glEnableVertexAttribArray(loc)
    glBindBuffer(GL_ARRAY_BUFFER, buff)
    glVertexAttribPointer(loc, 4, GL_FLOAT, False, stride, offset)


if __name__ == "__main__":

    # Hyper Params
    # ToDo Get hyper Params externaly
    WIDTH = 640
    HEIGHT = 480

    if not glfw.init():
        print("glfw failed!!!")
        raise RuntimeError("glfw init error")
        exit()

    glfw.window_hint(glfw.VISIBLE, False)
    window = glfw.create_window(WIDTH, HEIGHT, "Phantom", None, None)
    if not window:
        print("glfw window failed")
        glfw.terminate()
        raise RuntimeError("glfw window error")
        exit()

    glfw.make_context_current(window)

    data = np.zeros(3, [("position", np.float32, 2), ("color", np.float32, 4)])
    data["position"] = [(.0, 1.), (1, -1), (-1, -1)]
    data["color"] = [(.8, .0, .0, 1.),
                     (.0, .8, .0, 1.),
                     (.0, .0, .8, 1.)]

    program = glcu.compileProgram(vertex_code, fragment_code)
    buildBuffers(data, program)
    loc = glGetUniformLocation(program, "color")
    glUniform4f(loc, 0.0, 0.54, .2, 1.0)

    display()

    raw_read = glcu.readPixels(0, 0, WIDTH, HEIGHT)
    refine = np.asarray(raw_read[:, :, :3] * 255, dtype=np.uint8)
    cv2.imwrite("testrender.png", refine)

    glfw.destroy_window(window)
    glfw.terminate()
