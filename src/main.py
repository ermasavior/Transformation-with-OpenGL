from OpenGL.GL import *         #library OpenGL
from OpenGL.GLUT import *   
from OpenGL.GLU import *    
from OpenGL.arrays import vbo
from OpenGL.GL import shaders
from transformation import *    #modul transformasi
import time                     #library timer
import _thread                  #library multithread
import sys

window = 0                                  # glut window number
width, height = 1000, 1000                  # window size
input_finish = False

def refresh2d(width, height):
    # setting koordinat ruang 2 dimensi
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-500, 500, -500, 500, -500, 500)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def inputpoints():
    # menerima input koordinat titik bidang dan menyimpannya dalam sebuah matriks
    global n, points_matrix, input_finish, orig_matrix
    n = int(input("Input number of points: "))
    points_matrix = [[0 for column in range(3)] for row in range(n)]
    for i in range(0, n):
        x = int(input("Input x: "))
        y = int(input("Input y: "))
        points_matrix[i][0] = x
        points_matrix[i][1] = y
        points_matrix[i][2] = 1
    orig_matrix = points_matrix
    input_finish = True

def mainmenu():
    # menampilkan main menu dan meng-update matriks penyimpan titik yang ditampilkan tiap saat
    global n, points_matrix, input_finish, orig_matrix
    print("""
     _____                            __                         
    |_   _|                          / _|                        
      | |   _ __   __ _  _ __   ___ | |_   ___   _ __  _ __ ___    
      | |  | '__| / _` || '_ \ / __||  _| / _ \ | '__|| '_ ` _ \ 
      | |  | |   | (_| || | | |\__ \| |  | (_) || |   | | | | | |
      \_/  |_|    \__,_||_| |_||___/|_|   \___/ |_|   |_| |_| |_|
    """)
    # input titik-titik bidang
    inputpoints()
    temp_matrix = points_matrix

    print("""
    Command menu:
     ~ translate dx dy
     ~ dilate k
     ~ rotate deg a b
     ~ reflect ("x"/"y"/"x=y"/"x=-y"/"point")
     ~ shear ("x"/"y") k
     ~ stretch ("x"/"y") k
     ~ custom a b c d
     ~ multiple n
     ~ reset
     ~ exit
    """)
    # input command
    stat = input("Enter your command (in lower case): ")
    command = stat.split(" ")
    # bagi kasus sesuai input command
    if (command[0]=='exit'):
        glutLeaveMainLoop()
        _thread.exit()
    else:
        while(command[0]!='exit'):
            starttime = time.time()
            if(command[0]=='translate'):
                # translate with motion. loop with timer (time.sleep)
                i = 0
                j = 0
                k = 0
                l = 0
                while(abs(i)<=abs(float(command[1])) or abs(j)<=abs(float(command[2]))):              
                    points_matrix = translate2D(temp_matrix,k,l)
                    if (abs(i)<=abs(float(command[1]))):
                        if (float(command[1])>=0):
                            i = i+0.1
                        else:
                            i = i-0.1
                        k = i
                    else:
                        k = i-0.1
                    if (abs(j)<=abs(float(command[2]))):
                        if (float(command[2])>=0):
                            j = j+0.1
                        else:
                            j = j-0.1
                        l = j
                    else:
                        l = j-0.1
                    time.sleep(0.00005 - ((time.time() - starttime) % 0.00005))
            elif(command[0]=='dilate'):
                # dilate with motion. loop with timer (time.sleep)
                i = 1
                if (float(command[1])>1):
                    while(i<=float(command[1])):
                        points_matrix = dilate(temp_matrix,i)
                        i = i+0.1
                        time.sleep(0.05 - ((time.time() - starttime) % 0.05))
                else:
                    while(i>=float(command[1])):
                        points_matrix = dilate(temp_matrix,i)
                        i = i-0.1
                        time.sleep(0.05 - ((time.time() - starttime) % 0.05))
            elif(command[0]=='rotate'):
                # rotate with motion. loop with timer (time.sleep)
                i = 0
                while(abs(i)<=abs(float(command[1]))):
                    points_matrix = rotate2D(temp_matrix,i,float(command[2]),float(command[3]))
                    if (float(command[1])>=0):
                        i = i+0.1
                    else:
                        i = i-0.1
                    time.sleep(0.005 - ((time.time() - starttime) % 0.005))
            elif(command[0]=='reflect'):
                points_matrix = reflect2D(points_matrix, command[1])
            elif(command[0]=='shear'):
                # shear with motion. loop with timer (time.sleep)
                i = 0
                while(abs(i)<=abs(float(command[2]))):
                    points_matrix = shear2D(temp_matrix, command[1], i)
                    if (float(command[2])>=0):
                        i = i+0.1
                    else:
                        i = i-0.1
                    time.sleep(0.05 - ((time.time() - starttime) % 0.05))
            elif(command[0]=='stretch'):
                # stretch with motion. loop with timer (time.sleep)
                i = 1
                if (float(command[2])>1):
                    while(i<=float(command[2])):
                        points_matrix = stretch(temp_matrix, command[1], i)
                        i = i+0.1
                        time.sleep(0.05 - ((time.time() - starttime) % 0.05))
                else:
                    while(i>=float(command[2])):
                        points_matrix = stretch(temp_matrix, command[1], i)
                        i = i-0.1
                        time.sleep(0.05 - ((time.time() - starttime) % 0.05))
            elif(command[0]=='custom'):
                # transformasi custom
                points_matrix = custom2D(points_matrix, int(command[1]), int(command[2]), int(command[3]), int(command[4]))
            elif(command[0]=='multiple'):
                # multiple command
                points_matrix = multmenu(points_matrix,int(command[1]))
            elif(command[0]=='reset'):
                # mengembalikan bentuk original sebelum transformasi
                points_matrix = orig_matrix
            else:
                print("Wrong command, please re-enter")
            temp_matrix = points_matrix
            stat = input("Enter your command (in lower case): ")
            command = stat.split(" ")

        if(command[0]=='exit'):
            # exit command
            glutLeaveMainLoop()
            _thread.exit()

def draw(): 
    # menampilkan grafis input bidang 2D dan garis sumbu x dan y
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # clear the screen
    glLoadIdentity()                                   # reset position
    refresh2d(width, height)
    drawAxes()
    drawShape()
    glutSwapBuffers()                                  # important for double buffering

def drawShape():
    # translasi matriks ke koordinat bidang yang akan ditampilkan
    global points_matrix, input_finish
    glColor3f(0.0, 0.0, 1.0)                           # set color
    if (input_finish):
        glBegin(GL_POLYGON)
        for i in points_matrix:
            glVertex2f(i[0], i[1])
        glEnd()

def drawAxes():
    # gambar sumbu x dan y
	glColor3f(0.0, 1.0, 0.0)   
	glBegin(GL_LINES)
	glVertex2f(-500,0)
	glVertex2f(500,0)
	glVertex2f(0,-500)
	glVertex2f(0,500)
	glEnd()

# initialization
_thread.start_new_thread(mainmenu, ())
glutInit()                                                  # initialize glut
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
glutInitWindowSize(width, height)                           # set window size
glutInitWindowPosition(500, 0)                              # set window position
window = glutCreateWindow(b"Tugas Besar 2 Aljabar Geometri")# create window with title
glutDisplayFunc(draw)                                       # set draw function callback
glutIdleFunc(draw)                                          # draw all the time
glutMainLoop()                                              # start everything