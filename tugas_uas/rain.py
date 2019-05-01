import sys, pygame, math
import timeit
from pygame.locals import *
from pygame.constants import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random

class Particle():
    def __init__(self, startx, starty, startz, col):
        self.x = startx
        self.y = starty
        self.z = startz
        self.col = col
        self.sx = startx
        self.sy = starty
        self.sz = startz

    def move(self):
        if self.y > 1:
            self.x=self.sx
            self.y=self.sy
            self.z=self.sz

        else:
            self.y+=random.uniform(0.02, 0.07)

        self.x+=random.uniform(0.01, 0.05)

def main():
    color = (255,255,255,255)
    pygame.init()
    viewport = (800,600)
    hx = viewport[0]/2
    hy = viewport[1]/2
    srf = pygame.display.set_mode(viewport, OPENGL | DOUBLEBUF)

    glLightfv(GL_LIGHT0, GL_POSITION,  (-40, 0, 0, 0.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (float(color[0]) / 256, float(color[1]) / 256, float(color[2]) / 256, 1.0))
    glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION,  (40, 0, 0, 0.0))
    glLightfv(GL_LIGHT0, GL_SPOT_CUTOFF,  10)

    glEnable(GL_LIGHT0)

    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)
    glEnableClientState (GL_VERTEX_ARRAY)
    glShadeModel(GL_SMOOTH)           # most obj files expect to be smooth-shaded
    clock = pygame.time.Clock()

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    width, height = viewport
    gluPerspective(90.0, width/float(height), 1, 100.0)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_MODELVIEW)

    raindrop = []
    raining = -1
    rainspeed = float(color[3]) / 2550
    while raining < 1 :
        raindrop.append([raining, random.uniform(-1,1)])
        raining += 0.03
        
    while 1:
        start = timeit.default_timer()
        clock.tick(30)
        
        for hujan in range(len(raindrop)):
            glBegin(GL_QUADS)
            glColor3f(255,255,255)
            glVertex3f(raindrop[hujan][0] + 0.005  ,raindrop[hujan][1] + 0.05,-1)
            glVertex3f(raindrop[hujan][0] + 0.005  ,raindrop[hujan][1],-1)
            glVertex3f(raindrop[hujan][0]         ,raindrop[hujan][1],  -1)
            glVertex3f(raindrop[hujan][0]         ,raindrop[hujan][1] + 0.05,-1)
            glEnd()
            raindrop[hujan][1] -= rainspeed
            if raindrop[hujan][1] < -1:
                raindrop[hujan][1] = 1
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        pygame.display.flip()
        print(round(1/(-start+timeit.default_timer())))
        
if __name__ == '__main__':
    main()
