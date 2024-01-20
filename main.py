import pygame
import sys
import os
from main_functions import load_image, terminate, FPS, size, WIDTH, HEIGHT, clock, screen
from screensaver_screen import screensaver
from start_screen import start


if __name__ == '__main__':
    pygame.init()
    pygame.mixer.music.load('data/i_fell_in_love.mp3')
    screensaver()
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(1)
    start()
    pygame.quit()
