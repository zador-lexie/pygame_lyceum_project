import pygame
import sys
import os
from main_functions import load_image, terminate, FPS, size, WIDTH, HEIGHT, clock, screen
from settings_screen import settings
from level1 import level_1
from level2 import level_2

def show_levels():
    pred = pygame.transform.scale(load_image('predislovie.png'),
                                 (690, 60))
    pred.set_alpha(200)

    settings_btn = pygame.transform.scale(load_image('btn_settings.png'), (74, 74))

    back_btn = pygame.transform.scale(load_image('back_button.png'), (74, 74))

    btn_pressed = pygame.transform.scale(load_image('btn_lvl.png'),
                                 (75, 75))
    btn_not_pressed = pygame.transform.scale(load_image('btn_lvl_not.png'),
                                 (70, 70))
    fon = pygame.transform.scale(load_image('settings.png'),
                                 (WIDTH, HEIGHT))
    first_list_card = pygame.transform.scale(load_image('lvl_1.png'),
                                 (280, 380))
    first_list_card.set_alpha(230)

    second_list_card = pygame.transform.scale(load_image('lvl_2.png'),
                                             (280, 380))
    second_list_card.set_alpha(230)

    third_list_card = pygame.transform.scale(load_image('lvl_3.png'),
                                              (280, 380))
    third_list_card.set_alpha(230)

    text = pygame.font.Font('data/Kavoon-Regular.ttf', 48)
    text_2 = pygame.font.Font('data/Kavoon-Regular.ttf', 32)
    text_3 = pygame.font.Font('data/Kavoon-Regular.ttf', 15)
    text_r = text.render('Part 1', True, (0, 0, 0))
    text_2_r = text_2.render('Rethinking', True, (0, 0, 0))
    text_3_r = text_3.render('The level in development', True, (0, 0, 0))
    text_4_r = text_3.render("Oh, visibly, he isn't human", True, (0, 0, 0))
    text_5_r = text_3.render("anymore..", True, (0, 0, 0))
    text_6_r = text_3.render("Squirrel fur is often", True, (0, 0, 0))
    text_7_r = text_3.render("turned into clothing.", True, (0, 0, 0))


    screen.blit(fon, (0, 0))
    screen.blit(pred, (160, 510))
    screen.blit(settings_btn, (WIDTH - 100, 10))
    screen.blit(first_list_card, (40, 120))
    screen.blit(second_list_card, (358, 120))
    screen.blit(third_list_card, (676, 120))
    screen.blit(btn_pressed, (143, 330))
    screen.blit(btn_pressed, (461, 330))
    screen.blit(btn_not_pressed, (779, 330))
    screen.blit(text_r, (430, 25))
    screen.blit(text_2_r, (410, 80))
    screen.blit(text_3_r, (730, 250))
    screen.blit(text_4_r, (80, 250))
    screen.blit(text_5_r, (130, 280))
    screen.blit(text_6_r, (420, 250))
    screen.blit(text_7_r, (420, 280))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if (event.pos[0] - 965) ** 2 + (event.pos[1] - 47) ** 2 <= 37 ** 2:
                    settings()
                    show_levels()
                if (event.pos[0] - 498) ** 2 + (event.pos[1] - 367) ** 2 <= 39 ** 2:
                    pass
                if (event.pos[0] - (143 + 37)) ** 2 + (event.pos[1] - (330 + 37)) ** 2 <= 39 ** 2:
                    level_1()
                if (event.pos[0] - (461 + 37)) ** 2 + (event.pos[1] - (330 + 37)) ** 2 <= 39 ** 2:
                    level_2()

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    pygame.init()
    show_levels()
    pygame.quit()
