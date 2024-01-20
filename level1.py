import pygame
import sys
import os
import random
from main_functions import load_image, terminate, FPS, size, WIDTH, HEIGHT, clock, screen
from game_over_screen import game_over
from victory_screen import victory

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
stars = 0

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

class Frog(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("frog.png")
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
                    self.mod_x = 3
                if keys[pygame.K_LEFT] and keys[pygame.K_SPACE]:
                    self.is_jump = True
                    self.mod_x = -3

            if keys[pygame.K_SPACE]:
                self.is_jump = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.move = 0
                if event.key == pygame.K_RIGHT:
                    self.move = 0

        if self.rect.x > 1010:
            victory(3)

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

                else:
                    self.is_jump = False
                    self.mod_x = 0
                    self.jump_count = 10

        if pygame.sprite.collide_mask(self, ground):
            self.rect.y += 2

        if not self.is_jump and not pygame.sprite.collide_mask(self, ground):
            for _ in range(15):
                if not pygame.sprite.spritecollideany(self, groups['horizontal_borders']):
                    self.rect.y += 1

        if self.move:
            if self.move < 0:
                for _ in range(abs(self.move)):
                    if not pygame.sprite.spritecollideany(self, groups['left_boarders']):
                        self.rect.x -= 1
            elif self.move > 0:
                for _ in range(abs(self.move)):
                    if not pygame.sprite.spritecollideany(self, groups['right_boarders']):
                        self.rect.x += 1

        if self.rect.y > 600 and not self.over:
            self.over = True
        elif self.rect.y > 600 and self.over:
            self.rect.x = 50
            self.rect.y = 250


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


def level_1():
    background_img = load_image('background_2.png')

    beam = pygame.sprite.Sprite()
    beam.rect = (34, 365, 148, 17)
    beam.image = load_image('beam.png')
    beam.add(groups['all_sprites'])

    beam = pygame.sprite.Sprite()
    beam.rect = (101, 365, 148, 17)
    beam.image = load_image('beam.png')
    beam.add(groups['all_sprites'])

    # long_beam = pygame.sprite.Sprite()
    # long_beam.rect = (0, 358, 187, 17)
    # long_beam.image = load_image('long_beam.png')
    # long_beam.add(groups['all_sprites'])
    a = Platform((187, 17), (0, 358), load_image('long_beam.png'))
    do_boarders(a.platform_size, a.platform_coords)

    water_lily = pygame.sprite.Sprite()
    water_lily.rect = (200, 452, 145, 58)
    water_lily.image = load_image('water_lily.png')
    water_lily.add(groups['all_sprites'])
    lily_board = Border(200, 452, 200 + 145, 452, top=True)

    # cylinder = pygame.sprite.Sprite()
    # cylinder.rect = (411, 390, 114, 61)
    # cylinder.image = load_image('cylinder.png')
    # cylinder.add(groups['all_sprites'])
    a = Platform((61, 114), (411, 390), load_image('cylinder.png'))
    do_boarders(a.platform_size, a.platform_coords)

    triangle = pygame.sprite.Sprite()
    triangle.rect = (470, 390, 44, 45)
    triangle.image = load_image('triangle_platform.png')
    triangle.add(groups['all_sprites'])
    Border(470, 390, 470 + 44, 390, top=True)

    # platform = pygame.sprite.Sprite()
    # platform.rect = (588, 477, 92, 17)
    # platform.image = load_image('platform.png')
    # platform.add(groups['all_sprites'])
    a = Platform((92, 17), (588, 477), load_image('platform.png'))
    do_boarders(a.platform_size, a.platform_coords)

    # platform = pygame.sprite.Sprite()
    # platform.rect = (813, 477, 92, 17)
    # platform.image = load_image('platform.png')
    # platform.add(groups['all_sprites'])
    a = Platform((92, 17), (813, 477), load_image('platform.png'))
    do_boarders(a.platform_size, a.platform_coords)

    tree = pygame.sprite.Sprite()
    tree.rect = (709, 400, 83, 157)
    tree.image = load_image('tree2.png')
    tree.add(groups['all_sprites'])

    star1 = Stars()
    star1.rect.x = 90
    star1.rect.y = 100
    star1.add(groups['all_sprites'])

    star2 = Stars()
    star2.rect.x = 600
    star2.rect.y = 280
    star2.add(groups['all_sprites'])

    star3 = Stars()
    star3.rect.x = 709
    star3.rect.y = 350
    star3.add(groups['all_sprites'])

    player = Frog()
    player.rect.x = 50
    player.rect.y = 250
    player.add(groups['all_sprites'])

    ground = pygame.sprite.Sprite()
    ground.rect = (0, HEIGHT - 105, WIDTH, 105)
    ground.image = load_image('water.png')
    ground.add(groups['all_sprites'])

    # btn = pygame.sprite.Sprite()
    # btn.rect = (944, 15, 65, 65)
    # btn.image = load_image('restart_button.png')
    # btn.add(groups['all_sprites'])

    running = True
    last_event = ''

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if (event.pos[0] - 976) ** 2 + (event.pos[1] - 47) ** 2 <= 32 ** 2:
                    player.rect.x = 50
                    player.rect.y = 250
            last_event = event

        groups['all_sprites'].update(last_event)
        screen.fill((255, 255, 255))
        screen.blit(background_img, (0, 0))
        groups['all_sprites'].draw(screen)
        groups['top_horizontal'].draw(screen)
        groups['bottom_horizontal'].draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


player = Frog()
player.rect.x = 50
player.rect.y = 250
player.add(groups['all_sprites'])

water_lily = pygame.sprite.Sprite()
water_lily.rect = (200, 452, 145, 58)
water_lily.image = load_image('water_lily.png')
water_lily.mask = pygame.mask.from_surface(load_image('water_lily.png'))
water_lily.add(groups['all_sprites'])
lily_board = Border(200, 452, 200 + 145, 452, top=True)

ground = pygame.sprite.Sprite()
ground.rect = (0, HEIGHT - 105, WIDTH, 105)
ground.image = load_image('water.png')
ground.mask = pygame.mask.from_surface(load_image('water.png'))
ground.add(groups['all_sprites'])


