import numpy as np
import glfw
from OpenGL.GL import *

def render(M):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    # draw cooridnate
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([1.,0.]))
    glColor3ub(0, 255, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([0.,1.]))
    glEnd()
    glColor3ub(255, 255, 255)
    # draw point p
    glBegin(GL_POINTS)
    # your implementation
    glVertex2fv((M@np.array([1., 0.,1.]))[:-1])
    glEnd()
    # draw vector v
    glBegin(GL_LINES)
    # your implementation
    glVertex2fv((M@np.array([0. , 0., 0.]))[:-1])
    glVertex2fv((M@np.array([0.5, 0., 0.]))[:-1])
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
    glfw.swap_interval(1)

    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        # Poll events
        glfw.poll_events()

        # Render here, e.g. using pyOpenGL
        th = glfw.get_time()
        T = np.array(([[np.cos(th), -np.sin(th),0],[np.sin(th), np.cos(th), 0],[0, 0, 1]]))
        render(T)
        # Swap front and back buffers
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
