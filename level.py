import pygame
import sys
import os
import random
from main_functions import load_image, terminate, FPS, size, WIDTH, HEIGHT, clock, screen

groups = {
    'all_sprites': pygame.sprite.Group(),
    'horizontal_borders': pygame.sprite.Group(),
    'vertical_borders': pygame.sprite.Group(),
    'left_boarders': pygame.sprite.Group(),
    'right_boarders': pygame.sprite.Group(),
    'platforms': pygame.sprite.Group(),
}


# all_sprites = pygame.sprite.Group()
# horizontal_borders = pygame.sprite.Group()
# vertical_borders = pygame.sprite.Group()
# left_boarders = pygame.sprite.Group()
# right_boarders = pygame.sprite.Group()
# platforms = pygame.sprite.Group()


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2, right=False, left=False):
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


class Worm(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("worm.png")
        self.rect = self.image.get_rect()
        # self.rect.midbottom = (width / 2, height)
        self.mask = pygame.mask.from_surface(self.image)
        self.is_jump = False
        self.jump_count = 8
        self.mod_x = 0
        self.move = 0

    def update(self, event):
        keys = pygame.key.get_pressed()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.move = -5
            if event.key == pygame.K_RIGHT:
                self.move = 5
            if keys[pygame.K_RIGHT] and keys[pygame.K_SPACE]:
                self.is_jump = True
                self.mod_x = 3

        if keys[pygame.K_SPACE]:
            self.is_jump = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.move = 0
            if event.key == pygame.K_RIGHT:
                self.move = 0

        if self.is_jump:
            if self.jump_count >= -8:
                if self.jump_count < 0 and not pygame.sprite.spritecollideany(self, groups['horizontal_borders']) \
                        and not pygame.sprite.collide_mask(self, hill):
                    self.rect.y += (self.jump_count ** 2) // 2
                else:
                    self.rect.y -= (self.jump_count ** 2) // 2
                self.jump_count -= 1
                self.rect.x += self.mod_x

            else:
                self.is_jump = False
                self.mod_x = 0
                self.jump_count = 8

        if not self.is_jump:
            for _ in range(15):
                if not pygame.sprite.spritecollideany(self, groups['horizontal_borders']) and \
                        not pygame.sprite.collide_mask(self, hill):
                    self.rect.y += 1

        if self.move:
            if self.move < 0:
                for _ in range(abs(self.move)):
                    if not pygame.sprite.spritecollideany(self, groups['left_boarders']):
                        self.rect.x -= 1
            elif self.move > 0:
                for _ in range(abs(self.move)):
                    if pygame.sprite.collide_mask(self, hill):
                        self.rect.x += 1
                        self.rect.y -= 3
                    if not pygame.sprite.spritecollideany(self, groups['right_boarders']):
                        self.rect.x += 1


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


class Cloud(Platform):
    def __init__(self, platform_size: tuple, platform_coords: tuple, img: str):
        super().__init__(platform_size, platform_coords, img)
        self.mask = pygame.mask.from_surface(self.image)
        self.add(groups['horizontal_borders'])
        self.add(groups['vertical_borders'])
        self.move_down = True

    def update(self, event):
        for _ in range(2):
            self.rect.y += 1 if self.move_down else -1
            if self.rect.y == 145 or self.rect.y == 440:
                self.move_down = not self.move_down


def do_boarders(platform_size: tuple, platform_coords: tuple, ):
    width, height = platform_size
    p_x, p_y = platform_coords
    Border(p_x, p_y + 1, p_x, p_y + height - 1, right=True)
    Border(p_x + 1, p_y + height, p_x + width - 1, p_y + height)
    Border(p_x + width, p_y + 1, p_x + width, p_y + height - 1, left=True)
    Border(p_x + 1, p_y, p_x + width - 1, p_y + height)


def level_1():
    background_img = load_image('background_1.png')

    Border(10, 5, WIDTH - 10, 5)  # верхняя горизонталь
    Border(10, HEIGHT - 70, WIDTH - 272, HEIGHT - 70)  # нижняя горизонталь (левая часть)
    # ЯМА
    Border(WIDTH - 272, 531, WIDTH - 272, HEIGHT - 34, left=True)  # левая вертикаль ямы
    Border(WIDTH - 88, 531, WIDTH - 88, HEIGHT - 34, right=True)  # правая вертикаль ямы
    Border(WIDTH - 272, HEIGHT - 35, WIDTH - 88, HEIGHT - 35)  # горизонталь ямы
    # яма
    Border(WIDTH - 88, HEIGHT - 70, WIDTH - 10, HEIGHT - 70)  # нижняя горизонталь (правая часть)
    Border(10, 5, 10, HEIGHT - 70, left=True)  # левая вертикаль
    Border(WIDTH - 10, 5, WIDTH - 10, HEIGHT - 70, right=True)  # правая вертикаль

    # hill = load_image('hill.png')
    # hill.blit(screen, (190, HEIGHT - 80e))

    # groups['all_sprites'].add(hill)
    # groups['platforms'].add(hill)
    hill.rect = (200, HEIGHT - 70 - 173, 344, 173)
    hill.image = load_image('hill.png')
    pygame.mask.from_surface(hill.image)
    hill.add(groups['horizontal_borders'])
    hill.add(groups['vertical_borders'])

    a = Platform((327, 35), (249, 159), load_image('platform.png'))
    do_boarders(a.platform_size, a.platform_coords)
    a = Platform((152, 35), (57, 77), pygame.transform.scale(load_image('platform.png'), (152, 35)))
    do_boarders(a.platform_size, a.platform_coords)
    Platform((328, 75), (-20, 286), load_image('pol_platform.png'))
    Platform((328, 75), (-30, 216), load_image('pol_platform2.png'))
    leaf = Platform((175, 95), (40, 220), load_image('leaf.png'))
    pygame.mask.from_surface(leaf.image)
    leaf.add(groups['horizontal_borders'])
    leaf.add(groups['vertical_borders'])

    Cloud((176, 86), (608, 145), load_image('cloud.png'))

    player = Worm()
    groups['all_sprites'].add(player)
    player.rect.x = 30
    player.rect.y = 400
    # player.rect.x = 329
    # player.rect.y = 20
    running = True
    last_event = ''
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            last_event = event

        groups['all_sprites'].update(last_event)
        screen.fill((255, 255, 255))
        screen.blit(background_img, (0, 0))
        groups['all_sprites'].draw(screen)
        groups['horizontal_borders'].draw(screen)
        groups['vertical_borders'].draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    cloud = ''
    hill = pygame.sprite.Sprite()
    pygame.init()
    level_1()
    pygame.quit()
