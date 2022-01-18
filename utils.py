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

class Player:
    def __init(self,rect,image):
        self.__rect = rect
        self.__image = image
    @property
    def rect(self):
        return self.__rect

    @rect.setter
    def rect(self, rect):
        self.__rect = rect
    
    @property
    def image(self):
        return self.__image

    @image.setter
    def image(self, image):
        self.__image = image
    
class Tile:
    def __init__(self, rect,type):
        self.__rect = rect
        self.__type = type;
        self.__visible = False #visible to player
        self.__revealed = False #explored by player
   
    @property
    def rect(self):
        return self.__rect

    @rect.setter
    def rect(self, rect):
        self.__rect = rect
    
    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, type):
        self.__type = type
    
    @property
    def visible(self):
        return self.__visible

    @visible.setter
    def visible(self, visible):
        self.__visible = visible
    
    @property
    def revealed(self):
        return self.__revealed

    @revealed.setter
    def revealed(self, revealed):
        self.__revealed = revealed

    def drawTile(self, screen):
        screen.draw.rect(screen, black,rect)

class Dungeon():
    tileSize = 48
    mapWidth = 50
    mapHeight = 50
    mapRenderWidth= 16 #technically 16.67
    mapRenderHeight = 16
    mapRenderX = ((800-(mapRenderWidth*tileSize))/2) #offsets for map rendering because tiles don't fit exactly
    mapRenderY = ((800-(mapRenderHeight*tileSize))/2)
    holeTile = 0
    groundTile = 1
    wallTile = 2
    maxTiles = 200
    def __init__(self):
        self.__map = [mapWidth][mapHeight]
        self.__camera = cameraRect

    @property
    def map(self):
        return self.__map

    @map.setter
    def map(self, map):
        self.__map = map

    def loadTiles():
        holeTileImage = pygame.image.load("/images/holeTile.png")
        darkTileImage = pygame.image.load("/images/darkTile.png")
        wallTileImage = pygame.image.load("/images/wallTile.png")
        groundTileImage = pygame.image.load("/images/groundTile.png")
        tileImages = {0:holeTileImage,1:groundTileImage,2:wallTileImage}
    def drawMap(screen,cameraRect):
        mx = 0
        my = 0
        #iterates and draws tiles in accordance with camera position
        for x in range(0,mapRenderWidth):
            for y in range(0,mapRenderHeight):
                mx = x + camera.x
                my = y + camera.y
                if mx >=0 && my>=0 &&mx<mapWidth&&mx<mapHeight:
                    tile = map[mx][my]
                    if tile.revealed == True:
                        if tile.type!=0:
                            screen.blit(tileImages[tile.type],x*tileSize+mapRenderX,y*tileSize+mapRenderY)
                    elif tile.revealed == False:
                        screen.blit(darkTileImage,x*tileSize+mapRenderX,y*tileSize+mapRenderY)
    def generateMap():
        tidyWalls(randomWalk())

    def randomWalk():
        coverage = 20 + random.randint(0,16)  #percentage of map to be covered with tiles
        n = (mapWidth*mapHeight) * (coverage *0.01) # coverage converted to actual tile number
        for x in range(0,mapWidth):
            for y in range(0,mapHeight):
                map[x][y] = Tile(Rect(x,y,tileSize,tileSize),wallTile)
        x = random.randint(1,mapWidth-1)
        y = random.randint(1,mapHeight-1)
        dx = dy = straight = 0
        map[x][y].type=groundTile
        while n > 0:
            straight = max(straight-1,0) #makes tunnels
            if straight == 0:
                direction = random.randint(0,4)
                if direction == 0:
                    dx = 0
                    dy = -1
                elif direction == 1:
                    dx = 0
                    dy = 1
                elif direction == 2:
                    dx = -1
                    dy = 0
                elif direction == 3:
                    dx = 0
                    dy = 0
                elif direction == 4:
                    straight = 4 + random.randint(0,7)
            x = min(max(x+dx,1),mapWidth-2)
            y = min(max(y+dy,1),mapHeight-2)
            if map[x][y].type==wallTile:
                map[x][y].type = groundTile
                n-=1
        return [x,y]
    def tidyWalls(spawnCoords):
        while True: # do while loop using python
            tmp = [row[:] for row in map] #copies map without pointing to map, so i can change tmp without changing map
            for x in range(1,mapWidth):
                for y in range(1, mapHeight):
                    if map[x][y].type == wallTile and countWalls(x,y)<2:
                        wallsRemoved =1
                        tmp[x][y] = groundTile
            map = [row[:] for row in tmp]
            if wallsRemoved == 0:
                
        return spawnCoords
    def countWalls(mx,my): #counts wall tiles next to current tile to see if it's isolated
        for x in range(-1,2):
            for y in range(-1,2):
                if (x!=0 or y!=0) && map[mx+x][my+y].type == wallTile:
                    n++
        return n
        
