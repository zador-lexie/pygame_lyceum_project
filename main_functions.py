import pygame
import sys
import os


FPS = 40
size = WIDTH, HEIGHT = 1028, 600
screen = pygame.display.set_mode(size)
screen.fill((1, 15, 30))
clock = pygame.time.Clock()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def terminate():
    pygame.quit()
    sys.exit()
