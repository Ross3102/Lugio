import pygame
from spritesheet import spritesheet
from random import randint


class Room(pygame.sprite.Group):
    def __init__(self, filename, array):
        super(Room, self).__init__()

        self.sheet = spritesheet(filename)

        self.HORIZ = 0
        self.VERT = 1

        self.DR = 0
        self.DL = 1
        self.UL = 2
        self.UR = 3

        self.LEFT = 0
        self.UP = 1
        self.DOWN = 2
        self.RIGHT = 3

        self.dirt = pygame.transform.scale(self.sheet.image_at((0, 0, 16, 16)), (64, 64))
        self.single = pygame.transform.scale(self.sheet.image_at((16, 0, 16, 16)), (64, 64))
        self.four = pygame.transform.scale(self.sheet.image_at((32, 0, 16, 16)), (64, 64))
        self.straight_wall = [pygame.transform.scale(i, (64, 64)) for i in self.sheet.load_strip((0, 16, 16, 16), 2)]
        self.curved_wall = [pygame.transform.scale(i, (64, 64)) for i in self.sheet.load_strip((0, 32, 16, 16), 4)]
        self.end_wall = [pygame.transform.scale(i, (64, 64)) for i in self.sheet.load_strip((0, 48, 16, 16), 4)]
        self.three_wall = [pygame.transform.scale(i, (64, 64)) for i in self.sheet.load_strip((0, 64, 16, 16), 4)]

        self.walls = pygame.sprite.Group()

        character_coords = [(array[i].index("X")*64, i*64) for i in range(len(array)) if "X" in array[i]][0]

        for y in range(len(array)):
            for x in range(len(array[y])):
                if array[y][x] == " ": continue
                wall = True
                if array[y][x] == "*":
                    above = " " if y == 0 else array[y-1][x]
                    right = " " if x == len(array[y]) - 1 else array[y][x+1]
                    left = " " if x == 0 else array[y][x-1]
                    below = " " if y == len(array) - 1 else array[y+1][x]
                    if left == right == above == below == "*":
                        image = self.four
                    elif left == right == "*":
                        if above == "*":
                            image = self.three_wall[self.UP]
                        elif below == "*":
                            image = self.three_wall[self.DOWN]
                        else:
                            image = self.straight_wall[self.HORIZ]
                    elif above == below == "*":
                        if left == "*":
                            image = self.three_wall[self.LEFT]
                        elif right == "*":
                            image = self.three_wall[self.RIGHT]
                        else:
                            image = self.straight_wall[self.VERT]
                    elif above == left == "*":
                        image = self.curved_wall[self.DR]
                    elif above == right == "*":
                        image = self.curved_wall[self.DL]
                    elif below == left == "*":
                        image = self.curved_wall[self.UR]
                    elif below == right == "*":
                        image = self.curved_wall[self.UL]
                    # elif right + left in ("* ", " *"):
                    #     image = self.straight_wall[self.HORIZ]
                    # elif above + below in ("* ", " *"):
                    #     image = self.straight_wall[self.VERT]
                    elif right == "*":
                        image = self.end_wall[self.LEFT]
                    elif left == "*":
                        image = self.end_wall[self.RIGHT]
                    elif above == "*":
                        image = self.end_wall[self.DOWN]
                    elif below == "*":
                        image = self.end_wall[self.UP]
                    else:
                        image = self.single
                else:
                    image = self.dirt
                    wall = False
                block = Block(x*64 - character_coords[0] + 288, y*64 - character_coords[1] + 288, image)
                if wall:
                    self.walls.add(block)
                self.add(block)


class RandomRoom(Room):
    def __init__(self, filename, width, height):
        array = []
        for i in range(height):
            row = []
            for j in range(width):
                if randint(0, 1) == 0:
                    row.append("*")
                else:
                    row.append(".")
            array.append(row)

        array[randint(0, height-1)][randint(0, height-1)] = "X"
        super(RandomRoom, self).__init__(filename, array)

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super(Block, self).__init__()

        self.image = image

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, dx, dy):
        self.rect.x -= dx
        self.rect.y -= dy