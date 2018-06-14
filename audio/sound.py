# imports

import pygame
from pygame import mixer

import time


# init(frequency, size, stereo, buffer)

mixer.init(44100)


# music function

def music(file, volume=1, loop=1):

    pygame.mixer.music.load(file)

    pygame.mixer.music.set_volume(volume)

    if loop:
        pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.play()


# sound function

def sound(file, volume=1):
    loaded_sound = pygame.mixer.Sound(file)

    loaded_sound.set_volume(volume)
    loaded_sound.play()


# testing

def run():
    sound('Gun shot 1.ogg')

    time.sleep(2)
    music('wander.ogg', 0.5, True)

    time.sleep(5)
    sound('Gun shot 1.ogg')
    sound('Gun shot 1.ogg')


run()

time.sleep(600)


