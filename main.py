import pygame
import sys
import os
from main_functions import load_image, terminate, FPS, size, WIDTH, HEIGHT, clock, screen
from screensaver_screen import screensaver
from start_screen import start
from levels_screen import show_levels


if __name__ == '__main__':
    pygame.init()
    screensaver()
    start()
    show_levels()
    pygame.quit()
