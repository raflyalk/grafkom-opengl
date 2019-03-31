

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy
import json
import os
import sys

def main():
    # Check arguments
    if (len(sys.argv) != 2):
        print('Please add the name of the json file as an argument.')
        print('Example: python main.py unicorn')
        return
    file_name = sys.argv[1]

    # Initialize glfw
    if not glfw.init():
        return

    window = glfw.create_window(800, 600, "My OpenGL Window", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    # import json file containing vertices & elements
    json_file = open(os.path.join(os.path.dirname(__file__), 'res', file_name + '.json'))
    data = json.load(json_file)

    # Create a Vertex Buffer Object and copy the vertex data to it
    vbo = glGenBuffers(1)
    vertices = numpy.array(data['vertices'], dtype=numpy.float32)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, len(vertices) * 4, vertices, GL_STATIC_DRAW)

    # Create an element array
    ebo = glGenBuffers(1)
    elements = numpy.array(data['elements'], dtype=numpy.uint32)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(elements) * 4, elements, GL_STATIC_DRAW)

    # Create vertex shader
    vertex_shader = """
        #version 150 core
        in vec2 position;
        in vec3 color;
        out vec3 Color;
        void main()
        {
            Color = color;
            gl_Position = vec4(position, 0.0, 1.0);
        }
    """

    # Create fragment shader
    fragment_shader = """
        #version 150 core
        in vec3 Color;
        out vec4 outColor;
        void main()
        {
            outColor = vec4(Color, 1.0);
        }
    """

    # Compile vertex and fragment shader
    shader = OpenGL.GL.shaders.compileProgram(OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
                                              OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))

    # Specify the layout of the vertex data
    position = glGetAttribLocation(shader, "position")
    glVertexAttribPointer(position, 2, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(0))
    glEnableVertexAttribArray(position)

    color = glGetAttribLocation(shader, "color")
    glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(8))
    glEnableVertexAttribArray(color)

    glUseProgram(shader)

    glClearColor(0.2, 0.3, 0.2, 0.1)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        glClear(GL_COLOR_BUFFER_BIT)

        glDrawElements(GL_TRIANGLES, len(elements), GL_UNSIGNED_INT, None)

        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == '__main__':
    main()
