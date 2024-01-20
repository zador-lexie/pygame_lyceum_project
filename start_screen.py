import pygame
import sys
import os
from main_functions import load_image, terminate, FPS, size, WIDTH, HEIGHT, clock, screen
from settings_screen import settings
from levels_screen import show_levels


def start():
    fon = pygame.transform.scale(load_image('a-title-for-game-about-nature-in-light-colours (1) 1 (3).png'),
                                 (WIDTH, HEIGHT))
    btn = pygame.transform.scale(load_image('btn_play.png'), (120, 120))   # изм!!!
    settings_btn = pygame.transform.scale(load_image('btn_settings.png'), (74, 74))
    screen.blit(fon, (0, 0))
    text = pygame.font.Font('data/Kavoon-Regular.ttf', 64)
    text_2 = pygame.font.Font('data/Kavoon-Regular.ttf', 100)
    text_r = text.render('Mr.Kriron', True, (5, 28, 31))
    text_2_r = text_2.render('Reborn', True, (5, 28, 31))
    screen.blit(text_r, (350, 25))
    screen.blit(text_2_r, (330, 200))
    screen.blit(btn, (445, 400))
    screen.blit(settings_btn, (WIDTH - 100, 10))
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # переменная!!
                # (x - x0)^2 + (y - y0)^2 <= R^2  (проверка что координата пропадает в окружность по Пифагору)
                if (event.pos[0] - 505) ** 2 + (event.pos[1] - 460) ** 2 <= 60 ** 2:
                    screen.fill((0, 0, 0))
                    pygame.display.flip()
                    running = False
                    show_levels()

                if (event.pos[0] - 965) ** 2 + (event.pos[1] - 47) ** 2 <= 37 ** 2:
                    settings('start')
                    start()
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    start()
    pygame.quit() 
