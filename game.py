from random import randint

import pygame

from character import Player, Character
from colors import *
from room import Room, RandomRoom
from rooms import room_layouts


def draw_frame():
    screen.fill(BLACK)  # DIRT_BROWN

    player.update()
    room.update(ch.dx, ch.dy)
    npcs.update(ch.dx, ch.dy)

    ch.check_collide(all_sprites, collision_sprites)

    room.draw(screen)

    behind = pygame.sprite.Group()
    front = pygame.sprite.Group()

    for npc in npcs:
        if npc.rect.y < ch.rect.y:
            behind.add(npc)
        else:
            front.add(npc)

    behind.draw(screen)
    player.draw(screen)
    front.draw(screen)

    pygame.display.flip()


def say_things(character, messages, wait):
    for message in messages:
        if character.say(message):
            return True
        draw_frame()
        pygame.event.pump()
        pygame.time.delay(wait)
    return False


def game_loop():
    done = False
    gameStart = True

    while not done:
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True

        ch.handle_keys(all_sprites)
        draw_frame()

        if gameStart and say_things(ch, ["Welcome To The Game", "Hope You Have Fun!"], 200):
            done = True
        gameStart = False

        clock.tick(FPS)

GAME_TITLE = "Lugio"

BLOCK_SIZE = 64

BLOCKS_ACROSS = 10
BLOCKS_HIGH = 10

DISPLAY_WIDTH = BLOCK_SIZE * BLOCKS_ACROSS
DISPLAY_HEIGHT = BLOCK_SIZE * BLOCKS_HIGH

FPS = 30

SOUNDS_DIR = "sounds"
SHEETS_DIR = "spritesheets"

TEXT_SOUND_FILE = SOUNDS_DIR + "/text_sound.wav"
CHARACTER_SHEET = SHEETS_DIR + "/character-spritesheet.png"
ROOM_SHEET = SHEETS_DIR + "/blocks.gif"

pygame.init()

screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption(GAME_TITLE)
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
collision_sprites = pygame.sprite.Group()
npcs = pygame.sprite.Group()

text_sound = pygame.mixer.Sound(TEXT_SOUND_FILE)
text_sound.set_volume(0.25)
player= pygame.sprite.Group()
ch = Player(CHARACTER_SHEET, text_sound, screen, 288, 288)
player.add(ch)

rand = False

if rand:
    room = RandomRoom(ROOM_SHEET, BLOCKS_ACROSS, BLOCKS_HIGH)
else:
    room = Room(ROOM_SHEET, room_layouts.start)

[all_sprites.add(i) for i in room]
[collision_sprites.add(i) for i in room.walls]

npc1 = Character(CHARACTER_SHEET, text_sound, screen, 180, 240)
npcs.add(npc1)
all_sprites.add(npc1)
collision_sprites.add(npc1)

game_loop()
pygame.quit()
quit()
