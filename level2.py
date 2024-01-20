import pygame
import sys
import os
import random
from main_functions import load_image, terminate, FPS, size, WIDTH, HEIGHT, clock, screen
from game_over_screen import game_over
from victory_screen import victory
stars = 0

groups = {
    'all_sprites': pygame.sprite.Group(),
    'horizontal_borders': pygame.sprite.Group(),
    'vertical_borders': pygame.sprite.Group(),
    'left_boarders': pygame.sprite.Group(),
    'right_boarders': pygame.sprite.Group(),
    'platforms': pygame.sprite.Group(),
    'top_horizontal': pygame.sprite.Group(),
    'bottom_horizontal': pygame.sprite.Group(),
    'thorns': pygame.sprite.Group(),
    'vines': pygame.sprite.Group()
}


class Stars(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("small_star.png")
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, event):
        global stars
        if pygame.sprite.collide_mask(self, player):
            stars += 1
            self.kill()

class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2, right=False, left=False, top=False, bottom=False):
        super().__init__(groups['all_sprites'])
        if x1 == x2:  # вертикальная стенка
            self.add(groups['vertical_borders'])
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(groups['horizontal_borders'])
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)

        if right:
            self.add(groups['right_boarders'])
        elif left:
            self.add(groups['left_boarders'])
        elif top:
            self.add(groups['top_horizontal'])
        elif bottom:
            self.add(groups['bottom_horizontal'])
    # def __init__(self, boards):
    #     super().__init__(groups['all_sprites'])
    #     board_num = 1
    #     for board in boards:
    #         x1, y1, x2, y2 = board
    #         if x1 == x2:  # вертикальная стенка
    #             self.add(groups['vertical_borders'])
    #             self.image = pygame.Surface([1, y2 - y1])
    #             self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
    #         else:  # горизонтальная стенка
    #             self.add(groups['horizontal_borders'])
    #             self.image = pygame.Surface([x2 - x1, 1])
    #             self.rect = pygame.Rect(x1, y1, x2 - x1, 1)
    #
    #         if board_num == 1:
    #             self.add(groups['top_horizontal'])
    #         elif board_num == 2:
    #             self.add(groups['right_boarders'])
    #         elif board_num == 3:
    #             self.add(groups['bottom_horizontal'])
    #         elif board_num == 2:
    #             self.add(groups['left_boarders'])
    #
    #         board_num += 1


class Platform(pygame.sprite.Sprite):
    def __init__(self, platform_size: tuple, platform_coords: tuple, img: str):
        super().__init__(groups['all_sprites'])
        self.platform_size = platform_size
        self.platform_coords = platform_coords
        self.add(groups['all_sprites'])
        self.add(groups['platforms'])
        self.image = img
        self.rect = pygame.Rect(*platform_coords, *platform_size)

    def platform_board(self):
        do_boarders(self.platform_size, self.platform_coords)


def do_boarders(platform_size: tuple, platform_coords: tuple):
    width, height = platform_size
    p_x, p_y = platform_coords
    # Border(((p_x + 1, p_y, p_x + width - 1, p_y + height),
    #         (p_x + width, p_y + 1, p_x + width, p_y + height - 1),
    #         (p_x + 1, p_y + height, p_x + width - 1, p_y + height),
    #         (p_x, p_y + 1, p_x, p_y + height - 1)))
    Border(p_x + 1, p_y, p_x + width - 1, p_y + height, top=True)
    Border(p_x + width, p_y + 1, p_x + width, p_y + height - 1, left=True)
    Border(p_x + 1, p_y + height, p_x + width - 1, p_y + height, bottom=True)
    Border(p_x, p_y + 1, p_x, p_y + height - 1, right=True)


class Thorns(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(groups['all_sprites'])
        self.image = load_image("thorns_mountain.png")
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)


class Squirrel(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("squirrel.png")
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.is_jump = False
        self.over = False
        self.jump_count = 10
        self.mod_x = 0
        self.move = 0

    def update(self, event):
        keys = pygame.key.get_pressed()
        if type(event) != type(''):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.move = -5
                if event.key == pygame.K_RIGHT:
                    self.move = 5
                if keys[pygame.K_RIGHT] and keys[pygame.K_SPACE]:
                    self.is_jump = True
                    self.mod_x = 5
                if keys[pygame.K_LEFT] and keys[pygame.K_SPACE]:
                    self.is_jump = True
                    self.mod_x = -8

            if keys[pygame.K_SPACE]:
                self.is_jump = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.move = 0
                if event.key == pygame.K_RIGHT:
                    self.move = 0

        # if self.over:
        #     self.rect.x = 155
        #     self.rect.y = HEIGHT - 590
        #     self.add(groups['all_sprites'])
        #     self.over = False

        if self.rect.x > 1020:
            victory(stars)

        if self.is_jump:
            if self.is_jump:
                if self.jump_count >= -10:
                    if self.jump_count >= 0:
                        for i in range(1, (self.jump_count ** 2) // 2 + 1):
                            if not pygame.sprite.spritecollideany(self, groups['bottom_horizontal']):
                                self.rect.y -= 1
                            else:
                                self.is_jump = False
                                self.mod_x = 0
                                self.jump_count = 10
                                self.rect.y += i
                                break

                    elif self.jump_count < 0:
                        for i in range(1, (self.jump_count ** 2) // 2 + 1):
                            if not pygame.sprite.spritecollideany(self, groups['top_horizontal']):
                                self.rect.y += 1
                            else:
                                self.is_jump = False
                                self.mod_x = 0
                                self.jump_count = 10
                                break
                    self.jump_count -= 1
                    self.rect.x += self.mod_x

                    # if self.jump_count < 0 and not pygame.sprite.spritecollideany(self, groups['top_horizontal']):
                    #     self.rect.y += (self.jump_count ** 2) // 2
                    # else:
                    #     self.rect.y -= (self.jump_count ** 2) // 2
                    # self.jump_count -= 1
                    # self.rect.x += self.mod_x

                else:
                    self.is_jump = False
                    self.mod_x = 0
                    self.jump_count = 10

        for liana in groups['vines']:
            if pygame.sprite.collide_mask(self, liana):
                self.rect.y -= 10

        if not self.is_jump:
            for _ in range(15):
                if not pygame.sprite.spritecollideany(self, groups['horizontal_borders']):
                    self.rect.y += 1
                    self.rect.x += self.mod_x

        if self.move:
            if self.move < 0:
                for _ in range(abs(self.move)):
                    if not pygame.sprite.spritecollideany(self, groups['left_boarders']):
                        self.rect.x -= 1
            elif self.move > 0:
                for _ in range(abs(self.move)):
                    if not pygame.sprite.spritecollideany(self, groups['right_boarders']):
                        self.rect.x += 1

        if pygame.sprite.collide_mask(self, thorns) and not pygame.sprite.collide_mask(self, mountain):
            self.over = True

        for thorn in groups['thorns']:
            if pygame.sprite.collide_mask(self, thorn) and not self.over:
                self.over = True
            elif pygame.sprite.collide_mask(self, thorn) and self.over:
                self.rect.x = 155
                self.rect.y = HEIGHT - 590
                break





def level_2():
    # Border(((10, 5, WIDTH - 10, 5), (10, HEIGHT - 35, WIDTH - 10, HEIGHT - 35),
    #         (10, 5, 10, HEIGHT - 35,), (WIDTH - 10, 5, WIDTH - 10, HEIGHT - 35)))
    Border(10, 5, WIDTH - 10, 5, bottom=True)  # верхняя горизонталь
    Border(10, HEIGHT - 35, WIDTH - 10, HEIGHT - 35, top=True)  # нижняя горизонталь
    Border(10, 5, 10, HEIGHT - 35, left=True)  # левая вертикаль
    # Border(WIDTH - 10, 5, WIDTH - 10, HEIGHT - 35, right=True)  # правая вертикаль

    background_img = load_image('background_2.png')
    ground = pygame.sprite.Sprite()

    ground.rect = (0, HEIGHT - 35, WIDTH, 35)
    ground.image = load_image('ground_2.png')
    ground.add(groups['all_sprites'])

    tree = pygame.sprite.Sprite()
    tree.rect = (475, 237, 148, 328)
    tree.image = load_image('tree.png')
    tree.add(groups['all_sprites'])

    leaf_tree = pygame.sprite.Sprite()
    leaf_tree.rect = (650, 40, 362, 527)
    leaf_tree.image = load_image('tree_with_leaf.png')
    leaf_tree.add(groups['all_sprites'])

    mountain = pygame.sprite.Sprite()
    mountain.rect = (190, 220, 326, 345)
    mountain.image = load_image('mountain.png')
    mountain.add(groups['all_sprites'])

    thorn = pygame.sprite.Sprite()
    thorn.rect = (60, 185, 55, 67)
    thorn.image = load_image('thorn.png')
    thorn.add(groups['thorns'])
    thorn.add(groups['all_sprites'])


    a = Platform((83, 18), (80, HEIGHT - 53), load_image('platform_2.png'))
    do_boarders(a.platform_size, a.platform_coords)
    a = Platform((83, 18), (219, HEIGHT - 82), load_image('platform_2.png'))
    do_boarders(a.platform_size, a.platform_coords)
    a = Platform((83, 18), (323, HEIGHT - 132), load_image('platform_2.png'))
    do_boarders(a.platform_size, a.platform_coords)
    a = Platform((83, 18), (57, HEIGHT - 183), load_image('platform_2.png'))
    do_boarders(a.platform_size, a.platform_coords)
    a = Platform((83, 18), (423, HEIGHT - 190), load_image('platform_2.png'))
    do_boarders(a.platform_size, a.platform_coords)
    a = Platform((83, 18), (640, HEIGHT - 53), load_image('platform_2.png'))
    do_boarders(a.platform_size, a.platform_coords)
    a = Platform((83, 18), (910, HEIGHT - 53), load_image('platform_2.png'))
    do_boarders(a.platform_size, a.platform_coords)
    a = Platform((83, 18), (0, HEIGHT - 466), load_image('platform_2.png'))
    do_boarders(a.platform_size, a.platform_coords)
    a = Platform((185, 18), (-15, HEIGHT - 364), load_image('platform_3.png'))
    do_boarders(a.platform_size, a.platform_coords)
    a = Platform((185, 18), (149, HEIGHT - 500), load_image('platform_3.png'))
    do_boarders(a.platform_size, a.platform_coords)

    star1 = Stars()
    star1.rect.x = 90
    star1.rect.y = 100
    star1.add(groups['all_sprites'])

    star2 = Stars()
    star2.rect.x = 740
    star2.rect.y = 180
    star2.add(groups['all_sprites'])

    star3 = Stars()
    star3.rect.x = 70
    star3.rect.y = 300
    star3.add(groups['all_sprites'])

    # btn = pygame.sprite.Sprite()
    # btn.rect = (944, 15, 65, 65)
    # btn.image = load_image('restart_button.png')
    # btn.add(groups['all_sprites'])

    player = Squirrel()
    groups['all_sprites'].add(player)
    player.rect.x = 155
    player.rect.y = HEIGHT - 590

    running = True
    last_event = ''

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if (event.pos[0] - 976) ** 2 + (event.pos[1] - 47) ** 2 <= 32 ** 2:
                    player.rect.x = 155
                    player.rect.y = HEIGHT - 590

            last_event = event
        groups['all_sprites'].update(last_event)
        screen.fill((255, 255, 255))
        screen.blit(background_img, (0, 0))
        groups['all_sprites'].draw(screen)
        groups['top_horizontal'].draw(screen)
        groups['bottom_horizontal'].draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


thorns = Thorns()
thorns.rect = (200, 212, 278, 344)
thorns.image = load_image('hill_mountain.png')
thorns.mask = pygame.mask.from_surface(load_image('hill_mountain.png'))
thorns.add(groups['all_sprites'])
thorns.add(groups['thorns'])

mountain = pygame.sprite.Sprite()
mountain.rect = (190, 220, 326, 345)
mountain.image = load_image('mountain.png')
mountain.mask = pygame.mask.from_surface(load_image('mountain.png'))
mountain.add(groups['all_sprites'])

liana1 = pygame.sprite.Sprite()
liana1.rect = (410, 0, 40, 332)
liana1.image = load_image('liana_1.png')
liana1.mask = pygame.mask.from_surface(load_image('liana_1.png'))
liana1.add(groups['all_sprites'])
liana1.add(groups['vines'])

liana2 = pygame.sprite.Sprite()
liana2.rect = (510, 0, 13, 126)
liana2.image = load_image('liana_2.png')
liana2.mask = pygame.mask.from_surface(load_image('liana_2.png'))
liana2.add(groups['all_sprites'])
liana2.add(groups['vines'])

liana3 = pygame.sprite.Sprite()
liana3.rect = (570, 0, 35, 396)
liana3.image = load_image('liana_3.png')
liana3.mask = pygame.mask.from_surface(load_image('liana_3.png'))
liana3.add(groups['all_sprites'])
liana3.add(groups['vines'])

liana4 = pygame.sprite.Sprite()
liana4.rect = (650, 0, 37, 404)
liana4.image = load_image('liana_4.png')
liana4.mask = pygame.mask.from_surface(load_image('liana_4.png'))
liana4.add(groups['all_sprites'])
liana4.add(groups['vines'])

thorn1 = pygame.sprite.Sprite()
thorn1.rect = (390, 0, 55, 70)
thorn1.image = load_image('thorn2.png')
thorn1.mask = pygame.mask.from_surface(load_image('thorn2.png'))
thorn1.add(groups['all_sprites'])
thorn1.add(groups['thorns'])

thorn2 = pygame.sprite.Sprite()
thorn2.rect = (560, 0, 55, 70)
thorn2.image = load_image('thorn2.png')
thorn2.mask = pygame.mask.from_surface(load_image('thorn2.png'))
thorn2.add(groups['all_sprites'])
thorn2.add(groups['thorns'])

thorn3 = pygame.sprite.Sprite()
thorn3.rect = (670, 0, 55, 70)
thorn3.image = load_image('thorn2.png')
thorn3.mask = pygame.mask.from_surface(load_image('thorn2.png'))
thorn3.add(groups['all_sprites'])
thorn3.add(groups['thorns'])

player = Squirrel()
groups['all_sprites'].add(player)
player.rect.x = 155
player.rect.y = HEIGHT - 590
