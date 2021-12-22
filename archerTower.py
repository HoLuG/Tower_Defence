import pygame
from tower import Tower
import os
import math
import time


class ArcherTower(Tower):
    def __init__(self, x,y):
        super().__init__(x, y)
        tower_imgs1 = []
        archer_imgs1 = []
        tower_imgs1.append(pygame.transform.scale(
            pygame.image.load(os.path.join("game assets/Towers/archertower.png")).convert_alpha(), (150, 150)))
        for x in range(1, 6):
            archer_imgs1.append(pygame.transform.scale(
                pygame.image.load(os.path.join("game assets/Towers", 'archer_' + str(x) + ".png")).convert_alpha(), (60, 60)))
        self.archer_imgs = archer_imgs1[:]
        self.tower_imgs = tower_imgs1[:]
        self.archer_count = 0
        self.range = 200
        self.original_range = self.range
        self.inRange = False
        self.left = True
        self.damage = 1
        self.original_damage = self.damage
        self.width = self.height = 90
        self.moving = False
        self.name = "archer"
        self.timer = time.time()

    def draw(self, win):
        super().draw(win)
        if self.inRange and not self.moving:
            self.archer_count += 1
            if self.archer_count >= len(self.archer_imgs) * 18:
                self.archer_count = 0
        else:
            self.archer_count = 0

        archer = self.archer_imgs[self.archer_count // 18]
        if self.left == True:
            add = -25
        else:
            add = -archer.get_width() + 10
        self.archer_count += 1
        win.blit(archer, ((self.x + add), (self.y - archer.get_height() - 10)))

    def change_range(self, r):
        self.range = r

    def attack(self, enemies):
        self.inRange = False
        enemy_closest = []
        for enemy in enemies:
            x = enemy.x
            y = enemy.y
            dis = math.sqrt((self.x - 80/2 - x)**2 + (self.y - 80 /2 - y)**2)
            if dis <= self.range:
                self.inRange = True
                enemy_closest.append(enemy)

        enemy_closest.sort(key=lambda x: x.path_pos)
        enemy_closest = enemy_closest[::-1]
        if len(enemy_closest) > 0:
            first_enemy = enemy_closest[0]
            if time.time() - self.timer >= 0.85:
                self.timer = time.time()
                if first_enemy.hit(self.damage):
                    money = first_enemy.money
                    enemies.remove(first_enemy)
                    return money

            if first_enemy.x > self.x and not(self.left):
                self.left = True
                for x, img in enumerate(self.archer_imgs):
                    self.archer_imgs[x] = pygame.transform.flip(img, True, False)
            elif self.left and first_enemy.x < self.x:
                self.left = False
                for x, img in enumerate(self.archer_imgs):
                    self.archer_imgs[x] = pygame.transform.flip(img, True, False)
        return 0
