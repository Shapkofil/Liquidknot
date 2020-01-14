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
    glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)


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

    data = np.zeros(4, [("position", np.float32, 2)])
    data["position"] = [(-1, 1), (-1, -1), (+1, +1), (1, -1)]

    program = glcu.compileProgram(vertex_code, fragment_code)
    buildBuffers(data, program)
    loc = glGetUniformLocation(program, "resolution")
    glUniform2f(loc, WIDTH, HEIGHT)

    display()

    raw_read = glcu.readPixels(0, 0, WIDTH, HEIGHT)
    refine = np.asarray(raw_read[:, :, :3] * 255, dtype=np.uint8)
    cv2.imwrite("testrender.png", refine)

    glfw.destroy_window(window)
    glfw.terminate()
