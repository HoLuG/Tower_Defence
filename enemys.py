import pygame
import math


class Enemy:
    def __init__(self):
        self.animation_count = 0
        self.health = 1
        self.path = [(6, 548), (55, 547), (119, 537), (182, 522), (215, 483), (242, 435), (260, 386), (287, 341),
                     (328, 328), (383, 319), (440, 298), (474, 259), (497, 198), (506, 146), (545, 113), (589, 110),
                     (633, 111), (1127, 103), (1232, 131), (1271, 158), (1278, 219), (1257, 267), (1213, 308),
                     (1139, 329), (1083, 337), (1043, 378), (1040, 423), (1043, 477), (1056, 535), (1149, 553),
                     (1196, 567), (1216, 599), (1229, 677), (1231, 694), (1231, 800)]
        self.x = self.path[0][0]
        self.y = self.path[0][1]
        self.img = None
        self.imgs = []
        self.path_pos = 0
        self.max_health = 1
        self.flipped = False

    def draw(self, win):
        self.img = self.imgs[self.animation_count]

        win.blit(self.img, (self.x - self.img.get_width() / 2, self.y - self.img.get_height() / 1.2 - 35))
        self.draw_health_bar(win)

    def draw_health_bar(self, win):
        length = 50
        move_by = round(length / self.max_health)
        health_bar = move_by * self.health

        pygame.draw.rect(win, (255, 0, 0), (self.x-25, self.y-105, length, 10), 0)
        pygame.draw.rect(win, (0, 255, 0), (self.x-25, self.y - 105, health_bar, 10), 0)

    def move(self):
        self.animation_count += 1
        if self.animation_count >= len(self.imgs):
            self.animation_count = 0

        x1, y1 = self.path[self.path_pos]
        if self.path_pos + 1 >= len(self.path):
            x2, y2 = (1231, 800)
        else:
            x2, y2 = self.path[self.path_pos + 1]

        dis = ((x2 - x1) * 2, (y2 - y1) * 2)
        length = math.sqrt((dis[0]) ** 2 + (dis[1]) ** 2)
        if length == 0:
            length = 1
        dis = (dis[0] / length, dis[1] / length)

        if dis[0] < 0 and not self.flipped:
            self.flipped = True
            for x, img in enumerate(self.imgs):
                self.imgs[x] = pygame.transform.flip(img, True, False)
        elif dis[0] > 0 and self.flipped:
            self.flipped = False
            for x, img in enumerate(self.imgs):
                self.imgs[x] = pygame.transform.flip(img, True, False)
        move_x, move_y = ((self.x + dis[0]), (self.y + dis[1]))

        self.x = move_x
        self.y = move_y

        if dis[0] >= 0:
            if dis[1] >= 0:
                if self.x >= x2 and self.y >= y2:
                    self.path_pos += 1
            else:
                if self.x >= x2 and self.y <= y2:
                    self.path_pos += 1
        else:
            if dis[1] >= 0:
                if self.x <= x2 and self.y >= y2:
                    self.path_pos += 1
            else:
                if self.x <= x2 and self.y >= y2:
                    self.path_pos += 1

    def hit(self, damage):
        self.health -= damage
        if self.health <= 0:
            return True
        return False
