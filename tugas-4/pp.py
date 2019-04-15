import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *


def main():
    pygame.display.set_mode((1024,768), DOUBLEBUF|OPENGL)

    #GL Setup
    glShadeModel(GL_SMOOTH)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glClearDepth(1.0)

    #Viewport Setup
    glViewport(0, 0, 1024, 768)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, 1024.0/768, 0.1, 100)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    #sphere setup
    q = gluNewQuadric()
    glFrontFace(GL_CCW)
    gluQuadricTexture(q, GL_TRUE)
    gluQuadricNormals(q, GLU_FLAT)
    gluQuadricOrientation(q, GLU_OUTSIDE)

    #lighting setup
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT1)
    glLightfv(GL_LIGHT1, GL_POSITION, (0.0, 0.0, 0.0, 1.0)) 
    glLightfv(GL_LIGHT1, GL_AMBIENT, (0.0, 0.0, 0.0, 1.0))
    glLightfv(GL_LIGHT1, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))
    glLightfv(GL_LIGHT1, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))
    glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, (0.0, 0.0, 0.0, 1.0))
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glLightfv(GL_LIGHT1, GL_POSITION, (0.0, 0.0, 0.0))

    while True:
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0.0, -1.0, -5.0)
        gluSphere(q, 1.0, 32, 32)

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type in (QUIT, KEYDOWN):
                return

if __name__ == "__main__":
    main()
