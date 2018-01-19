from random import randint

import pygame

from character import Character
from colors import *
from room import Room, RandomRoom
from rooms import room_layouts


def drawFrame():
    screen.fill(BLACK)  # DIRT_BROWN

    character.update()
    room.update(ch.dx, ch.dy)

    ch.check_collide(room)

    room.draw(screen)
    character.draw(screen)

    pygame.display.flip()
    return False


def sayThings(character, messages, wait):
    text_sound = pygame.mixer.Sound(TEXT_SOUND_FILE)
    text_sound.set_volume(0.25)
    for message in messages:
        if character.say(message, text_sound):
            return True
        drawFrame()
        pygame.event.pump()
        pygame.time.delay(wait)
    return False

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

character = pygame.sprite.Group()
ch = Character(CHARACTER_SHEET, screen)
character.add(ch)

rand = False

if rand:
    room = RandomRoom(ROOM_SHEET, BLOCKS_ACROSS, BLOCKS_HIGH)
else:
    room = Room(ROOM_SHEET, room_layouts.start)

done = False
gameStart = True

while not done:
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True

    ch.handle_keys()
    drawFrame()

    if gameStart and sayThings(ch, ["Welcome to the GameWelcome to the GameWelcome to the GameWelcome to the GameWelcome to the GameWelcome to the GameWelcome to the GameWelcome to the GameWelcome to the GameWelcome to the GameWelcome to the GameWelcome to the GameWelcome to the Game", "Hope you have fun!"], 200):
        done = True
    gameStart = False

    clock.tick(FPS)


pygame.quit()
quit()
# Test
