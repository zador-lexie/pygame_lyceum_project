import pygame
import sys
import os
from main_functions import load_image, terminate, FPS, size, WIDTH, HEIGHT, clock, screen


def screensaver():
    fon = pygame.transform.scale(load_image('an-icon-with-the-letters-a-and-a 1.png'), (400, 400))
    txt = pygame.font.SysFont('times new roman', 30, True)
    txt_continue = txt.render('press any key to continue', False, (0, 255, 194))
    screen.blit(fon, (310, 125))
    screen.blit(txt_continue, (350, 515))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type in [pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN]:
                screen.fill((0, 0, 0))
                pygame.display.flip()
                running = False
                break
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    screensaver()
    pygame.quit()
