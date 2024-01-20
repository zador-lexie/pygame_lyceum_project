import pygame
import sys
import os
import random
from main_functions import load_image, terminate, FPS, size, WIDTH, HEIGHT, clock, screen


def game_over():
    fon = pygame.transform.scale(load_image('game_over.png'),
                                 (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))

    text = pygame.font.Font('fonts/Kavoon-Regular.ttf', 64)
    text_r = text.render('Game Over', True, (255, 255, 255))
    screen.blit(text_r, (320, 150))

    exit_btn = pygame.transform.scale(load_image('exit_button.png'), (170, 170))
    screen.blit(exit_btn, (170, 284))

    restart_btn = pygame.transform.scale(load_image('restart_btn.png'), (170, 170))
    screen.blit(restart_btn, (630, 284))

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if (event.pos[0] - 715) ** 2 + (event.pos[1] - 369) ** 2 <= 85 ** 2:
                    return
                elif (event.pos[0] - 255) ** 2 + (event.pos[1] - 369) ** 2 <= 85 ** 2:
                    exit()

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    pygame.init()
    game_over()
    pygame.quit()
