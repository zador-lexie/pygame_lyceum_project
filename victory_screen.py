import pygame
import sys
import os
import random
from main_functions import load_image, terminate, FPS, size, WIDTH, HEIGHT, clock, screen


def victory(stars_count):
    fon = pygame.transform.scale(load_image('victory.jpg'),
                                 (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))

    card = pygame.transform.scale(load_image('settings_card.png'),
                                  (660, 460))
    card.set_alpha(200)
    screen.blit(card, (150, 80))

    text = pygame.font.Font('fonts/Kavoon-Regular.ttf', 64)
    text_r = text.render('Victory!', True, (0, 0, 0))
    screen.blit(text_r, (350, 120))

    if stars_count >= 1:
        first_star = pygame.transform.scale(load_image('star.png'), (150, 150))
        screen.blit(first_star, (200, 234))
    if stars_count >= 2:
        second_star = pygame.transform.scale(load_image('star.png'), (150, 150))
        screen.blit(second_star, (400, 234))
    if stars_count == 3:
        third_star = pygame.transform.scale(load_image('star.png'), (150, 150))
        screen.blit(third_star, (600, 234))

    exit_btn = pygame.transform.scale(load_image('exit_button.png'), (120, 120))
    screen.blit(exit_btn, (410, 400))
    #
    # restart_btn = pygame.transform.scale(load_image('restart_btn.png'), (170, 170))
    # screen.blit(restart_btn, (630, 284))

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # if (event.pos[0] - 470) ** 2 + (event.pos[1] - 460) ** 2 <= 60 ** 2:
                #     show_levels()
                exit()

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    pygame.init()
    victory(3)
    pygame.quit()
