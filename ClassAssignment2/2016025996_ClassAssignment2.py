import numpy as np
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

WindowXSize = 640
WindowYSize = 640
LeftButtonPressed = False # Check if Mouse Left Button clicked
RightButtonPressed = False # Check if Mouse Right Button clicked
ZoomStats = 0 # If Mouse Scroll ups, then zoom-up, if down then zoom-down
lxpos = 320
rxpos = 320
lypos = 320
rypos = 320
ldx = 0
ldy = 0
rdx = 0
rdy = 0
cur = np.array([0.,0.,5.])
target = np.array([0.,0.,0.])
toggleWireToSolid = 0
toggleShading = 0
vertexList = None
normalList = None
faceList = None


def render(window):
    global ldx, ldy, rdx, rdy, ZoomStats, cur, target
    if toggleWireToSolid == 0:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    else :
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    get_mouse_coord(window)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1, 1, 10)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    u, v, w = myLookAt(cur, target, np.array([0,1,0]))
    
    if rdx != 0 or rdy != 0:
        cur += np.array([u[0]*rdx + v[0]*rdy, (u[1]*rdx + v[1]*rdy), u[2]*rdx + v[2]*rdy])
        target += np.array([u[0]*rdx + v[0]*rdy, (u[1]*rdx + v[1]*rdy), u[2]*rdx + v[2]*rdy])
    rdx = 0
    rdy = 0
        
    u, v, w = myLookAt(cur, target, np.array([0,1,0]))
    if ldx != 0 or ldy != 0:
        cur = target + rotateXZ(ldx * 5) @ (cur-target)
        cur = target + rotateY(ldy * 10) @ (cur-target)
    ldx = 0
    ldy = 0
    gluLookAt(*cur, *target,0,1,0)
    w_direction = w * ZoomStats * 0.1
    glTranslatef(w_direction[0],w_direction[1],w_direction[2])

    drawGrid()
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glEnable(GL_LIGHT2)
    glEnable(GL_NORMALIZE)
    glPushMatrix()
    lightPos = (3.,4.,5.,0.)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
    glPopMatrix()
    lightColor = (1.,0.,0.,1.)
    ambientLightColor = (.1,.1,.1,1.)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT0, GL_SPECULAR, lightColor)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor)
    glPushMatrix()
    lightPos = (4.,5.,3.,0.)
    glLightfv(GL_LIGHT1, GL_POSITION, lightPos)
    glPopMatrix()
    lightColor = (0.,1.,0.,1.)
    ambientLightColor = (.1,.1,.1,1.)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT1, GL_SPECULAR, lightColor)
    glLightfv(GL_LIGHT1, GL_AMBIENT, ambientLightColor)
    glPushMatrix()
    lightPos = (0.,10.,0.,1.)
    glLightfv(GL_LIGHT2, GL_POSITION, lightPos)
    glPopMatrix()
    lightColor = (0.,0.,1.,1.)
    ambientLightColor = (.1,.1,.1,1.)
    glLightfv(GL_LIGHT2, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT2, GL_SPECULAR, lightColor)
    glLightfv(GL_LIGHT2, GL_AMBIENT, ambientLightColor)
    objectColor = (1.,1.,1.,1.)
    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT,GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)
    glPushMatrix()
    #glScalef(.01,.005,.01)
    if faceList != None:
        draw_glDrawElement()
    glPopMatrix()
    glDisable(GL_LIGHTING)

def drawGrid():
    ## Draw Grid
    glBegin(GL_LINES)
    # Z Line
    glVertex3fv([-5,0,5])
    glVertex3fv([-5,0,-5])
    glVertex3fv([-4,0,5])
    glVertex3fv([-4,0,-5])
    glVertex3fv([-3,0,5])
    glVertex3fv([-3,0,-5])
    glVertex3fv([-2,0,5])
    glVertex3fv([-2,0,-5])
    glVertex3fv([-1,0,5])
    glVertex3fv([-1,0,-5])
    glVertex3fv([0,0,5])
    glVertex3fv([0,0,-5])
    glVertex3fv([1,0,5])
    glVertex3fv([1,0,-5])
    glVertex3fv([2,0,5])
    glVertex3fv([2,0,-5])
    glVertex3fv([3,0,5])
    glVertex3fv([3,0,-5])
    glVertex3fv([4,0,5])
    glVertex3fv([4,0,-5])
    glVertex3fv([5,0,5])
    glVertex3fv([5,0,-5])
    # X Line
    glVertex3fv([-5,0,5])
    glVertex3fv([5,0,5])
    glVertex3fv([-5,0,4])
    glVertex3fv([5,0,4])
    glVertex3fv([-5,0,3])
    glVertex3fv([5,0,3])
    glVertex3fv([-5,0,2])
    glVertex3fv([5,0,2])
    glVertex3fv([-5,0,1])
    glVertex3fv([5,0,1])
    glVertex3fv([-5,0,0])
    glVertex3fv([5,0,0])
    glVertex3fv([-5,0,-1])
    glVertex3fv([5,0,-1])
    glVertex3fv([-5,0,-2])
    glVertex3fv([5,0,-2])
    glVertex3fv([-5,0,-3])
    glVertex3fv([5,0,-3])
    glVertex3fv([-5,0,-4])
    glVertex3fv([5,0,-4])
    glVertex3fv([-5,0,-5])
    glVertex3fv([5,0,-5])
    glEnd()

def drawRobot():
    t= glfw.get_time()
    ## Draw start
    ## Draw Body
    glPushMatrix()
    glTranslatef(0,0.4,0)
    glPushMatrix()
    glScalef(0.4, 0.4, 0.4)
    drawCube()
    glPopMatrix()
    ## Draw Head
    glPushMatrix()
    glTranslatef(0,0.4,0)
    glRotatef(moveArm(100*t),1,0,0)
    glPushMatrix()
    glTranslatef(0,0.4,0)
    glScalef(0.4,0.4,0.4)
    drawSphere()
    glPopMatrix()
    glPopMatrix()
    ## Draw Left Arm
    glPushMatrix()
    glTranslatef(0.5,0.2,0.0)
    glRotatef(moveArm(10*t) , 1,0,0)
    glPushMatrix()
    glTranslatef(0,0,0.8)
    glPushMatrix()
    glScalef(0.1,0.1,0.6)
    drawCube()
    glPopMatrix()
    glPushMatrix()
    glTranslatef(0,0,0.6)
    glRotatef(moveArm(100*t),1,0,0)
    glPushMatrix()
    glTranslatef(0,0,0.1)
    glScalef(.1,.1,.1)
    drawSphere()
    glPopMatrix()
    glPopMatrix()
    glPopMatrix()
    glPopMatrix()
    ## Draw Right Arm
    glPushMatrix()
    glTranslatef(-0.5,0.2,0)
    glRotatef(moveArm(10*t + 6) , 1,0,0)
    glPushMatrix()
    glTranslatef(0, 0, 0.8)
    glPushMatrix()
    glScalef(0.1, 0.1, 0.6)
    drawCube()
    glPopMatrix()
    glPushMatrix()
    glTranslatef(0, 0, 0.6)
    glRotatef(moveArm(100*t + 6),1,0,0)
    glPushMatrix()
    glTranslatef(0,0,0.1)
    glScalef(.1, .1, .1)
    drawSphere()
    glPopMatrix()
    glPopMatrix()
    glPopMatrix()
    glPopMatrix()
    #
    glPushMatrix()
    #draw left
    glTranslate(0.3,-0.1,0)
    glPushMatrix()
    glRotatef(moveLeg(10*t),1,0,0)
    glPushMatrix()
    glTranslatef(0, -0.6, 0)
    glPushMatrix()
    glScalef(0.2,0.3,0.1)
    drawCube()
    glPopMatrix()
    glPushMatrix()
    glTranslatef(0,-0.6,0)
    glRotate(moveLeg(20*t),1,0,0)
    glPushMatrix()
    glScalef(0.2,0.3,0.1)
    drawCube()
    glPopMatrix()
    glTranslate(0,-0.3,0)
    glPushMatrix()
    glRotate(moveLeg(30*t),1,0,0)
    glPushMatrix()
    glTranslatef(0,0,0.2)
    glScalef(0.1,0.1,0.3)
    drawCube()
    glPopMatrix()
    glPopMatrix()
    glPopMatrix()
    glPopMatrix()
    glPopMatrix()
    glPopMatrix()
    #draw right
    glPushMatrix()
    glTranslate(-0.3,-0.1,0)
    glRotatef(moveLeg(10*t+6),1,0,0)
    glPushMatrix()
    glTranslatef(0, -0.6, 0)
    glPushMatrix()
    glScalef(0.2,0.3,0.1)
    drawCube()
    glPopMatrix()
    glPushMatrix()
    glTranslatef(0,-0.6,0)
    glRotate(moveLeg(20*t+6),1,0,0)
    glPushMatrix()
    glScalef(0.2,0.3,0.1)
    drawCube()
    glPopMatrix()
    glTranslate(0,-0.3,0)
    glPushMatrix()
    glRotate(moveLeg(30*t+6),1,0,0)
    glPushMatrix()
    glTranslatef(0,0,0.2)
    glScalef(0.1,0.1,0.3)
    drawCube()
    glPopMatrix()
    glPopMatrix()
    glPopMatrix()
    glPopMatrix()
    glPopMatrix()
    #
    glPopMatrix()

def moveArm(t):
    t %= 12
    if t < 3:
        t = t
    if t > 3 and t <= 9:
        t = -t + 6
    if t > 9:
        t = t - 12
    return 2*t

def moveLeg(t):
    t %= 12
    if t < 3:
        t = t
    if t > 3 and t <= 9:
        t = -t + 6
    if t > 9:
        t = t - 12
    return 2.5*t

def drawCube():
    glBegin(GL_QUADS)
    glVertex3f( 1.0, 1.0,-1.0)
    glVertex3f(-1.0, 1.0,-1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f( 1.0, 1.0, 1.0)
    glVertex3f( 1.0,-1.0, 1.0)
    glVertex3f(-1.0,-1.0, 1.0)
    glVertex3f(-1.0,-1.0,-1.0)
    glVertex3f( 1.0,-1.0,-1.0)
    glVertex3f( 1.0, 1.0,1.0)
    glVertex3f(-1.0, 1.0,1.0)
    glVertex3f(-1.0,-1.0,1.0)
    glVertex3f( 1.0,-1.0,1.0)
    glVertex3f( 1.0,-1.0,-1.0)
    glVertex3f(-1.0,-1.0,-1.0)
    glVertex3f(-1.0, 1.0,-1.0)
    glVertex3f( 1.0, 1.0,-1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(-1.0, 1.0,-1.0)
    glVertex3f(-1.0,-1.0,-1.0)
    glVertex3f(-1.0,-1.0, 1.0)
    glVertex3f(1.0, 1.0,-1.0)
    glVertex3f(1.0, 1.0, 1.0)
    glVertex3f(1.0,-1.0, 1.0)
    glVertex3f(1.0,-1.0,-1.0)
    glEnd()

# draw a sphere of radius 1, centered at the origin.
# numLats: number of latitude segments
# numLongs: number of longitude segments
def drawSphere(numLats=12, numLongs=12):
    for i in range(0, numLats + 1):
        lat0 = np.pi * (-0.5 + float(float(i - 1) /
        float(numLats)))
        z0 = np.sin(lat0)
        zr0 = np.cos(lat0)
        lat1 = np.pi * (-0.5 + float(float(i) / float(numLats)))
        z1 = np.sin(lat1)
        zr1 = np.cos(lat1)
        # Use Quad strips to draw the sphere
        glBegin(GL_QUAD_STRIP)
        for j in range(0, numLongs + 1):
            lng = 2 * np.pi * float(float(j - 1) / float(numLongs))
            x = np.cos(lng)
            y = np.sin(lng)
            glVertex3f(x * zr0, y * zr0, z0)
            glVertex3f(x * zr1, y * zr1, z1)
        glEnd()

def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([1.,0.,0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,1.,0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0.,0.,0]))
    glVertex3fv(np.array([0.,0.,1.]))
    glEnd()

def myLookAt(eye, at, up):
    w = eye - at
    w = w / np.sqrt(np.dot(w, w))
    u = np.cross(up, w)
    u = u / np.sqrt(np.dot(u, u))
    v = np.cross(w, u)
    return u,v,w

def rotateXZ(x):
    c = np.cos(x)
    s = np.sin(x)
    return np.array([[c,0,-s],[0,1,0],[s,0,c]])

def rotateY(rad):
    c = np.cos(rad)
    s = np.sin(rad)
    return np.array([[1,0,0],[0,c,-s],[0,s,c]])

def toUnit(x):
    return x / np.dot(x,x)

def deg(x,y):
    return np.arccos(np.dot(x,y) / (np.sqrt(np.dot(x,x)) * np.sqrt(np.dot(y,y)))) * 180 / np.pi

def cursor_callback(window, xpos, ypos):
    global ldx,ldy,rdx,rdy
    if xpos < 0 or xpos > WindowXSize or ypos < 0 or ypos > WindowYSize:
        rdx = 0
        rdy = 0

def button_callback(window, button, action, mod):
    global LeftButtonPressed, RightButtonPressed, lxpos, lypos, rxpos, rypos, ldx, ldy, rdx, rdy
    if button==glfw.MOUSE_BUTTON_LEFT:
        if action==glfw.PRESS:
            LeftButtonPressed = True
            (lxpos, lypos) = glfw.get_cursor_pos(window)
            lypos = -lypos + 640
        elif action==glfw.RELEASE:
            LeftButtonPressed = False
    if button==glfw.MOUSE_BUTTON_RIGHT:
        if action==glfw.PRESS:
            RightButtonPressed = True
            (rxpos, rypos) = glfw.get_cursor_pos(window)
            rypos = -rypos + 640
        elif action==glfw.RELEASE:
            RightButtonPressed = False
            #print("right button relase %d %d"%(rdx,rdy))
            rdx = 0
            rdy = 0
 
def scroll_callback(window, xoffset, yoffset):
    global ZoomStats
    ZoomStats += yoffset

def key_callback(window, key, scancode, action, mods):
    global toggleWireToSolid, toggleShading
    if action==glfw.PRESS or action == glfw.REPEAT:
        if key==glfw.KEY_Z:
            toggleWireToSolid ^= 1
        if key==glfw.KEY_S:
            toggleShading ^= 1

def get_mouse_coord(window):
    global lxpos, lypos, rxpos ,rypos, ldx, ldy, rdx, rdy
    if LeftButtonPressed:
        tmp_x, tmp_y = glfw.get_cursor_pos(window)
        tmp_y = (-tmp_y) + 640
        if tmp_x < WindowXSize and tmp_y < WindowYSize and tmp_x > 0 and tmp_y > 0:
            ldx += (tmp_x -lxpos) / WindowXSize
            ldy += (tmp_y -lypos) / WindowYSize
            lxpos = tmp_x
            lypos = tmp_y
            #print("Left Button pushed and ldx : %f and ldy : %f" %(ldx,ldy))
    if RightButtonPressed:
        tmp_x, tmp_y = glfw.get_cursor_pos(window)
        tmp_y = (-tmp_y) + 640
        if tmp_x < WindowXSize and tmp_y < WindowYSize and tmp_x > 0 and tmp_y > 0:
            #print(tmp_y , rypos)
            rdx = (tmp_x -rxpos) / WindowXSize
            rdy = (tmp_y -rypos) / WindowYSize
            rxpos = tmp_x
            rypos = tmp_y
            #print("Right Button pushed and rdx : %f and rdy : %f" %(rdx, rdy))

def drop_callback(window, path):
    global vertexList, normalList, faceList
    vertexList = []
    normalList = []
    faceList = []
    numOf3V = 0
    numOf4V = 0
    numOfBigV = 0
    with open(path[0], "r") as f:
        for line in f:
                split = line.split()
                #if blank line, skip
                if not len(split):
                        continue
                if split[0] == "v":
                        vertexList.append(split[1:])
                elif split[0] == "vn":
                        normalList.append(split[1:])
                elif split[0] == "f":
                        faceList.append(split[1:])
    print("file name :", path[0].split('/')[-1])
    print("face # : %d" %(len(faceList)))
    for face in faceList:
        if(len(face) == 3):
            numOf3V += 1
        elif (len(face) == 4):
            numOf4V += 1
        else:
            numOfBigV += 1
    print("Number of faces with 3 vertices : %d" %numOf3V)
    print("Number of faces with 4 vertices : %d" %numOf4V)
    print("Number of faces with more than 4 vertices : %d" %numOfBigV)

def createVertexArrayAndNormalArrayAndIndexArray():
    varr = np.array(vertexList, dtype=np.float32)
    if toggleShading == 0:
        narr = np.array(normalList, dtype=np.float32)
    else:
        tmp_narr = np.array(normalList, dtype=np.float32)
        narr = np.zeros((varr.size, 3), np.float32)
    tmp_iarr = []
    for face in faceList:
        ttmp_iarr = []
        for vertex in face:
            index = vertex.split("/")
            ttmp_iarr.append(int(index[0]) - 1)
            if toggleShading == 1:
                narr[int(index[0]) -1] += tmp_narr[int(index[2]) - 1]
        loop_size = len(ttmp_iarr) - 3
        i = 0
        while(i <= loop_size):
            tmp_iarr.append([ttmp_iarr[0], ttmp_iarr[i+1], ttmp_iarr[i+2]])
            i += 1
    iarr = np.array(tmp_iarr,dtype = np.uint)
    if toggleShading == 1:
        for i in narr:
            i = normalize(i)
    return varr, narr, iarr

def draw_glDrawElement():
    varr, narr, iarr = createVertexArrayAndNormalArrayAndIndexArray()
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_FLOAT, 3 * narr.itemsize, narr)
    glVertexPointer(3, GL_FLOAT, 3 * varr.itemsize, varr)
    glDrawElements(GL_TRIANGLES, iarr.size, GL_UNSIGNED_INT, iarr)

def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return tuple((v / norm).tolist())

def main():
    if not glfw.init():
        return
    window = glfw.create_window(WindowXSize, WindowYSize, "20160025996", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_cursor_pos_callback(window, cursor_callback)
    glfw.set_mouse_button_callback(window, button_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.set_key_callback(window, key_callback)
    glfw.set_drop_callback(window, drop_callback)
    glfw.swap_interval(1)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render(window)
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
