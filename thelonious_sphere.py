import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from math import sin, cos, pi
from PIL import Image
import time

def unit_sphere(lat_steps=40, long_steps=40):
    vertices = []
    for i in range(lat_steps):
        phi1 = pi * i / lat_steps
        phi2 = pi * (i + 1) / lat_steps

        for j in range(long_steps):
            theta1 = 2 * pi * j / long_steps
            theta2 = 2 * pi * (j + 1) / long_steps

            p = []
            for phi, theta in [
                    (phi1, theta1),
                    (phi2, theta1),
                    (phi2, theta2),
                    (phi1, theta2),
            ]:
                x = sin(phi) * cos(theta)
                y = cos(phi)
                z = sin(phi) * sin(theta)
                u = theta / (2 * pi)
                v = phi/pi
                p.append((x, y, z, u, v))
            vertices.extend([p[0], p[1], p[2], p[0], p[2], p[3]])
    return vertices
        

def load_texture(path):
    img = Image.open(path)
    img_data = img.convert("RGB").tobytes()

    tex = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.width, img.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    return tex
            
glfw.init()
win = glfw.create_window(800, 600, "Thelonious Sphere", None, None)
glfw.make_context_current(win)

glViewport(0, 0, 800, 600)
glClearColor(0.0, 0.0, 0.0, 1.0)

glEnable(GL_DEPTH_TEST)
glEnable(GL_TEXTURE_2D)

glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(45.0, 800/600, 0.1, 100.0)

glMatrixMode(GL_MODELVIEW)

sphere = unit_sphere()
texture = load_texture("thelonious-rectangle.jpg")

start = time.time()

while not glfw.window_should_close(win):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0, 0, -3)

    curr_time = time.time() - start
    angle = curr_time * 300

    glRotatef(angle, 0, 1, 0)
    glTranslatef(0, 0, -3*sin(curr_time))

    glBindTexture(GL_TEXTURE_2D, texture)
    glBegin(GL_TRIANGLES)
    for x, y, z, u, v in sphere:
        glTexCoord2f(u, v)
        glVertex3f(x, y, z)
    glEnd()

    glfw.swap_buffers(win)
    glfw.poll_events()

glfw.terminate()
