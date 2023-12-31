import pygame
import sys
import os


def load_image(name, colorkey=None):
    fullname = name
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def terminate():
    pygame.quit()
    sys.exit()


def menu_with_levels():
    text = pygame.font.Font('fonts/Kavoon-Regular.ttf', 64)
    text_2 = pygame.font.Font('fonts/Kavoon-Regular.ttf', 100)
    text_r = text.render('Mr.Kriron', True, (0, 0, 0))
    text_2_r = text_2.render('Reborn', True, (0, 0, 0))
    screen.blit(text_r, (350, 25))
    screen.blit(text_2_r, (330, 200))
    fon = pygame.transform.scale(load_image('data/a-title-for-game-about-nature-in-light-colours (1) 1 (3).png'), (WIDTH, HEIGHT))
    fon_1 = pygame.transform.scale(load_image('data/yellow_rect.png'), (300, 400))
    screen.blit(text_r, (500, 300))
    screen.blit(text_2_r, (100, 100))
    screen.blit(fon, (0, 0))
    screen.blit(fon_1, (114, 100))
    screen.blit(fon_1, (600, 100))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            # elif event.type == pygame.MOUSEBUTTONDOWN:
            #     screen.fill((0, 0, 0))
            #     pygame.display.flip()
            #     running = False
            #     break
        pygame.display.flip()
        clock.tick(FPS)


def title_with_button():
    fon = pygame.transform.scale(load_image('data/a-title-for-game-about-nature-in-light-colours (1) 1 (3).png'),
                                 (WIDTH, HEIGHT))
    btn = pygame.transform.scale(load_image('data/btn_play (1).png'), (100, 100))
    screen.blit(fon, (0, 0))
    text = pygame.font.Font('fonts/Kavoon-Regular.ttf', 64)
    text_2 = pygame.font.Font('fonts/Kavoon-Regular.ttf', 100)
    text_r = text.render('Mr.Kriron', True, (0, 0, 0))
    text_2_r = text_2.render('Reborn', True, (0, 0, 0))
    screen.blit(text_r, (350, 25))
    screen.blit(text_2_r, (330, 200))
    screen.blit(btn, (445, 400))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                btn_rect = pygame.Rect(445, 400, 100, 100)
                if btn_rect.collidepoint(x, y):
                    running = False
                    menu_with_levels()
                    break
        pygame.display.flip()
        clock.tick(FPS)


def start_screen():
    screen.fill((1, 15, 30))
    fon = pygame.transform.scale(load_image('data/an-icon-with-the-letters-a-and-a 1.png'), (400, 400))
    txt = pygame.font.SysFont('times new roman', 30, True)
    txt_continue = txt.render('press any key to continue', False, (0, 255, 194))
    screen.blit(txt_continue, (350, 515))
    screen.blit(fon, (310, 125))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type in [pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN]:
                screen.fill((0, 0, 0))
                pygame.display.flip()
                running = False
                title_with_button()
        pygame.display.flip()
        clock.tick(FPS)




if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    FPS = 50
    size = WIDTH, HEIGHT = 1028, 600
    screen = pygame.display.set_mode(size)
    screen.fill((1, 15, 30))
    clock = pygame.time.Clock()
    start_screen()

    pygame.quit()
