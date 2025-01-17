import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy
import pyrr


def main():

    # initialize glfw
    if not glfw.init():
        return

    window = glfw.create_window(800, 800, "My OpenGL window", None, None)

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    #        positions        colors
    cube = [-0.5, -0.5,  0.5, 1.0, 0.0, 0.0,
             0.5, -0.5,  0.5, 0.0, 1.0, 0.0,
             0.5,  0.5,  0.5, 0.0, 0.0, 1.0,
            -0.5,  0.5,  0.5, 1.0, 1.0, 1.0,

            -0.5, -0.5, -0.5, 1.0, 0.0, 0.0,
             0.5, -0.5, -0.5, 0.0, 1.0, 0.0,
             0.5,  0.5, -0.5, 0.0, 0.0, 1.0,
            -0.5,  0.5, -0.5, 1.0, 1.0, 1.0,

            0.5, 0, 0.5, 0.0, 1.0, 0.0,
            0.5, 0, -0.5, 0.0, 1.0, 0.0,
            0.5, -0.5, 0.5, 0.0, 1.0, 0.0,
            0.5, -0.5, -0.5, 0.0, 1.0, 0.0,

            0.8, -0.1, 0.5, 0.0, 1.0, 0.0,
            0.8, -0.1, -0.5, 0.0, 1.0, 0.0,
            0.8, -0.5, 0.5, 0.0, 1.0, 0.0,
            0.8, -0.5, -0.5, 0.0, 1.0, 0.0,
        ]

    
    cube = numpy.array(cube, dtype = numpy.float32)

    indices = [
        0, 1, 2, 3,
        4, 5, 6, 7,
        4, 5, 1, 0,
        6, 7, 3, 2,
        7, 4, 0, 3,
        6, 2, 8, 9,
        8, 10, 14, 12,
        9, 11, 15, 13,
        8, 9, 13, 12,
        12, 13, 15, 14,
        10, 11, 15, 14
    ]

    indices = numpy.array(indices, dtype= numpy.uint32)

    vertex_shader = """
    #version 320 es
    precision mediump float;
    in vec3 position;
    in vec3 color;
    uniform mat4 transform;
    out vec3 newColor;
    void main()
    {
        gl_Position = transform * vec4(position, 1.0f);
        newColor = color;
    }
    """

    fragment_shader = """
    #version 320 es
    precision mediump float;
    in vec3 newColor;
    out vec4 outColor;
    void main()
    {
        outColor = vec4(newColor, 1.0f);
    }
    """
    shader = OpenGL.GL.shaders.compileProgram(OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
                                              OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))

    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, len(cube)*4, cube, GL_STATIC_DRAW)

    EBO = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indices)*4, indices, GL_STATIC_DRAW)

    position = glGetAttribLocation(shader, "position")
    glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
    glEnableVertexAttribArray(position)

    color = glGetAttribLocation(shader, "color")
    glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
    glEnableVertexAttribArray(color)


    glUseProgram(shader)

    glClearColor(0.2, 0.3, 0.2, 1.0)
    glEnable(GL_DEPTH_TEST)
    # glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    counter_x = 0
    counter_y = 0
    while not glfw.window_should_close(window):
        glfw.poll_events()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        rot_x = pyrr.Matrix44.from_x_rotation(0.5 * counter_x )
        rot_y = pyrr.Matrix44.from_y_rotation(0.5 * counter_y )
        if (glfw.get_key(window,glfw.KEY_UP) == glfw.PRESS):
            counter_x-=0.01
        if (glfw.get_key(window,glfw.KEY_DOWN) == glfw.PRESS):
            counter_x+=0.01
        if (glfw.get_key(window,glfw.KEY_RIGHT) == glfw.PRESS):
            counter_y+=0.01
        if (glfw.get_key(window,glfw.KEY_LEFT) == glfw.PRESS):
            counter_y-=0.01
        transformLoc = glGetUniformLocation(shader, "transform")
        glUniformMatrix4fv(transformLoc, 1, GL_FALSE, rot_x * rot_y)

        glDrawElements(GL_QUADS, len(indices), GL_UNSIGNED_INT, None)

        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    main()
