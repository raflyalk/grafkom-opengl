import glfw
from OpenGL.GL import *
import ShaderLoader
import numpy
import pyrr
from PIL import Image
from ObjLoader import *
import random

class Particle:
    def __init__(self, x=None, y=10.0, z=None, vel=0):
        self.alive = True
        self.life = 10.0
        self.fade = random.uniform(0, 100)/1000 + 0.003

        if x == None:
            x = random.uniform(-10, 11)
        if z == None:
            z = random.uniform(-10, 11)

        self.xpos = x
        self.ypos = y
        self.zpos = z

        self.red = 1.0
        self.green = 1.0
        self.blue = 1.0

        self.vel = vel
        self.gravity = -0.8

MAX_RAIN_PARTICLES = 500
par_sys = [Particle()] * MAX_RAIN_PARTICLES
slowdown = 2.0

MAX_SMOKE_PARTICLES = 2000
smoke_par = [Particle(-0.40611, -0.145301, -1.409140, 10)] * MAX_SMOKE_PARTICLES
slowdown_smoke = 2.0

def initSmokeParticles(i):
    smoke_par[i] = Particle(-0.40611, -0.145301, -1.409140, 10)

def initParticles(i):
    par_sys[i] = Particle()

def drawSmoke():
    loop = 0

    while loop < MAX_SMOKE_PARTICLES:
        if (smoke_par[loop].alive == True):
            x = smoke_par[loop].xpos
            y = smoke_par[loop].ypos
            z = smoke_par[loop].zpos

            # Draw smoke particles
            glBegin(GL_QUADS)
            
            glVertex3f(x, y, z)
            glVertex3f(x-0.01, y, z)
            glVertex3f(x-0.01, y-0.01, z)
            glVertex3f(x, y-0.01, z)

            glVertex3f(x, y, z-0.01)
            glVertex3f(x-0.01, y, z-0.01)
            glVertex3f(x-0.01, y-0.01, z-0.01)
            glVertex3f(x, y-0.01, z-0.01)
            
            glVertex3f(x, y, z)
            glVertex3f(x, y, z-0.01)
            glVertex3f(x, y-0.01, z-0.01)
            glVertex3f(x, y-0.01, z)
            
            glVertex3f(x-0.01, y, z)
            glVertex3f(x-0.01, y, z-0.01)
            glVertex3f(x-0.01, y-0.01, z-0.01)
            glVertex3f(x-0.01, y-0.01, z)
            
            glVertex3f(x, y, z)
            glVertex3f(x-0.01, y, z)
            glVertex3f(x-0.01, y, z-0.01)
            glVertex3f(x, y, z-0.01)

            glVertex3f(x, y-0.01, z)
            glVertex3f(x-0.01, y-0.01, z)
            glVertex3f(x-0.01, y-0.01, z-0.01)
            glVertex3f(x, y-0.01, z-0.01)

            glEnd()

            # Move
            # Adjust slowdown for speed
            smoke_par[loop].zpos -= smoke_par[loop].vel / (slowdown*1000)
            smoke_par[loop].vel -= smoke_par[loop].vel / 1000

            smoke_par[loop].xpos += random.uniform(-100, 100) / (slowdown*5000)
            
            smoke_par[loop].ypos += random.uniform(-100, 100) / (slowdown*6000)
            
            # Decay
            smoke_par[loop].life = smoke_par[loop].life - smoke_par[loop].fade

            if smoke_par[loop].zpos <= -10:
                smoke_par[loop].life = -1.0
            
            # Revive
            if smoke_par[loop].life < 0.0:
                initSmokeParticles(loop)

        loop = loop + 2

def drawRain():
    loop = 0

    while loop < MAX_RAIN_PARTICLES:
        if (par_sys[loop].alive == True):
            x = par_sys[loop].xpos
            y = par_sys[loop].ypos
            z = par_sys[loop].zpos

            # Draw particles
            glColor3f(1.0, 1.0, 1.0)
            glLineWidth(2.0)
            glBegin(GL_LINES)
            glVertex3f(x, y, z)
            glVertex3f(x, y+0.5, z)
            glEnd()

            # Move
            # Adjust slowdown for speed
            par_sys[loop].ypos = par_sys[loop].ypos + par_sys[loop].vel / (slowdown*1000)
            par_sys[loop].vel = par_sys[loop].vel + par_sys[loop].gravity

            # Decay
            par_sys[loop].life = par_sys[loop].life - par_sys[loop].fade

            if par_sys[loop].ypos <= -10:
                par_sys[loop].life = -1.0
            
            # Revive
            if par_sys[loop].life < 0.0:
                initParticles(loop)

        loop = loop + 2


def window_resize(window, width, height):
    glViewport(0, 0, width, height)

def main():

    # initialize glfw
    if not glfw.init():
        return

    w_width, w_height = 800, 600

    #glfw.window_hint(glfw.RESIZABLE, GL_FALSE)

    window = glfw.create_window(w_width, w_height, "My OpenGL window", None, None)

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_window_size_callback(window, window_resize)

    obj = ObjLoader()
    obj.load_model("res/car_small.obj")

    texture_offset = len(obj.vertex_index)*12
    normal_offset = (texture_offset + len(obj.texture_index)*8)

    shader = ShaderLoader.compile_shader("shaders/vert_shader.vs", "shaders/frag_shader.fs")

    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, obj.model.itemsize * len(obj.model), obj.model, GL_STATIC_DRAW)

    #positions
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, obj.model.itemsize * 3, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    #textures
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, obj.model.itemsize * 2, ctypes.c_void_p(texture_offset))
    glEnableVertexAttribArray(1)
    #normals
    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, obj.model.itemsize * 3, ctypes.c_void_p(normal_offset))
    glEnableVertexAttribArray(2)

    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    # Set the texture wrapping parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    # Set texture filtering parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    # load image
    image = Image.open("res/water.jpeg")
    flipped_image = image.transpose(Image.FLIP_TOP_BOTTOM)
    img_data = numpy.array(list(flipped_image.getdata()), numpy.uint8)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
    glEnable(GL_TEXTURE_2D)

    glUseProgram(shader)

    glClearColor(0.2, 0.3, 0.2, 1.0)
    glEnable(GL_DEPTH_TEST)
    #glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    view = pyrr.matrix44.create_from_translation(pyrr.Vector3([0.0, 0.0, -3.0]))
    projection = pyrr.matrix44.create_perspective_projection_matrix(65.0, w_width / w_height, 0.1, 100.0)
    model = pyrr.matrix44.create_from_translation(pyrr.Vector3([0.0, 0.0, 0.0]))

    view_loc = glGetUniformLocation(shader, "view")
    proj_loc = glGetUniformLocation(shader, "projection")
    model_loc = glGetUniformLocation(shader, "model")
    transform_loc = glGetUniformLocation(shader, "transform")
    light_loc = glGetUniformLocation(shader, "light")

    glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)
    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)

    counter_x = 0
    counter_y = 0

    while not glfw.window_should_close(window):
        glfw.poll_events()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        rot_x = pyrr.Matrix44.from_x_rotation(0.9 * counter_x )
        rot_y = pyrr.Matrix44.from_y_rotation(0.9 * counter_y )
        if (glfw.get_key(window,glfw.KEY_UP) == glfw.PRESS):
            counter_x-=0.01
        if (glfw.get_key(window,glfw.KEY_DOWN) == glfw.PRESS):
            counter_x+=0.01
        if (glfw.get_key(window,glfw.KEY_RIGHT) == glfw.PRESS):
            counter_y+=0.01
        if (glfw.get_key(window,glfw.KEY_LEFT) == glfw.PRESS):
            counter_y-=0.01
        glUniformMatrix4fv(transform_loc, 1, GL_FALSE, rot_x * rot_y)
        glUniformMatrix4fv(light_loc, 1, GL_FALSE, rot_x * rot_y)

        glDrawArrays(GL_TRIANGLES, 0, len(obj.vertex_index))

        drawRain()
        drawSmoke()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()