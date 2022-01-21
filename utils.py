import pygame
import random
import json
import pickle
from typing import Any, List, Union, cast

def create_empty_map(width: int, height: int) -> List[List[None]]:
    __map: List[List[None]] = []
    for x in range(width):
        __map.append([])
        for _ in range(height):
            __map[x].append(None)
    return __map


class Rect:
    def __init__(self, x: float, y: float, width: int, height: int):
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height
        self.__pyg_rect: Union[None, pygame.Rect] = pygame.Rect(
            int(self.__x), int(self.__y), self.__width, self.__height
        )

    def __str__(self) -> str:
        return "x: {} y: {} width: {} height: {}".format(
            self.__x, self.__y, self.__width, self.__height
        )

    @property
    def x(self) -> float:
        return self.__x

    @x.setter
    def x(self, x: float) -> None:
        self.__x = float(x)
        cast(pygame.Rect, self.__pyg_rect).x = int(self.__x)

    @property
    def pyg_rect(self) -> Union[pygame.Rect, None]:
        return self.__pyg_rect
    
    @pyg_rect.deleter
    def pyg_rect(self) -> None:
        self.__pyg_rect = None


    @property
    def y(self) -> float:
        return self.__y

    @y.setter
    def y(self, y: float) -> None:
        self.__y = float(y)
        cast(pygame.Rect, self.__pyg_rect).y = int(self.__y)

    @property
    def width(self) -> int:
        return self.__width

    @property
    def height(self) -> int:
        return self.__height

    def colliderect(self, other: Any, adjustment: float = 0) -> bool:
        x = other.x + adjustment
        y = other.y + adjustment
        width = other.width - adjustment * 2
        height = other.height - adjustment * 2
        if (
            self.x + self.width > x
            and x + width > self.x
            and self.y + self.height > y
            and y + height > self.y
        ):
            return True
        else:
            return False


    # returns shared rect space between two rects
    def rectintersection(self, other: "Rect") -> "Rect":
        x5 = max(self.x, other.x)
        x6 = min(self.x + self.width, other.x + other.width)
        y5 = max(self.y, other.y)
        y6 = min(self.y + self.height, other.y + other.height)
        if x5 > x6 or y5 > y6:
            return Rect(0, 0, 0, 0)
        return Rect(x5, y5, x6 - x5, y6 - y5)


class Player:
    def __init__(self, rect: pygame.Rect, image: pygame.Surface):
        self.__rect = rect
        self.__image = image

    @property
    def rect(self) -> pygame.Rect:
        return self.__rect

    @rect.setter
    def rect(self, rect: pygame.Rect) -> None:
        self.__rect = rect

    @property
    def image(self) -> pygame.Surface:
        return self.__image

    @image.setter
    def image(self, image: pygame.Surface) -> None:
        self.__image = image


class Tile:
    def __init__(self, rect: Rect, type: int):
        self.__rect = rect
        self.__type = type
        self.__visible = False  # visible to player
        self.__revealed = False  # explored by player

    @property
    def rect(self) -> Rect:
        return self.__rect

    @rect.setter
    def rect(self, rect: Rect) -> None:
        self.__rect = rect

    @property
    def type(self) -> int:
        return self.__type

    @type.setter
    def type(self, type: int) -> None:
        self.__type = type

    @property
    def visible(self) -> bool:
        return self.__visible

    @visible.setter
    def visible(self, visible: bool) -> None:
        self.__visible = visible

    @property
    def revealed(self) -> bool:
        return self.__revealed

    @revealed.setter
    def revealed(self, revealed: bool) -> None:
        self.__revealed = revealed

    def drawTile(self, screen: pygame.Surface) -> None:
        screen.draw.rect(screen, self.visible, self.rect)

class RoomsJSON(json.JSONEncoder, json.JSONDecoder):
    def __init__(self) -> RoomsJSON:
        self.object_hook = self.__object_hook
        json.JSONEncoder.__init__(self)
        json.JSONDecoder.__init__(self)

    def default(self, obj) -> Union(dict[str, Any], Any):
        if isinstance(obj, Rect) or isinstance(obj, Tile):
            print("omg hi")
            obj_dict = obj.__dict__
            if isinstance(obj, Tile):
                del obj_dict["_Tile__rect"].pyg_rect
            return obj_dict
        return json.JSONEncoder.default(self, obj)

    def __object_hook(self, obj):
        if "__class__" in obj:
            if obj["__class__"] == Rect:
                return Rect(obj["x"], obj["y"], obj["width"], obj["height"])
            elif obj["__class__"] == Tile:
                return Tile(obj["rect"], obj["type"])
            
        return obj
    

class Dungeon:
    tileSize = 48
    mapWidth = 50
    mapHeight = 50
    mapRenderWidth = 16  # technically 16.67
    mapRenderHeight = 16
    mapRenderX = (
        800 - (mapRenderWidth * tileSize)
    ) / 2  # offsets for map rendering because tiles don't fit exactly
    mapRenderY = (800 - (mapRenderHeight * tileSize)) / 2
    holeTile = 0
    groundTile = 1
    wallTile = 2
    maxTiles = 200

    def __init__(self):
        self.map = create_empty_map(self.mapWidth, self.mapHeight)
        # self.__camera = cameraRect  # don't know what this line is supposed to be

    @property
    def map(self):
        return self.__map

    @map.setter
    def map(self, map):
        self.__map = map

    def loadTiles(self):
        holeTileImage = pygame.image.load("/images/holeTile.png")
        darkTileImage = pygame.image.load("/images/darkTile.png")
        wallTileImage = pygame.image.load("/images/wallTile.png")
        groundTileImage = pygame.image.load("/images/groundTile.png")
        self.tileImages = {0: holeTileImage, 1: groundTileImage, 2: wallTileImage}

    def drawMap(self, screen, cameraRect):
        mx = 0
        my = 0
        # iterates and draws tiles in accordance with camera position
        for x in range(0, self.mapRenderWidth):
            for y in range(0, self.mapRenderHeight):
                mx = x + self.__camera.x
                my = y + self.__camera.y
                if mx >= 0 and my >= 0 and mx < self.mapWidth and mx < self.mapHeight:
                    tile = self.map[mx][my]
                    if tile.revealed == True:
                        if tile.type != 0:
                            screen.blit(
                                self.tileImages[tile.type],
                                x * self.tileSize + self.mapRenderX,
                                y * self.tileSize + self.mapRenderY,
                            )
                    elif tile.revealed == False:
                        screen.blit(
                            self.darkTileImage,
                            x * self.tileSize + self.mapRenderX,
                            y * self.tileSize + self.mapRenderY,
                        )

    def generateMap(self):
        self.tidyWalls(self.randomWalk())

    def randomWalk(self):
        coverage = 20 + random.randint(
            0, 16
        )  # percentage of map to be covered with tiles
        n = (self.mapWidth * self.mapHeight) * (
            coverage * 0.01
        )  # coverage converted to actual tile number
        for x in range(0, self.mapWidth):
            for y in range(0, self.mapHeight):

                self.map[x][y] = Tile(
                    Rect(x, y, self.tileSize, self.tileSize), self.wallTile
                )
        x = random.randint(1, self.mapWidth - 1)
        y = random.randint(1, self.mapHeight - 1)
        dx = dy = straight = 0
        self.map[x][y].type = Tile(
            Rect(x, y, self.tileSize, self.tileSize), self.groundTile
        )
        while n > 0:
            straight = max(straight - 1, 0)  # makes tunnels
            if straight == 0:
                direction = random.randint(0, 4)
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
                    straight = 4 + random.randint(0, 7)
            x = min(max(x + dx, 1), self.mapWidth - 2)
            y = min(max(y + dy, 1), self.mapHeight - 2)
            if self.map[x][y].type == self.wallTile:
                self.map[x][y].type = self.groundTile
                n -= 1
        return [x, y]

    def tidyWalls(self, spawnCoords):
        while True:  # do while loop using python
            tmp = [
                row[:] for row in map
            ]  # copies map without pointing to map, so i can change tmp without changing map
            for x in range(1, self.mapWidth):
                for y in range(1, self.mapHeight):
                    if map[x][y].type == self.wallTile and self.countWalls(x, y) < 2:
                        wallsRemoved = 1
                        tmp[x][y] = self.groundTile
            map = [row[:] for row in tmp]
            if wallsRemoved == 0:
                break

        return spawnCoords

    def countWalls(
        self, mx, my
    ):  # counts wall tiles next to current tile to see if it's isolated
        n = 0
        for x in range(-1, 2):
            for y in range(-1, 2):
                if (x != 0 or y != 0) and self.map[mx + x][
                    my + y
                ].type == self.wallTile:
                    n += 1
        return n
