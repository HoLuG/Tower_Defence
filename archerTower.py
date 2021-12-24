import pygame
from tower import Tower
import os
import math
import time


class ArcherTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y)
        tower_imgs1 = []
        archer_imgs1 = []
        tower_imgs1.append(pygame.transform.scale(
            pygame.image.load(os.path.join("game assets/Towers/archertower.png")).convert_alpha(), (150, 150)))
        for i in range(1, 6):
            archer_imgs1.append(pygame.transform.scale(
                pygame.image.load(os.path.join("game assets/Towers", 'archer_' + str(i) + ".png")).convert_alpha(),
                (60, 60)))
        self.archer_imgs = archer_imgs1[:]
        self.tower_imgs = tower_imgs1[:]
        self.archer_count = 0
        self.range = 220
        self.original_range = self.range
        self.inRange = False
        self.left = True
        self.damage = 1
        self.original_damage = self.damage
        self.width = self.height = 90
        self.moving = False
        self.name = "archer"
        self.timer = time.time()
        self.coord_x, self.coord_y = x, y

    def draw(self, win, pause):
        super().draw(win)
        if self.inRange and not pause:
            self.archer_count += 1
            if self.archer_count >= len(self.archer_imgs) * 18:
                self.archer_count = 0
        else:
            self.archer_count = 0

        archer = self.archer_imgs[self.archer_count // 18]
        if self.left:
            add = -25
        else:
            add = -archer.get_width() + 10

        self.archer_count += 1
        surface = pygame.Surface((self.range * 2, self.range * 2), pygame.SRCALPHA, 32)
        pygame.draw.circle(surface, (128, 128, 128, 120), (self.range, self.range), self.range)
        win.blit(surface, (self.coord_x - self.range, self.coord_y - self.range))
        win.blit(archer, ((self.coord_x + add), (self.coord_y - archer.get_height() - 10)))

    def change_range(self, r):
        self.range = r

    def attack(self, enemies):
        self.inRange = False
        enemy_closest = []
        for enemy in enemies:
            x = enemy.x
            y = enemy.y - 40
            dis = math.sqrt((self.coord_x - x)**2 + (self.coord_y - y)**2)
            if dis <= self.range:
                self.inRange = True
                enemy_closest.append(enemy)

        if len(enemy_closest) > 0:
            first_enemy = enemy_closest[0]

            if first_enemy.x > self.coord_x and not self.left:
                self.left = True
                for x, img in enumerate(self.archer_imgs):
                    self.archer_imgs[x] = pygame.transform.flip(img, True, False)
            elif self.left and first_enemy.x < self.coord_x:
                self.left = False
                for x, img in enumerate(self.archer_imgs):
                    self.archer_imgs[x] = pygame.transform.flip(img, True, False)

            if time.time() - self.timer >= 0.85:
                self.timer = time.time()
                if first_enemy.hit(self.damage):
                    money = first_enemy.money
                    enemies.remove(first_enemy)
                    return money
        return 0
