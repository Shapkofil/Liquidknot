from OpenGL.GL import *

import numpy as np


def compileShader(shader, shader_type):
    glCompileShader(shader)
    if not glGetShaderiv(shader, GL_COMPILE_STATUS):
        error = glGetShaderInfoLog(shader).decode()
        st = "vertex" if shader_type == GL_VERTEX_SHADER else "fragment"
        print("{0} shader error:\n{1}".format(st, error))
        raise RuntimeError("{0} shader compilation error".format(st))


def compileProgram(vertex_code, fragment_code):
    program = glCreateProgram()
    vertex = glCreateShader(GL_VERTEX_SHADER)
    fragment = glCreateShader(GL_FRAGMENT_SHADER)

    glShaderSource(vertex, vertex_code)
    glShaderSource(fragment, fragment_code)

    compileShader(vertex, GL_VERTEX_SHADER)
    compileShader(fragment, GL_FRAGMENT_SHADER)

    glAttachShader(program, vertex)
    glAttachShader(program, fragment)

    glLinkProgram(program)
    if not glGetProgramiv(program, GL_LINK_STATUS):
        error = glGetProgramInfoLog(program).decode()
        print("link error:\n{0}".format(error))
        raise RuntimeError("Link error")

    glDetachShader(program, vertex)
    glDetachShader(program, fragment)

    glUseProgram(program)
    return program


def readPixels(x, y, w, h, clrspace=GL_RGBA):
    im = glReadPixels(x, y, w, h, clrspace, GL_FLOAT)
    im = np.frombuffer(im, np.float32)
    im.shape = h, w, 3
    im = im[::-1, :]
    return im
