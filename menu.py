import pygame
import os
pygame.font.init()


filename = "game assets/" + 'PingPong.ttf'


def print_text(message, x, y, font_color=(23, 41, 32), font_type=filename, font_size=30):  # печать текста на экран
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    screen.blit(text, (x, y))


class Button:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.inactive_colour = (82, 91, 209)
        self.active_colour = (51, 62, 191)

    def draw(self, x, y, message, font_size=30):
        mouse = pygame.mouse.get_pos()
        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pygame.draw.rect(screen, self.active_colour, (x, y, self.width, self.height))
        else:
            pygame.draw.rect(screen, self.inactive_colour, (x, y, self.width, self.height))

        print_text(message=message, x=x + 10, y=y + 10, font_size=font_size)


def start_screen():  # стартовое меню
    global flag_menu, win, flag, screen

    FPS = 50
    clock = pygame.time.Clock()
    pygame.display.set_icon(pygame.image.load("game assets/start.png").convert_alpha())  # создание иконки игры

    start_btn = Button(280, 60)
    quit_btn = Button(120, 60)
    load_btn = Button(280, 60)
    control_btn = Button(220, 60)
    highscores_btn = Button(280, 60)
    back_btn = Button(120, 60)


start_screen()


