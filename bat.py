import pygame
import os
from enemys import Enemy

imgs = []
for x in range(25):
    add_str = str(x)
    if x < 10:
        add_str = "0" + add_str
    imgs.append(pygame.transform.scale(pygame.image.load(
        os.path.join("game assets/enemies2", "Version1_Walk_" + add_str + ".png")), (80, 80)))


class Bat(Enemy):
    def __init__(self):
        super().__init__()
        self.name = "bat"
        self.money = 10
        self.max_health = 2
        self.health = self.max_health
        self.imgs = imgs[:]
