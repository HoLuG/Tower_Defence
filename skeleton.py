import pygame
import os
from enemys import Enemy

imgs = []
for x in range(17):
    add_str = str(x)
    if x < 10:
        add_str = "0" + add_str
    imgs.append(pygame.transform.scale(pygame.image.load
                                       (os.path.join("game assets/enemies", "Walking_0" + add_str + ".png")), (80, 80)))


class Skeleton(Enemy):
    def __init__(self):
        super().__init__()
        self.name = "skeleton"
        self.money = 1
        self.max_health = 7
        self.health = self.max_health
        self.imgs = imgs[:]
