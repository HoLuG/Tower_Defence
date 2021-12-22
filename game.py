import pygame
import os
from skeleton import Skeleton
from bat import Bat
import time
import random
from archerTower import ArcherTower


waves = [[3, 1, 0],
         [2, 0, 0],
         [0, 1, 0],
         ]
attack_tower_names = ["archer", "archer2"]
support_tower_names = ["range", "damage"]


class Game:
    def __init__(self, win):
        self.width = 1350
        self.height = 700
        self.win = win
        self.timer = time.time()
        self.enemies = []
        self.towers = [ArcherTower(370, 370), ArcherTower(1100, 170)]
        self.attack_towers = []
        self.support_towers = []
        self.lives = 10
        self.money = 1000
        self.life_font = pygame.font.SysFont("comicsans", 65)
        self.selected_tower = None
        self.bg = pygame.image.load(os.path.join("game assets", "mb.png"))
        self.lives_img = pygame.transform.scale(pygame.image.load(os.path.join("game assets", "heart.png")).convert_alpha(), (60, 60))
        self.money_img = pygame.transform.scale(pygame.image.load(os.path.join("game assets", "money.png")).convert_alpha(), (60, 60))
        self.bg = pygame.transform.scale(self.bg, (self.width, self.height))
        self.clicks = []
        self.wave = 0
        self.pause = False
        self.current_wave = waves[self.wave][:]

    def gen_enemies(self):

        if sum(self.current_wave) == 0:
            if len(self.enemies) == 0:
                pygame.time.delay(10000)  # пауза после прохождения волны
                if self.wave + 1 < len(waves):
                    self.wave += 1
                    self.current_wave = waves[self.wave]
                else:
                    self.pause = True

        else:
            wave_enemies = [Skeleton(), Bat()]
            for x in range(len(self.current_wave)):
                if self.current_wave[x] != 0:
                    self.enemies.append(wave_enemies[x])
                    self.current_wave[x] = self.current_wave[x] - 1
                    break

    def draw(self):
        self.win.blit(self.bg, (0, 0))
        for en in self.enemies:
            en.draw(self.win)

        for tw in self.towers:
            tw.draw(self.win)
        # draw lives
        text = self.life_font.render(str(self.lives), 1, (255, 255, 255))
        life = pygame.transform.scale(self.lives_img, (50, 50))
        start_x = self.width - life.get_width() - 10

        self.win.blit(text, (start_x - text.get_width() - 10, -15))
        self.win.blit(life, (start_x, 10))

        text = self.life_font.render(str(self.money), 1, (255, 255, 255))
        money = pygame.transform.scale(self.money_img, (50, 50))
        start_x = self.width - life.get_width() - 10

        self.win.blit(text, (start_x - text.get_width() - 10, 40))
        self.win.blit(money, (start_x, 65))
        pygame.display.update()

    def run(self):
        running = True
        clock = pygame.time.Clock()
        while running:
            clock.tick(500)
            if self.pause == False:
                if time.time() - self.timer >= random.randrange(1, 9):
                    self.timer = time.time()
                    self.gen_enemies()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                pos = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.clicks += [pos]
                    print(self.clicks)

            if not self.pause:
                to_del = []
                for en in self.enemies:
                    en.move()
                    if en.y > 798:
                        to_del.append(en)
                # delete all enemies off the screen
                for d in to_del:
                    self.lives -= 1
                    self.enemies.remove(d)

                for tw in self.towers:
                    self.money += tw.attack(self.enemies)

                for tw in self.towers:
                    tw.attack(self.enemies)

                if self.lives <= 0:
                    print("You Lose")
                    exit()

            pygame.event.pump()
            self.draw()
        pygame.quit()

