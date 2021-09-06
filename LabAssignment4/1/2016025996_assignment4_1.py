import numpy as np
import glfw
from OpenGL.GL import *

actionStateList = [];
def transformation():
     global actionStateList
     for i in actionStateList:
         if(i == 1):
             glTranslate(-0.1, 0, 0)
         elif(i == 2):
             glTranslate(0.1, 0, 0)
         elif(i == 3):
             glRotate(10, 0, 0, 1)
         elif(i == 4):
             glRotate(-10, 0, 0, 1)


def key_callback(window, key, scancode, action, mods):
    global actionState
    if key==glfw.KEY_Q:
        if action == glfw.PRESS or action==glfw.REPEAT:
            # actionStateList.append(1)
            actionStateList.insert(0, 1)
    elif key==glfw.KEY_E:
        if action==glfw.PRESS or action==glfw.REPEAT:
            # actionStateList.append(2)
            actionStateList.insert(0, 2)
    elif key==glfw.KEY_A:
        if action==glfw.PRESS or action==glfw.REPEAT:
            # actionStateList.append(3)
            actionStateList.insert(0, 3)
    elif key==glfw.KEY_D:
        if action==glfw.PRESS or action==glfw.REPEAT:
            # actionStateList.append(4)
            actionStateList.insert(0, 4)
    elif key==glfw.KEY_1:
        if action==glfw.PRESS or action==glfw.REPEAT:
            actionStateList.clear()

def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    # draw cooridnates
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([1.,0.]))
    glColor3ub(0, 255, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([0.,1.]))
    glEnd()
    glColor3ub(255, 255, 255)
    transformation()
    drawTriangle()

def drawTriangle():
    glBegin(GL_TRIANGLES)
    glVertex2fv(np.array([0.,.5]))
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([.5,0.]))
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
    glfw.swap_interval(1)

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
