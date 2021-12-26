import pygame
import os
from skeleton import Skeleton
from bat import Bat
from orc import Orc
import time
import random
import sys
from archerTower import ArcherTower
from Button import PlayPauseButton

pygame.init()

filename = "game assets/" + 'PingPong.ttf'


def print_text(self, message, x, y, font_color=(23, 41, 32), font_type=filename,
               font_size=30):  # печать текста на экран
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    self.win.blit(text, (x, y))


waves = [[1, 0, 3],
         [2, 0, 2],
         [0, 1, 0],
         ]
attack_tower_names = ["archer", "archer2"]
support_tower_names = ["range", "damage"]

play_btn = pygame.transform.scale(pygame.image.load(os.path.join("game assets", "play.png")), (50, 50))
pause_btn = pygame.transform.scale(pygame.image.load(os.path.join("game assets", "pause.png")), (50, 50))


class Game:
    def __init__(self, win):
        self.num = 0
        self.width = 1350
        self.height = 700
        self.win = win
        self.timer = time.time()
        self.enemies = []
        self.towers = []
        self.attack_towers = []
        self.lives = 5
        self.money = 450
        self.action = False
        self.life_font = pygame.font.SysFont("comicsans", 65)
        self.bg = pygame.image.load(os.path.join("game assets", "mb.png"))
        self.ending = pygame.transform.scale(
            pygame.image.load(os.path.join("game assets", "ending.png")).convert_alpha(), (550, 600))
        self.choice = pygame.transform.scale(
            pygame.image.load(os.path.join("game assets", "choice.png")).convert_alpha(), (900, 200))
        self.lives_img = pygame.transform.scale(pygame.image.load(os.path.join("game assets", "heart.png")).
                                                convert_alpha(), (60, 60))
        self.money_img = pygame.transform.scale(pygame.image.load(os.path.join("game assets", "money.png")).
                                                convert_alpha(), (60, 60))
        self.empty_btn = pygame.image.load(os.path.join("game assets", "empty.png")).convert_alpha()

        self.btn_quit = (self.width / 2 - self.empty_btn.get_width() / 2, 300, self.empty_btn.get_width(),
                         self.empty_btn.get_height())
        self.flags = [False, False, False, False, False, False, False]
        self.bg = pygame.transform.scale(self.bg, (self.width, self.height))
        self.wave = 0
        self.towers_in = [ArcherTower(370, 370), ArcherTower(620, 150), ArcherTower(93, 390), ArcherTower(1105, 155),
                          ArcherTower(870, 330), ArcherTower(1157, 370), ArcherTower(1107, 580)]
        self.pause = False
        self.current_wave = waves[self.wave][:]
        self.playPauseButton = PlayPauseButton(play_btn, pause_btn, 20, self.height - 60)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Terminal", 60)
        self.time_left = 20.0

    def gen_enemies(self):
        if sum(self.current_wave) == 0:
            if len(self.enemies) == 0:
                if self.wave + 1 < len(waves):
                    self.wave += 1
                    self.current_wave = waves[self.wave]

        wave_enemies = [Skeleton(), Bat(), Orc()]
        for x in range(len(self.current_wave)):
            if self.current_wave[x] != 0:
                self.enemies.append(wave_enemies[x])
                self.current_wave[x] = self.current_wave[x] - 1
                break

    def draw(self):
        self.win.blit(self.bg, (0, 0))
        if 0 < self.time_left < 20:
            self.win.blit(self.time_left_rendered, (0, 0))

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
        if self.action and self.money >= 200:
            self.win.blit(self.choice, (250, 200))
            print_text(self, message='Do you want to build tower for 200 money?', x=260, y=220,
                       font_size=40, font_color='black')
            self.win.blit(self.empty_btn, (self.btn_quit[0] - 200, self.btn_quit[1]))
            self.win.blit(self.empty_btn, (self.btn_quit[0] + 250, self.btn_quit[1]))
        elif self.action:
            self.win.blit(self.choice, (250, 200))
            print_text(self, message='Not enough money', x=430, y=220,
                       font_size=60, font_color='black')
            print_text(self, message='(200 required)', x=590, y=280,
                       font_size=30, font_color='black')
            self.win.blit(self.empty_btn, (self.btn_quit[0] + 20, self.btn_quit[1] + 20))

        pygame.display.update()

    def draw_end(self, x, y, end):
        self.win.blit(self.ending, (400, 50))
        self.win.blit(self.empty_btn, (self.btn_quit[0], self.btn_quit[1]))
        self.win.blit(self.empty_btn, (self.btn_quit[0], self.btn_quit[1] + 100))
        if end == 'Bad':
            message = 'RETURN'
            x_mes = self.width / 2 - self.empty_btn.get_width() / 2 + 22
            print_text(self, message='YOU LOSE', x=400, y=100,
                       font_size=125, font_color='red')
        else:
            message = "LOBBY"
            x_mes = self.width / 2 - self.empty_btn.get_width() / 2 + 34
            print_text(self, message='Congratulations!!!', x=460, y=70,
                       font_size=50, font_color='black')
            print_text(self, message='YOU WIN', x=429, y=100,
                   font_size=125, font_color='green')

        if self.btn_quit[0] <= x <= self.btn_quit[0] + self.btn_quit[2] and \
                self.btn_quit[1] <= y <= self.btn_quit[1] + self.btn_quit[3]:
            print_text(self, message=message, x=x_mes, y=303,
                       font_size=60, font_color='grey')
        else:
            print_text(self, message=message, x=x_mes, y=303,
                       font_size=60, font_color='white')
        if self.btn_quit[0] <= x <= self.btn_quit[0] + self.btn_quit[2] and \
                self.btn_quit[1] + 100 <= y <= self.btn_quit[1] + self.btn_quit[3] + 100:
            print_text(self, message='QUIT', x=self.width / 2 - self.empty_btn.get_width() / 2 + 50, y=403,
                       font_size=60, font_color='grey')
        else:
            print_text(self, message='Quit', x=self.width / 2 - self.empty_btn.get_width() / 2 + 50, y=403,
                       font_size=60, font_color='white')
        pygame.display.update()

    def run(self):
        running = True
        end = 'good'
        self.flag = False
        self.time_left = 20.0
        while running:
            x, y = pygame.mouse.get_pos()
            if len(self.enemies) == 0 and not self.flag and self.wave + 1 < len(waves):
                if self.time_left > 0:
                    time_passed = self.clock.tick()
                    time_passed_seconds = time_passed / 1000.
                    self.time_left -= time_passed_seconds
                    self.time_left_rendered = self.font.render(
                        "Time left = {:02}:{:02}".format(round(int(self.time_left) / 60),
                                                         round(int(self.time_left) % 60)), False,
                        (255, 255, 255))
                    self.win.blit(self.time_left_rendered, (0, 0))
                else:
                    self.flag = True

            if not self.pause and self.flag:
                if time.time() - self.timer >= random.randrange(1, 9):
                    self.timer = time.time()
                    self.gen_enemies()

            if self.action and self.money >= 200:
                if self.btn_quit[0] - 200 <= x <= self.btn_quit[0] - 200 + self.btn_quit[2] and \
                        self.btn_quit[1] <= y <= self.btn_quit[1] + self.btn_quit[3]:
                    print_text(self, message='BUY', x=430, y=305,
                               font_size=60, font_color='grey')
                else:
                    print_text(self, message='BUY', x=430, y=305,
                               font_size=60, font_color='white')
                if self.btn_quit[0] + 250 <= x <= self.btn_quit[0] + 250 + self.btn_quit[2] and \
                        self.btn_quit[1] <= y <= self.btn_quit[1] + self.btn_quit[3]:
                    print_text(self, message='RETURN', x=833, y=305,
                               font_size=60, font_color='grey')
                else:
                    print_text(self, message='RETURN', x=833, y=305,
                               font_size=60, font_color='white')

            elif self.action:
                if self.btn_quit[0] + 20 <= x <= self.btn_quit[0] + 20 + self.btn_quit[2] and \
                        self.btn_quit[1] + 20 <= y <= self.btn_quit[1] + 20 + self.btn_quit[3]:
                    print_text(self, message='BACK', x=635, y=322,
                               font_size=60, font_color='grey')
                else:
                    print_text(self, message='BACK', x=635, y=322,
                               font_size=60, font_color='white')
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 20 <= x <= 20 + 50 and 640 <= y <= 640 + 50 and not self.pause:
                        self.pause = True
                    elif 20 <= x <= 20 + 50 and 640 <= y <= 640 + 50 and self.pause:
                        self.pause = False

                    if self.action and self.money >= 200:
                        if self.btn_quit[0] - 200 <= x <= self.btn_quit[0] - 200 + self.btn_quit[2] and \
                                self.btn_quit[1] <= y <= self.btn_quit[1] + self.btn_quit[3]:
                            self.action = False
                            self.pause = False
                            self.flags[self.num] = True
                            self.money -= 200
                            self.towers += [self.towers_in[self.num]]
                        elif self.btn_quit[0] + 250 <= x <= self.btn_quit[0] + 250 + self.btn_quit[2] and \
                                self.btn_quit[1] <= y <= self.btn_quit[1] + self.btn_quit[3]:
                            self.action = False
                            self.pause = False
                    elif self.action:
                        if self.btn_quit[0] + 20 <= x <= self.btn_quit[0] + 20 + self.btn_quit[2] and \
                                self.btn_quit[1] + 20 <= y <= self.btn_quit[1] + 20 + self.btn_quit[3]:
                            self.action = False
                            self.pause = False

                    if 322 <= x <= 440 and 390 <= y <= 440 and not self.flags[0]:
                        self.num = 0
                        self.pause = True
                        self.action = True
                    elif 565 <= x <= 675 and 165 <= y <= 215 and not self.flags[1]:
                        self.num = 1
                        self.pause = True
                        self.action = True
                    elif 45 <= x <= 155 and 410 <= y <= 455 and not self.flags[2]:
                        self.num = 2
                        self.pause = True
                        self.action = True
                    elif 1053 <= x <= 1165 and 180 <= y <= 220 and not self.flags[3]:
                        self.num = 3
                        self.pause = True
                        self.action = True
                    elif 820 <= x <= 926 and 356 <= y <= 398 and not self.flags[4]:
                        self.num = 4
                        self.pause = True
                        self.action = True
                    elif 1100 <= x <= 1214 and 395 <= y <= 435 and not self.flags[5]:
                        self.num = 5
                        self.pause = True
                        self.action = True
                    elif 1056 <= x <= 1163 and 608 <= y <= 650 and not self.flags[6]:
                        self.num = 6
                        self.pause = True
                        self.action = True

            if not self.pause and self.flag:
                to_del = []
                for en in self.enemies:
                    en.move()
                    if en.y > 798:
                        to_del.append(en)

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

                if self.wave + 1 == len(waves) and self.enemies == []:
                    running = False

                if not self.enemies:
                    time_passed = self.clock.tick()
                    self.flag = False
                    self.time_left = 20.0

            pygame.event.pump()
            self.draw()

        running = True
        while running:
            x, y = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.btn_quit[0] <= x <= self.btn_quit[0] + self.btn_quit[2] and \
                            self.btn_quit[1] <= y <= self.btn_quit[1] + self.btn_quit[3]:
                        running = False
                    if self.btn_quit[0] <= x <= self.btn_quit[0] + self.btn_quit[2] and \
                            self.btn_quit[1] + 100 <= y <= self.btn_quit[1] + self.btn_quit[3] + 100:
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.draw_end(x, y, end)
