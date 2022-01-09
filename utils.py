import pygame
import random

class Rect:

    def __init__(self, x: float, y: float, width: int, height: int):
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height
        self.__pyg_rect = pygame.Rect(
            int(self.__x), int(self.__y), self.__width, self.__height)

    def __str__(self):
        return 'x: {} y: {} width: {} height: {}'.format(self.__x, self.__y,
            self.__width, self.__height)

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, x):
        self.__x = float(x)
        self.__pyg_rect.x = int(self.__x)

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, y):
        self.__y = float(y)
        self.__pyg_rect.y = int(self.__y)

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    def colliderect(self, other):
        if self.x+self.width > other.x and \
                other.x+other.width > self.x and \
                self.y+self.height > other.y and \
                other.y+other.height > self.y:
            return True
        else:
            return False
    #overlowads other method with an adjustment variable
    def colliderect(self, other, adjustment):
        x=other.x+adjustment
        y=other.y+adjustment
        width=other.width-adjustment*2
        height=other.height-adjustment*2
        if self.x + self.width > x and \
                x+width > self.x and \
                self.y + self.height > y and \
                y+height > self.y:
            return True
        else:
            return False
    #returns shared rect space between two rects
    def rectintersection(self, other):
        x5 = max(self.x, other.x)
        x6 = min(self.x+self.width, other.x+other.width)
        y5 = max(self.y, other.y)
        y6 = min(self.y+self.height, other.y+other.height)
        if x5 > x6 or y5 > y6:
            return Rect(0, 0, 0, 0)
        return Rect(x5, y5, x6-x5, y6-y5)

black = (0,0,0)
class Room:
    def __init__(self, rect):
        self.__rect = rect
    def drawRoom(self, screen):
        screen.draw.rect(screen, black,rect)
def generateMap(numRooms,mapSize):
    matrix = [numRooms][numRooms]
    for i in range(0,numRooms):
        matrix[i]=i
        for j in i:
            j = Math.random(1,11)
            if j>numRooms or i==j:
                j = 0
    rooms = []
    #creates placeholders
    for i in range(numRooms):
        rooms.append(Room(Rect(0,0,0,0)))
    #creates first room to generate map from
    rooms[0] = Room(Rect(0,0,random.randint(mapSize/numRooms/2,mapSize/numRooms/5),random.randint(mapSize/numRooms/2,mapSize/numRooms/5)))
    
    #keeps track of rooms that have been initialized
    roomsInit = [False]*numRooms
    roomsInit[0] = True
    #keeps track of passages for each room and for what room
    passages = {}
    for i in range(numRooms):
        passages[i]=[None]*numRooms

    for i in matrix:
        # starts with first room connections
        for j in i:
            #checks for connection between room i and room j and if passage has already been created
            if j!=0 and passages[j][i]==None:
                #makes passageway
                tempRect = Rect(0,0,0,0)
                generatePassage(random.randint(1,4))
                for room in range(len(rooms)):
                    while roomsInit[room] and rooms[room].colliderect(tempRect):
                        generatePassage(random.randint(1,4))
                rooms.append(tempRect)
                passages[i][j]=numRooms


def generatePassage(direction):
    global tempRect
    if direction == 1: #top
        tempRect.height = matrix[i][j]*(mapSize/numRooms)/50
        tempRect.width = (mapSize/numRooms)/50
        tempRect.x = rooms[i].rect.x+rooms[i].rect.width/2
        tempRect.y = room[i].rect.y-tempRect.height
    elif direction == 2: #left
        tempRect.height =(mapSize/numRooms)/50
        tempRect.width = matrix[i][j]*(mapSize/numRooms)/50
        tempRect.x = rooms[i].rect.x-tempRect.width
        tempRect.y = rooms[i].rect.y+rooms[i].rect.height/2
    elif direction == 3: #right
        tempRect.height =(mapSize/numRooms)/50
        tempRect.width = matrix[i][j]*(mapSize/numRooms)/50
        tempRect.x = rooms[i].rect.x+rooms[i].rect.width
        tempRect.y = rooms[i].rect.y+rooms[i].rect.height/2
    elif direction == 3: # bottom
        tempRect.height = matrix[i][j]*(mapSize/numRooms)/50
        tempRect.width = (mapSize/numRooms)/50
        tempRect.x = rooms[i].rect.x+rooms[i].rect.width/2
        tempRect.y = rooms[i].rect.y+rooms[i].rect.height-tempRect.height
