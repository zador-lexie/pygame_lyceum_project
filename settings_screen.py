import pygame
import sys
import os
from main_functions import load_image, terminate, FPS, size, WIDTH, HEIGHT, clock, screen


def settings(window=None):
    fon = pygame.transform.scale(load_image('settings.png'),
                                 (WIDTH, HEIGHT))
    back_btn = pygame.transform.scale(load_image('back_button.png'), (74, 74))
    screen.blit(fon, (0, 0))
    screen.blit(back_btn, (WIDTH - 1010, 10))

    text = pygame.font.Font('data/Kavoon-Regular.ttf', 48)
    text_r = text.render('100', True, (0, 0, 0))
    # plus = pygame.transform.scale(load_image('plus.png'),
    #                               (80, 80))
    # minus = pygame.transform.scale(load_image('minus.png'),
    #                               (113, 37))
    # screen.blit(plus, (150, 100))
    # screen.blit(minus, (350, 120))
    # screen.blit(text_r, (250, 100))


    running = True
    volume = 1.0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                coord = pygame.mouse.get_pos()
                if (350, 200) <= coord <= (420, 280):
                    if volume < 1:
                        volume += 0.1
                if (550, 225) <= coord <= (630, 305):
                    if volume > 0:
                        volume -= 0.1
                if (event.pos[0] - 55) ** 2 + (event.pos[1] - 47) ** 2 <= 37 ** 2:
                    return

                volume = round(volume, 1)
        fon = pygame.transform.scale(load_image('settings.png'),
                                     (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        card = pygame.transform.scale(load_image('settings_card.png'),
                                     (660, 460))
        card.set_alpha(200)
        screen.blit(card, (200, 80))
        text = pygame.font.Font('data/Kavoon-Regular.ttf', 48)
        text_r = text.render(f'{int(volume * 100)}', True, (0, 0, 0))
        text_2_r = text.render('music volume', True, (5, 28, 31))
        back_btn = pygame.transform.scale(load_image('back_button.png'), (74, 74))
        pygame.mixer.music.set_volume(volume)
        clock = pygame.time.Clock()
        running = True
        plus = pygame.transform.scale(load_image('plus.png'),
                                      (80, 80))
        screen.blit(plus, (350, 200))
        screen.blit(back_btn, (WIDTH - 1010, 10))
        minus = pygame.transform.scale(load_image('minus.png'),
                                       (80, 30))
        screen.blit(minus, (550, 225))
        screen.blit(text_r, (450, 210))
        screen.blit(text_2_r, (350, 100))

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    settings()
    pygame.quit()
