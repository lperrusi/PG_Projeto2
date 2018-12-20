from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

globVector = []
deltaOne = []
deltaTwo = []
firstDerivate = []
secondDerivate = []
curvatureK = []
vetores = []
debug = False


# Trata todas as chamadas necessarias para realizacao das contas
def bezier(pontos, factor):
    global globVector
    global deltaOne
    global deltaTwo
    global firstDerivate
    global secondDerivate
    global vetores
    global curvatureK
    global debug
    globVector = []
    firstDerivate = []

    t = 0
    plus_factor = 1.0 / factor

    while t <= 1:
        bezier_Castel(pontos, t)
        t += plus_factor

    # Chamada do calculo do delta um e da primeira derivada
    if len(pontos) > 1:

        getDeltaOne(pontos)
        firstDerivate = []
        u = 0
        while u <= 1:
            first_derivate_castel(pontos, deltaOne, u)
            u += plus_factor

        if debug: print deltaOne
        if debug: print firstDerivate

    # Chamada do calculo do delta dois e da segunda derivada
    if len(pontos) > 2:
        getDeltaTwo(pontos)
        secondDerivate = []
        u = 0
        while u <= 1:
            second_derivate_castel(pontos, deltaTwo, u)
            u += plus_factor

        if debug: print deltaTwo
        if debug: print len(secondDerivate)

    # Chamada do calculo de curvatura
    if len(pontos) > 2:
        curvatureK = []
        curvature(firstDerivate, secondDerivate)

        if debug: print curvatureK

    print "\n"
    return globVector


# Calculo da curva de bezier usando o algoritmo de casteljau
def bezier_Castel(pontos, t):
    global globVector
    global vetores
    num_points = len(pontos)

    if num_points == 1:
        globVector.append(pontos[0])
        glVertex2f(pontos[0]['x'], pontos[0]['y'])
    else:
        updated_points = []

        for i in range(0, num_points - 1):
            p = {'x': 0, 'y': 0}
            p['x'] = t * pontos[i + 1]['x'] + (1 - t) * pontos[i]['x']
            p['y'] = t * pontos[i + 1]['y'] + (1 - t) * pontos[i]['y']

            updated_points.append(p)
        bezier_Castel(updated_points, t)


# Calcula o Delta um para usar na primeira derivada
def getDeltaOne(pontos):
    global deltaOne
    deltaOne = []
    size_pontos = len(pontos)

    for i in range(0, size_pontos - 1):
        p = {'x': 0.0, 'y': 0.0}
        deltaX = pontos[i + 1]['x'] - pontos[i]['x']
        deltaY = pontos[i + 1]['y'] - pontos[i]['y']
        p['x'] = deltaX * (size_pontos - 1)
        p['y'] = deltaY * (size_pontos - 1)
        deltaOne.append(p)


# Calculo da primeira derivada de bezier
def first_derivate_castel(pontos, deltaOne, t):
    global firstDerivate
    num_points = len(deltaOne)

    if num_points == 1:
        firstDerivate.append(deltaOne[0])
    else:
        updated_points = []

        for i in range(0, num_points - 1):
            p = {'x': 0.0, 'y': 0.0}
            p['x'] = t * deltaOne[i + 1]['x'] + (1 - t) * deltaOne[i]['x']
            p['y'] = t * deltaOne[i + 1]['y'] + (1 - t) * deltaOne[i]['y']

            updated_points.append(p)
        first_derivate_castel(pontos, updated_points, t)


# Calculo do delta dois para a segunda derivada de bezier
def getDeltaTwo(pontos):
    global deltaTwo
    deltaTwo = []
    size_pontos = len(pontos)

    for i in range(0, size_pontos - 2):
        p = {'x': 0.0, 'y': 0.0}
        deltaX = pontos[i + 2]['x'] - 2 * pontos[i + 1]['x'] + pontos[i]['x']
        deltaY = pontos[i + 2]['y'] - 2 * pontos[i + 1]['y'] + pontos[i]['y']
        p['x'] = deltaX * ((size_pontos - 1) * (size_pontos - 2))
        p['y'] = deltaY * ((size_pontos - 1) * (size_pontos - 2))
        deltaTwo.append(p)


# Calculo da segunda derivada de bezier
def second_derivate_castel(pontos, deltaTwo, t):
    global secondDerivate
    num_points = len(deltaTwo)

    if num_points == 1:
        secondDerivate.append(deltaTwo[0])
    else:
        updated_points = []

        for i in range(0, num_points - 1):
            p = {'x': 0.0, 'y': 0.0}
            p['x'] = t * deltaTwo[i + 1]['x'] + (1 - t) * deltaTwo[i]['x']
            p['y'] = t * deltaTwo[i + 1]['y'] + (1 - t) * deltaTwo[i]['y']

            updated_points.append(p)
        second_derivate_castel(pontos, updated_points, t)


# calculo da curvatura
def curvature(firstDerivate, secondDerivate):
    global curvatureK
    size = len(firstDerivate)

    for p in range(0, size):
        numK = (firstDerivate[p]['x'] * secondDerivate[p]['y']) - firstDerivate[p]['y'] * secondDerivate[p]['x']
        demK = math.pow(math.pow(firstDerivate[p]['x'], 2) + math.pow(firstDerivate[p]['y'], 2), 1.5)
        K = numK / demK
        curvatureK.append(K)
