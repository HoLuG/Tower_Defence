import pygame
import os
import math


class Enemy:
    def __init__(self):
        self.width = 64
        self.height = 64
        self.animation_count = 0
        self.health = 1
        self.vel = 3
        self.path = [(6, 548), (55, 547), (119, 537), (182, 522), (215, 483), (242, 435), (260, 386), (287, 341), (328, 328), (383, 319), (440, 298), (474, 259), (497, 198), (506, 146), (545, 113), (589, 110), (633, 111), (1127, 103), (1232, 131), (1271, 158), (1278, 219), (1257, 267), (1213, 308), (1139, 329), (1083, 337), (1043, 378), (1040, 423), (1043, 477), (1056, 535), (1149, 553), (1196, 567), (1216, 599), (1229, 677), (1231, 694), (1231, 800)]
        self.x = self.path[0][0]
        self.y = self.path[0][1]
        self.img = None
        self.dis = 0
        self.imgs = []
        self.path_pos = 0
        self.move_count = 0
        self.move_dis = 0
        self.max_health = 1
        self.speed_increase = 1.2
        self.flipped = False

    def draw(self, win):
        self.img = self.imgs[self.animation_count]

        win.blit(self.img, (self.x - self.img.get_width() / 2, self.y - self.img.get_height() / 1.2 - 35))
        self.draw_health_bar(win)

    def draw_health_bar(self, win):
        """
        draw health bar above enemy
        :param win: surface
        :return: None
        """
        length = 50
        move_by = round(length / self.max_health)
        health_bar = move_by * self.health

        pygame.draw.rect(win, (255,0,0), (self.x-25, self.y-105, length, 10), 0)
        pygame.draw.rect(win, (0, 255, 0), (self.x-25, self.y - 105, health_bar, 10), 0)

    def collide(self, X, Y):
        if X <= self.x + self.width and X >= self.x:
            if Y <= self.y + self.height and Y >= self.y:
                return True
        return False

    def move(self):
        self.animation_count += 1
        if self.animation_count >= len(self.imgs):
            self.animation_count = 0

        x1, y1 = self.path[self.path_pos]
        if self.path_pos + 1 >= len(self.path):
            x2, y2 = (1231, 800)
        else:
            x2, y2 = self.path[self.path_pos + 1]

        dirn = ((x2 - x1) * 2, (y2 - y1) * 2)
        length = math.sqrt((dirn[0]) ** 2 + (dirn[1]) ** 2)
        if length == 0:
            length = 1
        dirn = (dirn[0] / length, dirn[1] / length)

        if dirn[0] < 0 and not(self.flipped):
            self.flipped = True
            for x, img in enumerate(self.imgs):
                self.imgs[x] = pygame.transform.flip(img, True, False)
        elif dirn[0] > 0 and self.flipped:
            self.flipped = False
            for x, img in enumerate(self.imgs):
                self.imgs[x] = pygame.transform.flip(img, True, False)


        move_x, move_y = ((self.x + dirn[0]), (self.y + dirn[1]))

        self.x = move_x
        self.y = move_y

        # Go to next point
        if dirn[0] >= 0:  # moving right
            if dirn[1] >= 0:  # moving down
                if self.x >= x2 and self.y >= y2:
                    self.path_pos += 1
            else:
                if self.x >= x2 and self.y <= y2:
                    self.path_pos += 1
        else:  # moving left
            if dirn[1] >= 0:  # moving down
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


