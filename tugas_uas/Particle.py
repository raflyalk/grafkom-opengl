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
