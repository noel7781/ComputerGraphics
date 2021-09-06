import numpy as np
import glfw
from OpenGL.GL import *

draw_value = 4
draw_dict = {1:GL_POINTS, 2:GL_LINES, 3:GL_LINE_STRIP, 4:GL_LINE_LOOP, 5:GL_TRIANGLES, 6:GL_TRIANGLE_STRIP,
        7:GL_TRIANGLE_FAN, 8:GL_QUADS, 9:GL_QUAD_STRIP, 0:GL_POLYGON}
def key_callback(window, key, scancode, action, mods):
    global draw_value
    if key==glfw.KEY_1 and action == glfw.PRESS:
        draw_value = 1
    elif key==glfw.KEY_2 and action==glfw.PRESS:
        draw_value = 2
    elif key==glfw.KEY_3 and action==glfw.PRESS:
        draw_value = 3
    elif key==glfw.KEY_4 and action==glfw.PRESS:
        draw_value = 4
    elif key==glfw.KEY_5 and action==glfw.PRESS:
        draw_value = 5
    elif key==glfw.KEY_6 and action==glfw.PRESS:
        draw_value = 6
    elif key==glfw.KEY_7 and action==glfw.PRESS:
        draw_value = 7
    elif key==glfw.KEY_8 and action==glfw.PRESS:
        draw_value = 8
    elif key==glfw.KEY_9 and action==glfw.PRESS:
        draw_value = 9
    elif key==glfw.KEY_0 and action==glfw.PRESS:
        draw_value = 0
def render():
    global draw_value
    global draw_dict
    degree = np.linspace(0, 360, 13)
    d2r = [np.deg2rad(i) for i in degree]
    d2r = d2r[:12]
    vertex = [(np.cos(i), np.sin(i)) for i in d2r]
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glBegin(draw_dict[draw_value])
    for i in vertex:
        glVertex2fv(i)
    glEnd()

def main():
    # Initialize the library
    if not glfw.init():
        return
    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(480, 480, "2016025996", None, None)
    if not window:
        glfw.terminate()
        return

    # Make the window's context current
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        # Poll events
        glfw.poll_events()

        # Render here, e.g. using pyOpenGL
        render()

        # Swap front and back buffers
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
