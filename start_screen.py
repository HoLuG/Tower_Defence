from game import Game
import pygame
import os


class MainMenu:
    def __init__(self, win):
        self.start_btn = pygame.image.load(os.path.join("game assets", "play.png")).convert_alpha()
        self.width = 1350
        self.height = 700
        self.bg = pygame.image.load(os.path.join("game assets", "start.png"))
        self.bg = pygame.transform.scale(self.bg, (self.width, self.height))
        self.win = win
        self.btn = (self.width/2 - self.start_btn.get_width()/2, 350, self.start_btn.get_width(), self.start_btn.get_height())

    def run(self):
        run = True

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONUP:
                    # check if hit start btn
                    x, y = pygame.mouse.get_pos()

                    if self.btn[0] <= x <= self.btn[0] + self.btn[2]:
                        if self.btn[1] <= y <= self.btn[1] + self.btn[3]:
                            game = Game(self.win)
                            game.run()
                            del game
            self.draw()

        pygame.quit()

    def draw(self):
        self.win.blit(self.bg, (0, 0))
        self.win.blit(self.start_btn, (self.btn[0], self.btn[1]))
        pygame.display.update()