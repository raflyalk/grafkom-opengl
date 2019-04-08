import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *


verticies = (
    (-0.9, -0.9, 1,1),
    (-0.6, -1, 1,1),
    (-0.6, -0.8, 1,1),
    (-0.3, -0.8, 1,1),
    (-0.3, -1, 1,1),
    (0.3, -1, 1,1),
    (0.3, -0.8, 1,1),
    (0.6, -0.8, 1,1),
    (0.6, -1, 1,1),
    (1, -1, 1,1),
    (1, 1, 1,1),
    (0.1, 1, 1,1),
    (-0.3, 0, 1,1),
    (-1, -0.5, 1,1),

    (-0.9, -0.9, -1,1),
    (-0.6, -1, -1,1),
    (-0.6, -0.8, -1,1),
    (-0.3, -0.8, -1,1),
    (-0.3, -1, -1,1),
    (0.3, -1, -1,1),
    (0.3, -0.8, -1,1),
    (0.6, -0.8, -1,1),
    (0.6, -1, -1,1),
    (1, -1, -1,1),
    (1, 1, -1,1),
    (0.1, 1, -1,1),
    (-0.3, 0, -1,1),
    (-1, -0.5, -1,1),

    (-0.6, -0.5, 1,1),
    (-0.3, -0.5, 1,1),
    (0.3, -0.5, 1,1),
    (0.6, -0.5, 1,1),
    (1, -0.5, 1,1),
    (1, 0, 1,1),

    (-0.6, -0.5, -1,1),
    (-0.3, -0.5, -1,1),
    (0.3, -0.5, -1,1),
    (0.6, -0.5, -1,1),
    (1, -0.5, -1,1),
    (1, 0, -1,1),
    )

samping = (
    (13,0,1,28),
    (28,2,3,29),
    (29,4,5,30),
    (30,6,7,31),
    (31,8,9,32),
    (13,32,33,12),
    (12,33,10,11),
)

samping2 = (
    (27,14,15,34),
    (34,16,17,35),
    (35,18,19,36),
    (36,20,21,37),
    (37,22,23,38),
    (27,38,39,26),
    (26,39,24,25),
)


colors = (
    (1,1,1),
    (0,0,0),
    (0.7,0.5,1)
    )

surfaces = (
    (13,0,14,27),
    (12,13,27,26),
    (11,12,26,25),
    (10,11,25,24),
    (9,10,24,23),
)

def Car():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glShadeModel(GL_SMOOTH)
    glBegin(GL_QUADS)

    x = 0

    glColor3fv(colors[2]);
    for surface in surfaces:
        for vertex in surface:
            glVertex4fv(verticies[vertex])

    glColor3fv(colors[0])
    for surface in samping:
        x+=1
        for vertex in surface:
            glVertex4fv(verticies[vertex])

    glColor3fv(colors[0])
    for surface in samping2:
        x+=1
        for vertex in surface:
            glVertex4fv(verticies[vertex])

    glEnd()


def main():
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0.0,0.0, -5)

    glRotatef(0,0,0,0)
    glEnable(GL_DEPTH_TEST)
    glDepthMask(GL_TRUE)
    glDepthFunc(GL_LEQUAL)


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    glRotatef(2, 0, -1, 0)
                if event.key == pygame.K_RIGHT:
                    glRotatef(2, 0 , 1, 0)
                if event.key == pygame.K_UP:
                    glRotatef(2, 1, 0, 0)
                if event.key == pygame.K_DOWN:
                    glRotatef(2, -1, 0, 0)
        #glRotatef(1,1,3,1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        pygame.time.wait(10)

        glDepthRange(0.0, 1.0)

        Car()
        pygame.display.flip()

        pygame.time.wait(10)


main()
