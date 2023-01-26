import pygame
import sys
import os
import sqlite3

pygame.init()
FPS = 60
WIDTH, HEIGHT = WINDOW_SIZE = 530, 300
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

def progress_screen():
    con = sqlite3.connect("results_of_game\progress.db")
    cur = con.cursor()
    result = cur.execute("""select * from progress""").fetchall()
    con.commit()
    font = pygame.font.Font(None, 50)
    string_rendered = font.render(f"Количество игр - {result[0][0]}", 1, "white")
    screen.blit(string_rendered, (0, 10))
    string_rendered = font.render(f"Количество побед - {result[0][1]}", 1, "white")
    screen.blit(string_rendered, (0, 50))
    string_rendered = font.render(f"Количество поражений - {result[0][2]}", 1, "white")
    screen.blit(string_rendered, (0, 90))
    string_rendered = font.render(f"Количество ничьих - {result[0][3]}", 1, "white")
    screen.blit(string_rendered, (0, 130))
    string_rendered = font.render(f"Текущая серия побед - {result[0][4]}", 1, "white")
    screen.blit(string_rendered, (0, 170))
    string_rendered = font.render(f"Максимальная серия побед - {result[0][5]}", 1, "white")
    screen.blit(string_rendered, (0, 210))
    font = pygame.font.Font(None, 30)
    string_rendered = font.render("Нажмите Esc, чтобы вернуться на главный экран", 1, "white")
    screen.blit(string_rendered, (0, 270))

clock = pygame.time.Clock()
screen.fill('black')
progress_screen()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                os.startfile("start.pyw")
                sys.exit()
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()