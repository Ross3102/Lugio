import pygame
from pygame.locals import *
from spritesheet import spritesheet
from colors import *
from math import sqrt

class Character(pygame.sprite.Sprite):
    def __init__(self, filename, text_sound, screen, x, y):
        super(Character, self).__init__()

        self.text_sound = text_sound
        self.screen = screen

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
        self.rect.x = x
        self.rect.y = y

    def update(self, dx, dy):
        self.rect.x -= dx
        self.rect.y -= dy
        self.update_rects()

    def update_rects(self):
        self.collide_rect = self.rect.copy()
        self.collide_rect.y += self.collide_rect.height * 3 / 4
        self.collide_rect.height /= 4

        self.interact_rect = Rect(0, 0, 1, 1)
        x = self.rect.x
        y = self.rect.y
        if self.direction == self.UP:
            x += 17
            y -= 5
        elif self.direction == self.DOWN:
            x += 17
            y += 55
        elif self.direction == self.LEFT:
            x -= 5
            y += 25
        elif self.direction == self.RIGHT:
            x += 39
            y += 25
        self.interact_rect.x = x
        self.interact_rect.y = y

    def say(self, message, wait=0):
        font_size = 40
        font = pygame.font.SysFont("Courier New", font_size)
        text_width, text_height = font.size(message)
        x_offset = -(text_width - self.rect.width) / 2
        y_offset = -5
        buffer = 2

        points = (
            (self.rect.x + x_offset, self.rect.y - (text_height + buffer) + y_offset),
            (self.rect.x + text_width + x_offset + buffer, self.rect.y - (text_height + buffer) + y_offset),
            (self.rect.x + text_width + x_offset + buffer, self.rect.y + y_offset),
            (self.rect.x + self.rect.width * 3 / 4, self.rect.y + y_offset),
            (self.rect.x + self.rect.width * 2 / 4, self.rect.y),
            (self.rect.x + self.rect.width * 1 / 4, self.rect.y + y_offset),
            (self.rect.x + x_offset, self.rect.y + y_offset)
        )

        pygame.draw.polygon(self.screen, WHITE, points)
        pygame.draw.polygon(self.screen, BLACK, points, buffer)

        skip = False
        self.text_sound.play(-1)
        for i in range(len(message)):
            text = font.render(message[:i + 1], False, BLACK)
            self.screen.blit(text, [self.rect.x + x_offset + buffer, self.rect.y - text_height + y_offset + buffer])
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_SPACE:
                    text = font.render(message, False, BLACK)
                    self.screen.blit(text,
                                     [self.rect.x + x_offset + buffer, self.rect.y - text_height + y_offset + buffer])
                    skip = True
            pygame.display.flip()
            if skip:
                break
            pygame.time.delay(50)
        self.text_sound.stop()

        nxt = False
        while not nxt:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return True
                elif event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        nxt = True
        pygame.time.delay(wait)
        return False


class Player(Character):
    def interact(self, all_sprites):
        for i in all_sprites:
            r = i.rect
            if self.interact_rect.colliderect(r):
                try:
                    i.say("Hello", 100)
                except:
                    pass

    def handle_keys(self, all_sprites):
        self.moving = False
        self.dx = 0
        self.dy = 0

        keys = pygame.key.get_pressed()
        if keys[K_UP]:
            self.direction = self.UP
            self.dy = -5
            self.moving = True
        if keys[K_DOWN]:
            self.direction = self.DOWN
            self.dy = 5
            self.moving = True
        if keys[K_LEFT]:
            self.direction = self.LEFT
            self.dx = -5
            self.moving = True
        if keys[K_RIGHT]:
            self.direction = self.RIGHT
            self.dx = 5
            self.moving = True
        if keys[K_SPACE]:
            self.interact(all_sprites)

    def check_collide(self, all_sprites, collide_sprites):
        rect_list = []
        for i in collide_sprites:
            if hasattr(i, "collide_rect"):
                rect_list.append(i.collide_rect)
            else:
                rect_list.append(i.rect)

        if self.collide_rect.collidelist(rect_list) != -1:
            for block in all_sprites:
                block.rect.x += self.dx
            if self.collide_rect.collidelist(rect_list) != -1:
                for block in all_sprites:
                    block.rect.x -= self.dx
                    block.rect.y += self.dy
                if self.collide_rect.collidelist(rect_list) != -1:
                    for block in all_sprites:
                        block.rect.x += self.dx

    def update(self):
        if self.dx != 0 and self.dy != 0:
            self.dx = round(self.dx / sqrt(2))
            self.dy = round(self.dy / sqrt(2))
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
        self.update_rects()