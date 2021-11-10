import numpy as np
import pygame
import math
import random
from numpy import ones,vstack
from numpy.linalg import lstsq
import matplotlib.pyplot as plt

WIDTH = 750
HEIGHT = 750
FPS = 300
CELLS = 500
CELLSIZE = 5
BASECOLOUR = (0, 0, 0)
RADIUS = 25
#ELEMENTS = random.randint(3,7)
ELEMENTS = random.randint(3,7)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("poop fart")

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class Element():
    def __init__(self, num, color,alpha,beta):
        self.num = num
        self.color = (0,0,0)
        self.alpha = 0
        self.beta = 0
        self.numInf = 0
        self.InfVal = []
        self.attraction_maps_x = []
        self.attraction_maps_y = []
        self.friction = random.randint(12,50)/10
    def colorSet(self):
        self.color = (random.randint(50,100),random.randint(50,100),random.randint(50,100))
        #self.color = (255,255,255)
        print(self.color)
    def alphaSet(self):
        #self.alpha = random.randint(170,180)
        self.alpha = 180
    def betaSet(self):
        #self.beta = random.randint(20,40)
        self.beta = 25
    def numInfSet(self):
        #self.numInf = float(random.randint(5,10)/10)
        self.numInf=random.randint(10,20)/10
        print(self.numInf)
    def InfSet(self):
        for i in range(0, ELEMENTS):
            self.InfVal.append(random.randint(-5,40)/20)
    def getInf(self, i):
        return self.InfVal[i]
    def attraction_maps_set(self, num,radius):
        for i in range(num):
            tempx,tempy = line_func(radius,5,2)
            self.attraction_maps_x.append(tempx)
            self.attraction_maps_y.append(tempy)
    def getFriction(self):
        return self.friction

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class Cell():
    def __init__(self, x, y, velocity, num, element):
        # x is x position, y is y position, alpha is current angle, beta is change angle, velocity is change magnitude
        self.x = x
        self.y = y
        self.velocity = velocity
        self.num = num
        self.pic = pygame.Rect(self.x, self.y, CELLSIZE, CELLSIZE)
        self.color = BASECOLOUR
        self.inf = 0
        self.leftRight = 0
        self.angle = 0
        self.colortype = random.randint(1,3)
        self.element = element
        self.yVec = 0
        self.xVec = 0

    def update(self,elements):

        if 0 < self.x + math.cos(self.angle) and self.x + math.cos(self.angle) < WIDTH-10:
            self.x += self.xVec
        else:
            self.loopx()
        if 0 < self.y + math.sin(self.angle) and self.y + math.sin(self.angle) < HEIGHT-10:
            self.y += self.yVec
        else:
            self.loopy()

        #print big V values to check for overflow errors
        self.yVec = friction(self.yVec,elements,self.element)
        self.xVec = friction(self.xVec,elements,self.element)

        if abs(self.yVec) > 10:
            print(self.yVec)
        if abs(self.xVec) > 10:
            print(self.xVec)


        self.pic = pygame.Rect(self.x, self.y, CELLSIZE, CELLSIZE)
    def getNum(self):
        return self.num

    def colour(self):
        return self.color

    def changeColour(self, color):
        self.color = (colorval(self.inf) * color[0], colorval(self.inf) * color[1], colorval(self.inf) * color[2])

    def loopx(self):
        if self.x > 100:
            self.x = 12
        else:
            self.x = WIDTH -12

    def loopy(self):
        if self.y > 100:
            self.y = 12
        else:
            self.y = HEIGHT -12

    def addInfluence(self):
        self.inf+=1

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def friction(vector,elements,elementNum):
    frictionVal = elements[elementNum].friction
    #if abs(vector) >10:
    #    vector = 10
    return vector/frictionVal


#creates graphs which map out a particles attraction to other particles, every particle will have an attraction map to every other particle
def line_func(radius, amplitude, num=None):
    points = []
    lines = []
    x = []
    y = []
    if num is None:
            num = random.randint(5, 10)

    y.append(-10)
    x.append(0)
    y.append(0)
    x.append(CELLSIZE*2)
    temp_x = CELLSIZE*2
    points.append([x[len(x)-1], y[len(y)-1]])

    for i in range(0, num):
        y.append(random.randint(-amplitude, amplitude)*(1 - (i/num)))
        a = random.randint(temp_x,RADIUS)
        x.append(a)
        temp_x = a
        points.append([x[len(x)-1], y[len(y)-1]])

    points.append([radius,random.randint(-amplitude, amplitude)])
    y.append(0)
    x.append(radius)
    points.append([x[len(x)-1], y[len(y) - 1]])
    print(points)
    plt.plot(x, y)
    plt.plot([0, radius], [0, 0])
    plt.show()

    return x,y


#radius = 100
#amplitude = 20
#num = 4

#for i in range(1):
    #x, y = line_func(radius, amplitude,num)
    #plt.plot(x,y)
    #plt.plot([0,radius], [0,0])
    #plt.show()


def leftright(cell,cell2,radius):
    x1 = (radius+1) * math.cos(180 + cell.angle)
    x2 = radius * math.cos(cell.angle)
    y1 = radius * math.sin(180 + cell.angle)
    y2 = radius * math.sin(cell.angle)

    xA = cell2.x
    yA = cell2.y

    v1 = (x2 - x1, y2 - y1)  # Vector 1
    v2 = (x2 - xA, y2 - yA)  # Vector 1
    xp = v1[0] * v2[1] - v1[1] * v2[0]  # Cross product
    if xp > 0:
        return 1 #clockwise
    elif xp < 0:
        return -1 #counter clockwise
    else:
        return 0 #same


def colorval(poopey):
    '''print(poopey)
    if poopey >5:
        return 1
    return (poopey/6)+0.16
    '''
    return 1


def dir(left, right):
    if left-right <1:
        return -1
    else:
        return 1


def sign(num):
    if num > 0:
        return 1
    elif num <0:
        return -1
    else:
        return 0


def collide(bins, radius,bx,by, elements):
    for x in range(bx):
        for y in range(by):
            for cell in bins[x][y]:
                for dx in {-1, 0, 1}:
                    for dy in {-1, 0, 1}:
                        try:
                            for c in bins[x + dx][y + dy]:
                                if cell.num < c.num:
                                    d = math.hypot(cell.x - c.x, cell.y - c.y)
                                    if d < radius:
                                        try:
                                            c.inf+=1
                                            cell.inf+=1
                                            cell.yVec += math.sin(math.atan2((c.y - cell.y), (c.x - cell.x))) * np.interp(d, elements[cell.element].attraction_maps_x[c.element], elements[cell.element].attraction_maps_y[c.element])
                                            cell.xVec += math.cos(math.atan2((cell.y - c.y), (c.x - cell.x))) * np.interp(d, elements[cell.element].attraction_maps_x[c.element], elements[cell.element].attraction_maps_y[c.element])

                                            c.yVec += math.sin(math.atan2((cell.y - c.y), (cell.x - c.x))) * np.interp(d, elements[c.element].attraction_maps_x[cell.element], elements[c.element].attraction_maps_y[cell.element])
                                            c.xVec += math.cos(math.atan2((c.y - cell.y), (cell.x - c.x))) * np.interp(d, elements[c.element].attraction_maps_x[cell.element], elements[c.element].attraction_maps_y[cell.element])
                                            '''
                                            if abs(cell.yVec) >= 7:
                                                cell.yVec = 7*sign(cell.yVec)
                                            if abs(cell.xVec) >= 7:
                                                cell.xVec = 7*sign(cell.xVec)
                                            if abs(c.yVec) >= 7:
                                                c.yVec = 7*sign(c.yVec)
                                            if abs(c.xVec) >= 7:
                                                c.xVec = 7*sign(c.xVec)
                                            '''
                                        except ZeroDivisionError:
                                            continue
                        except IndexError:
                            continue


def updateBins(cells,bxnum,bynum):
    bins = [0] * bxnum
    for x in range(len(bins)):
        bins[x] = [0] * bynum
        for y in range(len(bins[x])):
            bins[x][y] = []
    for cell in cells:
        bx = math.floor(cell.x / 100)
        by = math.floor(cell.y / 100)
        try:
            bins[bx][by].append(cell)
        except IndexError:
            continue
    return bins


# moves and then places the cells on the screen
def update(cells, radius, elements):
    WIN.fill((0,0.,0))
    for cell in cells:
        cell.update(elements)
        cell.changeColour(elements[cell.element].color)
        cell.inf = 0
        pygame.draw.circle(WIN, cell.colour(), (cell.pic.x, cell.pic.y), CELLSIZE)
    bxnum = 40
    bynum = 20
    bins = updateBins(cells,bxnum,bynum)
    collide(bins, radius,bxnum,bynum, elements)


def main():
    clock = pygame.time.Clock()
    run = True
    cells = []
    elements = []
    for i in range(ELEMENTS):
        element = Element(i,0,random.randint(-180,180),random.randint(-40,40))
        element.colorSet()
        element.alphaSet()
        element.betaSet()
        element.numInfSet()
        element.InfSet()
        element.attraction_maps_set(ELEMENTS,RADIUS)
        #print(str(element.alpha) + " || "+ str(element.beta) + " || " +str(element.numInf)+ " || "+ str(element.color)+ " || " + str(element.InfVal))
        elements.append(element)
    for i in range(CELLS):
        cell = Cell(random.randint(10, WIDTH-10), random.randint(10, HEIGHT-10), 0.1, i, random.randint(0,ELEMENTS-1))
        cells.append(cell)

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        update(cells, RADIUS, elements)
        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    main()
