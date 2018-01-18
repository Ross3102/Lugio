import pygame
from pygame.locals import *
from spritesheet import spritesheet
from math import sqrt, pi
import rooms
from random import randint

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TRANSPARENT_BLACK = Color(0, 0, 0, 15)


class Room(pygame.sprite.Group):
    def __init__(self, array, filename):
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


class Character(pygame.sprite.Sprite):
    def __init__(self, filename):
        super(Character, self).__init__()

        self.prev_move = pygame.time.get_ticks()
        self.moving = False
        self.dx = 0
        self.dy = 0

        self.NUM_SPRITES = 4

        self.sheet = spritesheet(filename)

        self.sprites = []

        self.DOWN = 0
        self.LEFT = 1
        self.RIGHT = 2
        self.UP = 3

        HORIZONTAL_SPACE = (15, 15)
        VERTICAL_SPACE = (10, 4)

        for row in range(4):
            self.sprites.append(
                self.sheet.images_at(
                    [(
                         64*i+HORIZONTAL_SPACE[0],
                         64*row+VERTICAL_SPACE[0],
                         64-sum(HORIZONTAL_SPACE),
                         64-sum(VERTICAL_SPACE)
                     ) for i in range(4)],-1)
            )

        self.pos = 0
        self.direction = self.DOWN

        self.image = self.sprites[self.direction][self.pos]

        self.rect = self.image.get_rect()
        self.rect.x = 288
        self.rect.y = 288

    def handle_keys(self):
        self.moving = False
        self.dx = 0
        self.dy = 0

        keys = pygame.key.get_pressed()
        if keys[K_UP]:
            self.direction = ch.UP
            self.dy = -5
            self.moving = True
        if keys[K_DOWN]:
            self.direction = ch.DOWN
            self.dy = 5
            self.moving = True
        if keys[K_LEFT]:
            self.direction = ch.LEFT
            self.dx = -5
            self.moving = True
        if keys[K_RIGHT]:
            self.direction = ch.RIGHT
            self.dx = 5
            self.moving = True

    def update(self):
        if self.dx != 0 and self.dy != 0:
            self.dx = round(self.dx/sqrt(2))
            self.dy = round(self.dy/sqrt(2))
        new_time = pygame.time.get_ticks()
        if self.moving:
            if new_time - self.prev_move >= 150:
                self.prev_move = new_time
                self.pos = (self.pos + 1) % self.NUM_SPRITES
                self.moving = False
        else:
            self.pos = (self.pos + self.pos % 2) % self.NUM_SPRITES
            self.dx = 0
            self.dy = 0
        self.image = self.sprites[self.direction][self.pos]

    def check_collide(self, room):
        self.collide_rect = self.rect.copy()
        self.collide_rect.y += self.collide_rect.height*3/4
        self.collide_rect.height /= 4

        rect_list = [i.rect for i in room.walls]

        if self.collide_rect.collidelist(rect_list) != -1:
            for block in room:
                block.rect.x += self.dx
            if self.collide_rect.collidelist(rect_list) != -1:
                for block in room:
                    block.rect.x -= self.dx
                    block.rect.y += self.dy
                if self.collide_rect.collidelist(rect_list) != -1:
                    for block in room:
                        block.rect.x += self.dx

    def say(self, messages, wait=0):
        ts = pygame.mixer.Sound("mySound.wav")
        for message in messages:
            font_size = 25
            font = pygame.font.SysFont("Courier New", font_size)
            text_width, text_height = font.size(message)
            x_offset = -(text_width-self.rect.width)/2
            y_offset = -5
            buffer = 2

            points = (
                (self.rect.x + x_offset, self.rect.y - (text_height + buffer) + y_offset),
                (self.rect.x + text_width + x_offset + buffer, self.rect.y - (text_height + buffer) + y_offset),
                (self.rect.x + text_width + x_offset + buffer, self.rect.y + y_offset),
                (self.rect.x + self.rect.width*3/4, self.rect.y + y_offset),
                (self.rect.x + self.rect.width*2/4, self.rect.y),
                (self.rect.x + self.rect.width*1/4, self.rect.y + y_offset),
                (self.rect.x + x_offset, self.rect.y + y_offset)
            )

            pygame.draw.polygon(screen, WHITE, points)
            pygame.draw.polygon(screen, BLACK, points, buffer)

            skip = False

            for i in range(len(message)):
                text = font.render(message[:i+1], False, BLACK)
                screen.blit(text, [self.rect.x + x_offset + buffer, self.rect.y - text_height + y_offset + buffer])
                for event in pygame.event.get():
                    if event.type == KEYDOWN and event.key == K_SPACE:
                        text = font.render(message, False, BLACK)
                        screen.blit(text,
                                    [self.rect.x + x_offset + buffer, self.rect.y - text_height + y_offset + buffer])
                        skip = True
                pygame.display.flip()
                ts.play()
                if skip:
                    break
                pygame.time.delay(50)

            nxt = False
            while not nxt:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        return True
                    elif event.type == KEYDOWN:
                        if event.key == K_SPACE:
                            nxt = True
            drawFrame()
            pygame.event.pump()
            pygame.time.delay(wait)
        return False


def drawFrame():
    screen.fill(BLACK)  # (120, 85, 73))

    character.update()
    room.update(ch.dx, ch.dy)

    ch.check_collide(room)

    room.draw(screen)
    character.draw(screen)

    # pygame.draw.rect(screen, (255, 0, 0), ch.collide_rect)

    pygame.display.flip()
    return False

BLOCK_SIZE = 64

DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 640

FPS = 30

pygame.init()

screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), DOUBLEBUF, 32)
clock = pygame.time.Clock()

character = pygame.sprite.Group()
ch = Character("character-spritesheet.png")
character.add(ch)

# Random Room

array = []
for i in range(10):
    row = []
    for j in range(10):
        if randint(0, 1) == 0:
            row.append("*")
        else:
            row.append(".")
    array.append(row)

array[randint(0, 9)][randint(0, 9)] = "X"

# End Random Room

rand = False

room = Room(array if rand else rooms.start, "blocks.gif")

done = False
gameStart = True

while not done:
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True

    ch.handle_keys()
    drawFrame()

    if gameStart and ch.say(["TESTINGTESTINGTESTINGTESTINGTESTINGTESTINGTESTINGTESTINGTESTINGTESTINGTESTINGTESTINGTESTINGTESTING"], 200):
        done = True
    gameStart = False

    clock.tick(FPS)


pygame.quit()
quit()
# Test