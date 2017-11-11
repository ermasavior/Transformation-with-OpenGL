# module transformation
import math
import numpy as np

def KaliMatriks (A, B):
    # mengalikan dua buah matriks. asumsi jumlah kolom A = jumlah baris B
    BrsA = len(A)
    KolA = len(A[0])
    BrsB = len(B)
    KolB = len(B[0])

    C = [[0 for column in range(KolA)] for row in range(BrsB)]
    for j in range(BrsB):
        for i in range(KolB):
            for k in range(KolB):
                C[j][i] += A[i][k] * B[j][k]
    return C

def translate2D(M,dx,dy):
    # menghasilkan hasil kali matriks translasi dengan matriks koordinat
    NKol = len(M[0])
    NBrs = len(M)
    Mtrans = [[0 for column in range(NKol)] for row in range(NBrs)]
    Mtrans = ([[1, 0, dx],
               [0, 1, dy],
               [0, 0, 1]])
    M = KaliMatriks(Mtrans, M)
    return M

def dilate(M, k):
    # menghasilkan hasil kali matriks dilatasi dengan matriks koordinat
    Md = [[0 for column in range(3)] for row in range(3)]
    Md = ([[k, 0, 0],
           [0, k, 0],
           [0, 0, 1]])
    M = KaliMatriks(Md,M)
    return M

def rotate2D(M, deg, x, y):
    # menghasilkan hasil kali matriks rotasi dengan matriks koordinat
    pi = 3.14159265359
    Mrot = [[0 for column in range(3)] for row in range(3)]
    a = math.cos(deg*pi/180)
    b = math.sin(deg*pi/180)
    Mrot = ([[a, b*-1, 0],
             [b, a, 0],
             [0, 0, 1]])
    M = translate2D(M, x*-1, y*-1)
    M = KaliMatriks(Mrot, M)
    M = translate2D(M, x, y)
    return M

def reflect2D(M, param):
    # menghasilkan hasil kali matriks refleksi dengan matriks koordinat
    Mref = [[0 for column in range(3)] for row in range(3)]
    if (param == "x"):
        Mref = ([[1, 0, 0],
                 [0, -1, 0],
                 [0, 0, 1]])
        M = KaliMatriks(Mref, M)
    elif (param == "y"):
        Mref = ([[-1, 0, 0],
                 [0, 1, 0],
                 [0, 0, 1]])
        M = KaliMatriks(Mref, M)
    elif (param == "x=y"):
        Mref = ([[0, 1, 0],
                 [1, 0, 0],
                 [0, 0, 1]])
        M = KaliMatriks(Mref, M)
    elif (param == "x=-y"):
        Mref = ([[0, -1, 0],
                 [-1, 0, 0],
                 [0, 0, 1]])
        M = KaliMatriks(Mref, M)
    elif (param == "point"):
        NKol = len(M[0])
        Mtrans = [[0 for column in range(NKol)] for row in range(3)]
        inputpoint = input("Input reflection point x y: ")
        titik = inputpoint.split(" ")
        Mref = ([[-1, 0, 0],
                 [0, -1, 0],
                 [0, 0, -1]])
        M = KaliMatriks(Mref, M)
        M = translate2D(M, 2*int(titik[0]), 2*int(titik[1]))
    else:
        print("Invalid input.")
    return M

def shear2D(M, param, k):
    # menghasilkan hasil kali matriks shear dengan matriks koordinat
    Mshear = [[0 for column in range(3)] for row in range(3)]
    if (param == "x"):
        Mshear = ([[1, k, 0],
                   [0, 1, 0],
                   [0, 0, 1]])
    elif (param == "y"):
        Mshear = ([[1, 0, 0],
                   [k, 1, 0],
                   [0, 0, 1]])
    M = KaliMatriks(Mshear, M)
    return M

def stretch(M, param, k):
    # menghasilkan hasil kali matriks stretch dengan matriks koordinat
    Mstretch = [[0 for column in range(3)] for row in range(3)]
    if (param == "x"):
        Mstretch = ([[k, 0, 0],
                     [0, 1, 0],
                     [0, 0, 1]])
    elif (param == "y"):
        Mstretch = ([[1, 0, 0],
                     [0, k, 0],
                     [0, 0, 1]])
    else:
        print("Invalid input")
        Mstretch = ([[1, 0, 0],
                     [0, 1, 0],
                     [0, 0, 1]])
    M = KaliMatriks(Mstretch, M)
    return M

def custom2D(M, a, b, c, d):
    # menghasilkan hasil kali matriks custom dengan matriks koordinat
    Mcust = [[0 for column in range(3)] for row in range(3)]
    Mcust = ([[a,b,0],
              [c,d,0],
              [0,0,1]])
    M = KaliMatriks(Mcust, M)
    return M

def multmenu(points_matrix, n):
    # menghasilkan matriks hasil transformasi beberapa command
    mult_matrix = points_matrix
    for i in range (0,n):
        stat = input("(Mult) Enter your command (in lower case): ")
        command = stat.split(" ")
        if(command[0]=='translate'):
            mult_matrix = translate2D(mult_matrix,int(command[1]),int(command[2]))
        elif(command[0]=='dilate'):
            mult_matrix = dilate(mult_matrix,float(command[1]))
        elif(command[0]=='rotate'):
            mult_matrix = rotate2D(mult_matrix,float(command[1]),float(command[2]),float(command[3]))
        elif(command[0]=='reflect'):
            mult_matrix = reflect2D(mult_matrix, command[1])
        elif(command[0]=='shear'):
            mult_matrix = shear2D(mult_matrix, command[1], float(command[2]))
        elif(command[0]=='stretch'):
            mult_matrix = stretch(mult_matrix, command[1], float(command[2]))
        elif(command[0]=='custom'):
            mult_matrix = custom2D(mult_matrix, int(command[1]), int(command[2]), int(command[3]), int(command[4]))
        else:
            print("Wrong command, please re-enter")
    points_matrix = mult_matrix
    return points_matrix