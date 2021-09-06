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
vertexList = []
vertexList2 = []
normalList = []
faceList = []
stack = []
result = []
frame = 0
frametime = 0
initstate = []
vertexArr = []
start = 0
framecounter = 0
fileidx = -1
is_obj = 0

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
    gluPerspective(45, 1, 1, 20)
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
        cur = target + rotatexz(ldx * 5) @ (cur-target)
        cur = target + rotatey(ldy * 10) @ (cur-target)
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
    #glScalef(0.01, 0.01, 0.01)
    #if faceList != [] and result != []:
    drawAction()
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

def rotatexz(x):
    c = np.cos(x)
    s = np.sin(x)
    return np.array([[c,0,-s],[0,1,0],[s,0,c]])

def rotatey(rad):
    c = np.cos(rad)
    s = np.sin(rad)
    return np.array([[1,0,0],[0,c,-s],[0,s,c]])

def rotateX(rad):
    rad = np.deg2rad(float(rad))
    M = np.identity(4)
    M[:3, :3] = [[1,0,0],
                   [0, np.cos(rad), -np.sin(rad)],
                   [0, np.sin(rad), np.cos(rad)]]
    return M



def rotateY(rad):
    rad = np.deg2rad(float(rad))
    M = np.identity(4)
    M[:3, :3] = [[np.cos(rad), 0, np.sin(rad)],
                   [0,1,0],
                   [-np.sin(rad), 0, np.cos(rad)]]
    return M

def rotateZ(rad):
    rad = np.deg2rad(float(rad))
    M = np.identity(4)
    M[:3, :3] = [[np.cos(rad), -np.sin(rad), 0], [np.sin(rad), np.cos(rad), 0], [0,0,1]]
    
    return M

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
            rdx = 0
            rdy = 0
 
def scroll_callback(window, xoffset, yoffset):
    global ZoomStats
    ZoomStats += yoffset

def key_callback(window, key, scancode, action, mods):
    global toggleWireToSolid, toggleShading, start
    if action==glfw.PRESS or action == glfw.REPEAT:
        if key==glfw.KEY_Z:
            toggleWireToSolid ^= 1
        if key==glfw.KEY_S:
            toggleShading ^= 1
        if key==glfw.KEY_SPACE:
            start = 1

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
    if RightButtonPressed:
        tmp_x, tmp_y = glfw.get_cursor_pos(window)
        tmp_y = (-tmp_y) + 640
        if tmp_x < WindowXSize and tmp_y < WindowYSize and tmp_x > 0 and tmp_y > 0:
            rdx = (tmp_x -rxpos) / WindowXSize
            rdy = (tmp_y -rypos) / WindowYSize
            rxpos = tmp_x
            rypos = tmp_y

def drop_callback(window, path):
    global stack, result, frame, frametime, initstate, vertexArr, start, framcounter,vertexList, normalList, faceList, fileidx, is_obj
    with open(path[0], "r") as f:
        if path[0][-3:] == "bvh":
            stack = []
            result = []
            vertexArr = []
            start = 0
            framecounter = 0
            frame = 0
            frametime = 0
            initstate = []
            cnt = 0
            tmp = []
            is_open = 0
            level = 0 
            idx = 0
            stack_idx = 1
            length = 0
            init = 0
            joints = []
            for line in f:
                split = line.split()
                if not len(split):
                    continue
                if split[0] == "HIERARCHY" or split[0] == "MOTION" or split[0] == "End":
                    pass
                elif split[0] == "JOINT" or split[0] == "ROOT":
                    joints.append(split[1])
                elif split[0] == "{":
                    if len(tmp) > 2:
                        length += 1
                    if level != 0:
                        stack.append(tmp)
                    level += 1
                    is_open = 1
                    tmp = []
                elif split[0] == "OFFSET":
                    tmp.append(level)
                    tmp.append(split)
                elif split[0] == "CHANNELS":
                    tmp.append(split)
                elif split[0] == "}":
                    level -= 1
                elif split[0] == "Frames:":
                    frame = int(split[1])
                elif split[0] == "Frame" and split[1] == "Time:":
                    frametime = float(split[2])
                else:
                    idx = 0
                    stack_length = len(stack)
                    while idx < stack_length:
                        if idx  == 0:
                            init += 1
                            x1 = split[0]
                            y1 = split[1]
                            z1 = split[2]
                            rt1 = split[3]
                            rt2 = split[4]
                            rt3 = split[5]
                            stack_idx = 6

                            M = np.identity(4)
                            T = np.identity(4)
                            offset = np.array([float(x1), float(y1), float(z1)])
                            T[:3, 3] = offset
                            if stack[idx][2][7].upper() == "XROTATION":
                                R1 = rotateX(rt3)
                            elif stack[idx][2][7].upper() == "YROTATION":
                                R1 = rotateY(rt3)
                            elif stack[idx][2][7].upper() == "ZROTATION":
                                R1 = rotateZ(rt3)
                            if stack[idx][2][6].upper() == "XROTATION":
                                R2 = rotateX(rt2)
                            elif stack[idx][2][6].upper() == "YROTATION":
                                R2 = rotateY(rt2)
                            elif stack[idx][2][6].upper() == "ZROTATION":
                                R2 = rotateZ(rt2)
                            if stack[idx][2][5].upper() == "XROTATION":
                                R3 = rotateX(rt1)
                            elif stack[idx][2][5].upper() == "YROTATION":
                                R3 = rotateY(rt1)
                            elif stack[idx][2][5].upper() == "ZROTATION":
                                R3 = rotateZ(rt1)

                            M = R3 @ R2 @ R1 @ M
                            M = T @ M
                            I = np.identity(4)
                            if init == 1:
                                initstate.append([stack[idx][0], I])
                            result.append([stack[idx][0], M])
                            idx += 1
                            continue
                        if len(stack[idx]) == 3:
                            M = np.identity(4)
                            T = np.identity(4)
                            offset = np.array([float(stack[idx][1][1]), float(stack[idx][1][2]), float(stack[idx][1][3])])
                            T[:3, 3] = offset
                            r1 = split[stack_idx]
                            stack_idx += 1
                            r2 = split[stack_idx]
                            stack_idx += 1
                            r3 = split[stack_idx]
                            stack_idx += 1
                            if stack[idx][2][4].upper() == "XROTATION":
                                R1 = rotateX(r3)
                            elif stack[idx][2][4].upper() == "YROTATION":
                                R1 = rotateY(r3)
                            elif stack[idx][2][4].upper() == "ZROTATION":
                                R1 = rotateZ(r3)
                            if stack[idx][2][3].upper() == "XROTATION":
                                R2 = rotateX(r2)
                            elif stack[idx][2][3].upper() == "YROTATION":
                                R2 = rotateY(r2)
                            elif stack[idx][2][3].upper() == "ZROTATION":
                                R2 = rotateZ(r2)
                            if stack[idx][2][2].upper() == "XROTATION":
                                R3 = rotateX(r1)
                            elif stack[idx][2][2].upper() == "YROTATION":
                                R3 = rotateY(r1)
                            elif stack[idx][2][2].upper() == "ZROTATION":
                                R3 = rotateZ(r1)

                            M = R3 @ R2 @ R1 @ M
                            M = T @ M
                            if init == 1:
                                initstate.append([stack[idx][0],T])
                            result.append([stack[idx][0], M])
                        else:
                            T = np.identity(4)
                            offset = np.array([float(stack[idx][1][1]), float(stack[idx][1][2]), float(stack[idx][1][3])])
                            T[:3, 3] = offset
                            if init == 1:
                                initstate.append([stack[idx][0],T])
                            result.append([stack[idx][0], T])
                        idx += 1
             


            print("filme name : ", path[0].split('/')[-1])
            print("Number of frames : ", frame)
            print("FPS : ", 1 / frametime)
            print("Number of joints : ", len(joints))
            print("List of all joint names : ", joints)
        elif path[0][-3:] == "obj":
            is_obj = 1
            fileidx = -1
            vertexList = []
            normalList = []
            faceList = []
            for line in f:
                split = line.split()
                if not len(split):
                        continue
                if split[0] == "o":
                        fileidx += 1
                if split[0] == "v":
                        vertexList.append([fileidx,split[1:]])
                elif split[0] == "vn":
                        normalList.append([fileidx,split[1:]])
                elif split[0] == "f":
                        faceList.append([fileidx,split[1:]])


def drawInitialState():
    global initstate, vertexArr
    idx = 0
    draw = 0
    length = len(initstate)
    glBegin(GL_LINES)
    while idx < length:
        if idx == 0:
            vertexArr.append(initstate[idx][1])
        else:
            if initstate[idx][0] > initstate[idx - 1][0]:
                vertexArr.append(vertexArr[idx - 1] @ initstate[idx][1])
                glVertex3fv((vertexArr[idx - 1] @ [0,0,0,1])[:-1])
                glVertex3fv((vertexArr[idx] @ [0,0,0,1])[:-1])
            else:
                tmp = idx - 1
                while initstate[idx][0] <= initstate[tmp][0]:
                    tmp -= 1
                vertexArr.append(vertexArr[tmp] @ initstate[idx][1])
                glVertex3fv((vertexArr[tmp] @ [0,0,0,1])[:-1])
                glVertex3fv((vertexArr[idx] @ [0,0,0,1])[:-1])
        idx += 1
    glEnd()       

def drawInitialState2():
    global initstate, vertexArr, vertexList, vertexList2
    idx = 0
    draw = 0
    v_idx = 0
    length = len(initstate)
    if(vertexList2 != []):
        draw_glDrawElement()
        return
    while idx < length:
        if idx == 0:
            vertexArr.append(initstate[idx][1])
            for x in vertexList:
                if x[0] == v_idx:
                    new = np.array([0.,0.,0.,1.])
                    new[:3] = x[1]
                    new_axis = (vertexArr[idx] @ new)[:-1]
                    vertexList2.append([x[0], new_axis])
                elif x[0] < v_idx:
                    continue
                else:
                    break
            v_idx += 1
        else:
            if initstate[idx][0] > initstate[idx - 1][0]:
                vertexArr.append(vertexArr[idx - 1] @ initstate[idx][1])

                if idx + 1 < length and initstate[idx][0] >= initstate[idx + 1][0]:
                    idx += 1 
                    continue

                for x in vertexList:
                    if x[0] == v_idx:
                        new = np.array([0.,0.,0.,1.])
                        new[:3] = x[1]
                        new_axis = (vertexArr[idx] @ new)[:-1]
                        vertexList2.append([x[0], new_axis])
                    elif x[0] < v_idx:
                        continue
                    else:
                        break
                v_idx +=1

            else:
                tmp = idx - 1
                while initstate[idx][0] <= initstate[tmp][0]:
                    tmp -= 1
                vertexArr.append(vertexArr[tmp] @ initstate[idx][1])
                for x in vertexList:
                    if x[0] == v_idx:
                        new = np.array([0.,0.,0.,1.])
                        new[:3] = x[1]
                        new_axis = (vertexArr[idx] @ new)[:-1]
                        vertexList2.append([x[0], new_axis])
                    elif x[0] < v_idx:
                        continue
                    else:
                        break
                v_idx += 1
        idx += 1
    draw_glDrawElement()

def drawMove():
    global result, framecounter
    actionArr = []
    idx = 0
    length = len(stack)
    idx = framecounter * length
    glBegin(GL_LINES)
    while idx < length * (framecounter + 1):
        t_idx = idx % length
        if t_idx == 0:
            actionArr.append(result[idx][1])
        elif result[t_idx][0] > result[t_idx - 1][0]:
            actionArr.append(actionArr[t_idx - 1] @ result[idx][1])
            glVertex3fv((actionArr[t_idx - 1] @ [0, 0, 0, 1])[:-1])
            glVertex3fv((actionArr[t_idx] @ [0, 0, 0, 1])[:-1])
        else:
            tmp = t_idx - 1
            while result[t_idx][0] <= result[tmp][0]:
                tmp -= 1
            actionArr.append(actionArr[tmp] @ result[idx][1])
            glVertex3fv((actionArr[tmp] @ [0, 0, 0, 1])[:-1])
            glVertex3fv((actionArr[t_idx] @ [0, 0, 0, 1])[:-1])
        idx += 1
    glEnd()
    framecounter += 1
    if framecounter == frame:
        framecounter = 0
        idx = 0

def drawMove2():
    global result, framecounter, vertexList, vertexList2
    actionArr = []
    idx = 0
    length = len(stack)
    idx = framecounter * length
    v_idx = 0
    while idx < length * (framecounter + 1):
        t_idx = idx % length
        if t_idx == 0:
            actionArr.append(result[idx][1])
            for x in vertexList:
                if x[0] == v_idx:
                    new = np.array([0.,0.,0.,1.])
                    new[:3] = x[1]
                    new_axis = (actionArr[t_idx] @ new)[:-1]
                    vertexList2.append([x[0], new_axis])
                elif x[0] < v_idx:
                    continue
                else:
                    break
            v_idx += 1
        elif result[t_idx][0] > result[t_idx - 1][0]:
            actionArr.append(actionArr[t_idx - 1] @ result[idx][1])
            if t_idx + 1 < length and result[t_idx][0] >= result[t_idx + 1][0]:
                idx += 1 
                continue
            for x in vertexList:
                if x[0] == v_idx:
                    new = np.array([0.,0.,0.,1.])
                    new[:3] = x[1]
                    new_axis = (actionArr[t_idx] @ new)[:-1]
                    vertexList2.append([x[0], new_axis])
                elif x[0] < v_idx:
                    continue
                else:
                    break
            v_idx += 1
        else:
            tmp = t_idx - 1
            while result[t_idx][0] <= result[tmp][0]:
                tmp -= 1
            actionArr.append(actionArr[tmp] @ result[idx][1])
            for x in vertexList:
                if x[0] == v_idx:
                    new = np.array([0.,0.,0.,1.])
                    new[:3] = x[1]
                    new_axis = (actionArr[t_idx] @ new)[:-1]
                    vertexList2.append([x[0], new_axis])
                elif x[0] < v_idx:
                    continue
                else:
                    break
            v_idx += 1
        idx += 1
    framecounter += 1
    draw_glDrawElement()
    vertexList2 = []
    v_idx = 0
    if framecounter == frame:
        framecounter = 0
        idx = 0
        vertexList2 = []
        v_idx = 0

def drawAction():
    global vertexArr, framecounter
    if start == 0:
        framecounter = 0
        if is_obj == 0:
            drawInitialState()
        else:
            if result == []:
                return
            drawInitialState2()
    else:
        if is_obj == 0:
            drawMove()
        else:
            if result == []:
                return
            drawMove2()

def createVertexArrayAndNormalArrayAndIndexArray():
    #if start == 0:
    #    vl = [vertexList[i][1] for i in range(len(vertexList))]
    #    print("vertexList Size",len(vertexList))
    #else:
    vl = [vertexList2[i][1] for i in range(len(vertexList2))]
    nl = [normalList[i][1] for i in range(len(normalList))]
    fl = [faceList[i][1] for i in range(len(faceList))]
    '''
    if start == 0:
        vl = [vertexList[n][i] for i in range(len(vertexList[n]))]
    else:
        vl = [vertexList[n][i] for i in range(len(vertexList[n]))]
    nl = [normalList[n][i] for i in range(len(normalList[n]))]
    fl = [faceList[n][i] for i in range(len(faceList[n]))]
    '''
    #varr = np.array(vertexList, dtype=np.float32)
    varr = np.array(vl, dtype=np.float32)
    if toggleShading == 0:
        #narr = np.array(normalList, dtype=np.float32)
        narr = np.array(nl, dtype=np.float32)
    else:
        #tmp_narr = np.array(normalList, dtype=np.float32)
        tmp_narr = np.array(nl, dtype=np.float32)
        narr = np.zeros((varr.size, 3), np.float32)
    tmp_iarr = []
    #for face in faceList:
    for face in fl:
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
