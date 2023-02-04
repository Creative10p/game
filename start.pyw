import pygame
import sys
import os

pygame.init()
FPS = 50
WIDTH, HEIGHT = WINDOW_SIZE = 400, 300
screen = pygame.display.set_mode(WINDOW_SIZE)


def load_image(filename, colorkey=None):
    fullname = filename
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    fon = pygame.transform.scale(load_image(r'images\back.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 60)
    string_rendered = font.render("Новая игра", True, "black")
    screen.blit(string_rendered, (87, 80))
    string_rendered = font.render("Прогресс", True, "black")
    screen.blit(string_rendered, (100, 180))


def action_on_the_first_screen(position):
    global current_screen
    if 80 <= position[0] <= 300 and 80 <= position[1] <= 120:
        fon = pygame.transform.scale(load_image(r'images\back.png'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 56)
        string_rendered = font.render("Игра с другом", True, "black")
        screen.blit(string_rendered, (60, 40))
        string_rendered = font.render("Игра с легким ИИ", True, "black")
        screen.blit(string_rendered, (35, 140))
        string_rendered = font.render("Игра со сложным ИИ", True, "black")
        screen.blit(string_rendered, (0, 235))
        current_screen = 'second'
    elif 80 <= position[0] <= 290 and 180 <= position[1] <= 220:
        os.startfile("progress1.pyw")
        current_screen = 'second'
        sys.exit()


def action_on_the_second_screen(position):
    if 60 <= position[0] <= 340 and 40 <= position[1] <= 80:
        os.startfile("local_multiplayer.pyw")
        sys.exit()
    if 35 <= position[0] <= 370 and 140 <= position[1] <= 180:
        os.startfile("easy_AI.pyw")
        sys.exit()
    if 0 <= position[0] <= 400 and 235 <= position[1] <= 270:
        os.startfile('hard_AI.pyw')
        sys.exit()


clock = pygame.time.Clock()
start_screen()
current_screen = 'first'
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            if current_screen == "first":  # если главный экран
                action_on_the_first_screen(event.pos)
            elif current_screen == "second":
                action_on_the_second_screen(event.pos)
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
