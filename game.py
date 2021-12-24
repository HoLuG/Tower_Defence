import pygame
import os
from skeleton import Skeleton
from bat import Bat
import time
import random
import sys
from archerTower import ArcherTower
from game_menu import PlayPauseButton

pygame.init()

filename = "game assets/" + 'PingPong.ttf'


def print_text(self, message, x, y, font_color=(23, 41, 32), font_type=filename,
               font_size=30):  # печать текста на экран
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    self.win.blit(text, (x, y))


waves = [[40, 0, 0],
         [2, 0, 0],
         [0, 1, 0],
         ]
attack_tower_names = ["archer", "archer2"]
support_tower_names = ["range", "damage"]

play_btn = pygame.transform.scale(pygame.image.load(os.path.join("game assets", "play.png")), (50, 50))
pause_btn = pygame.transform.scale(pygame.image.load(os.path.join("game assets", "pause.png")), (50, 50))


class Game:
    def __init__(self, win):
        self.width = 1350
        self.height = 700
        self.win = win
        self.timer = time.time()
        self.enemies = []
        self.towers = [ArcherTower(375, 368), ArcherTower(1105, 155), ArcherTower(880, 330)]
        self.attack_towers = []
        self.support_towers = []
        self.lives = 5
        self.money = 1000
        self.life_font = pygame.font.SysFont("comicsans", 65)
        self.selected_tower = None
        self.bg = pygame.image.load(os.path.join("game assets", "mb.png"))
        self.lives_img = pygame.transform.scale(pygame.image.load(os.path.join("game assets", "heart.png")).
                                                convert_alpha(), (60, 60))
        self.money_img = pygame.transform.scale(pygame.image.load(os.path.join("game assets", "money.png")).
                                                convert_alpha(), (60, 60))
        self.empty_btn = pygame.image.load(os.path.join("game assets", "empty.png")).convert_alpha()
        self.btn_quit = (self.width / 2 - self.empty_btn.get_width() / 2, 300, self.empty_btn.get_width(),
                         self.empty_btn.get_height())
        self.bg = pygame.transform.scale(self.bg, (self.width, self.height))
        self.clicks = []
        self.wave = 0
        self.pause = False
        self.current_wave = waves[self.wave][:]
        self.playPauseButton = PlayPauseButton(play_btn, pause_btn, 20, self.height - 60)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Terminal", 60)
        self.time_left = 30.0

    def gen_enemies(self):
        if sum(self.current_wave) == 0:
            if len(self.enemies) == 0:
                print(1)
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
        #  if 0 < self.time_left < 2:
            #  self.win.blit(self.time_left_rendered, (0, 0))

        for en in self.enemies:
            en.draw(self.win)

        for tw in self.towers:
            tw.draw(self.win, self.pause)
        # draw lives
        text = self.life_font.render(str(self.lives), True, (255, 255, 255))
        life = pygame.transform.scale(self.lives_img, (50, 50))
        start_x = self.width - life.get_width() - 10

        self.win.blit(text, (start_x - text.get_width() - 10, -15))
        self.win.blit(life, (start_x, 10))

        text = self.life_font.render(str(self.money), True, (255, 255, 255))
        money = pygame.transform.scale(self.money_img, (50, 50))
        start_x = self.width - life.get_width() - 10

        self.win.blit(text, (start_x - text.get_width() - 10, 40))
        self.win.blit(money, (start_x, 65))

        self.playPauseButton.draw(self.win, self.pause)

        pygame.display.update()

    def draw_end(self, x, y, end):
        pygame.draw.rect(self.win, (139, 69, 19), (400, 50, 550, 600))
        self.win.blit(self.empty_btn, (self.btn_quit[0], self.btn_quit[1]))
        if end == 'Bad':
            message_1 = 'YOU LOSE'
        else:
            message_1 = 'YOU WIN'
        print_text(self, message=message_1, x=400, y=100,
                   font_size=125, font_color='black')

        if self.btn_quit[0] <= x <= self.btn_quit[0] + self.btn_quit[2] and \
                self.btn_quit[1] <= y <= self.btn_quit[1] + self.btn_quit[3]:
            print_text(self, message='Return', x=self.width / 2 - self.empty_btn.get_width() / 2 + 22, y=303,
                       font_size=60, font_color='grey')
        else:
            print_text(self, message='Return', x=self.width / 2 - self.empty_btn.get_width() / 2 + 22, y=303,
                       font_size=60, font_color='white')
        pygame.display.update()

    def run(self):
        running = True
        end = 'good'
        while running:
            self.clock.tick(500)
            x, y = pygame.mouse.get_pos()
            # if len(self.enemies) == 0:
                #  self.time_left = 5.0
                #  while self.time_left > 0:
                #      time_passed = self.clock.tick()
                #      time_passed_seconds = time_passed / 1000.
                #      self.time_left -= time_passed_seconds
                #      self.time_left_rendered = self.font.render(
                #          "Time left = {:02}:{:02}".format(round(int(self.time_left) / 60),
                #                                           round(int(self.time_left) % 60)), False,
                #          (255, 255, 255))
                #      self.win.blit(self.time_left_rendered, (0, 0))
                #      self.draw()

            if not self.pause:
                if time.time() - self.timer >= random.randrange(1, 9):
                    self.timer = time.time()
                    self.gen_enemies()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 20 <= x <= 20 + 50 and 640 <= y <= 640 + 50 and not self.pause:
                        self.pause = True
                    elif 20 <= x <= 20 + 50 and 640 <= y <= 640 + 50 and self.pause:
                        self.pause = False

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
                running = False
                end = 'Bad'

            pygame.event.pump()
            self.draw()

        running = True
        while running:
            x, y = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(x, y, self.btn_quit)
                    if self.btn_quit[0] <= x <= self.btn_quit[0] + self.btn_quit[2] and \
                            self.btn_quit[1] <= y <= self.btn_quit[1] + self.btn_quit[3]:
                        running = False
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.draw_end(x, y, end)
