import pygame
import sys
import os
from main_functions import load_image, terminate, FPS, size, WIDTH, HEIGHT, clock, screen


def show_levels():
    fon = pygame.transform.scale(load_image('settings.png'),
                                 (WIDTH, HEIGHT))
    text = pygame.font.Font('data/Kavoon-Regular.ttf', 48)
    text_2 = pygame.font.Font('data/Kavoon-Regular.ttf', 32)
    text_r = text.render('Part 1', True, (0, 0, 0))
    text_2_r = text_2.render('Rethinking', True, (0, 0, 0))
    screen.blit(fon, (0, 0))
    screen.blit(text_r, (430, 25))
    screen.blit(text_2_r, (410, 80))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                screen.fill((0, 0, 0))
                pygame.display.flip()
                running = False
                break
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    pygame.init()
    show_levels()
    pygame.quit()
