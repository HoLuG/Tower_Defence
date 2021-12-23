from game import Game
import pygame
import sys
import os


filename = "game assets/" + 'PingPong.ttf'


def print_text(self, message, x, y, font_color=(23, 41, 32), font_type=filename,
               font_size=30):  # печать текста на экран
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    self.win.blit(text, (x, y))


class MainMenu:
    def __init__(self, win):
        pygame.display.set_icon(pygame.image.load("game assets/icon.png").convert_alpha())
        self.empty_btn = pygame.image.load(os.path.join("game assets", "empty.png")).convert_alpha()
        self.logo = pygame.transform.scale(pygame.image.load(os.path.join("game assets", "logo.png")).convert_alpha(), (500, 500))
        self.logo_2 = pygame.transform.flip(pygame.transform.scale(pygame.image.load(os.path.join("game assets", "logo_2.png")).convert_alpha(),
                                           (475, 475)), True, False)
        self.logo_3 = pygame.transform.scale(pygame.image.load(os.path.join("game assets", "icon.png")).convert_alpha(),
                                           (200, 200))
        self.width = 1350
        self.height = 700
        self.bg = pygame.image.load(os.path.join("game assets", "start.png"))
        self.bg = pygame.transform.scale(self.bg, (self.width, self.height))
        self.win = win
        self.btn_start = (self.width/2 - self.empty_btn.get_width()/2, 200, self.empty_btn.get_width(), self.empty_btn.get_height())
        self.btn_quit = (self.width / 2 - self.empty_btn.get_width() / 2, 300, self.empty_btn.get_width(), self.empty_btn.get_height())

    def run(self):
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    if self.btn_start[0] <= x <= self.btn_start[0] + self.btn_start[2]:
                        if self.btn_start[1] <= y <= self.btn_start[1] + self.btn_start[3]:
                            game = Game(self.win)
                            game.run()
                            del game
                    if self.btn_quit[0] <= x <= self.btn_quit[0] + self.btn_quit[2]:
                        if self.btn_quit[1] <= y <= self.btn_quit[1] + self.btn_quit[3]:
                            pygame.quit()
                            sys.exit()
            self.draw()

        pygame.quit()

    def draw(self):
        x, y = pygame.mouse.get_pos()
        self.win.blit(self.bg, (0, 0))
        self.win.blit(self.logo, (75, 100))
        self.win.blit(self.logo_2, (800, 100))
        self.win.blit(self.logo_3, (575, 0))
        self.win.blit(self.empty_btn, (self.btn_start[0], self.btn_start[1]))
        self.win.blit(self.empty_btn, (self.btn_quit[0], self.btn_quit[1]))
        if self.btn_start[0] <= x <= self.btn_start[0] + self.btn_start[2] and self.btn_start[1] <= y <= self.btn_start[1] + self.btn_start[3]:
            print_text(self, message='PLAY', x=self.width / 2 - self.empty_btn.get_width() / 2 + 60, y=203,
                       font_size=60, font_color='grey')
        else:
            print_text(self, message='PLAY', x=self.width / 2 - self.empty_btn.get_width() / 2 + 60, y=203,
                       font_size=60, font_color='white')

        if self.btn_quit[0] <= x <= self.btn_quit[0] + self.btn_quit[2] and self.btn_quit[1] <= y <= self.btn_quit[1] + self.btn_quit[3]:
            print_text(self, message='Quit', x=self.width / 2 - self.empty_btn.get_width() / 2 + 50, y=303,
                       font_size=60, font_color='grey')
        else:
            print_text(self, message='Quit', x=self.width / 2 - self.empty_btn.get_width() / 2 + 50, y=303, font_size=60, font_color='white')
        pygame.display.update()