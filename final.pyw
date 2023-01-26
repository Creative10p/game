import os
import sys
import pygame


pygame.init()
size = width, height = 600, 600
screen = pygame.display.set_mode(size)


def load_image(filename, colorkey=None):
    fullname = f"images\{filename}"
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
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


class Cross_sprite(pygame.sprite.Sprite):
    image = load_image("cross.png")

    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = Cross_sprite.image
        self.rect = self.image.get_rect()
        self.rect.topleft = position

    def render(self, screen):
        screen.blit(self.image, self.rect)

    def rotate(self):
        self.rect.topleft = (self.rect.topleft[0]+10, self.rect.topleft[1]+10)
        self.image = load_image("cross_3.png")

    def update(self):
        self.rect.y += 15

    def check_place(self):
        if self.rect.topleft[1] < 600:
            return True
        else:
            return False

class Zero_sprite(pygame.sprite.Sprite):
    image = load_image("zero.png")

    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = Zero_sprite.image
        self.rect = self.image.get_rect()
        self.rect.topleft = position

    def render(self, screen):
        screen.blit(self.image, self.rect)

    def rotate(self):
        self.rect.topleft = (self.rect.topleft[0]+10, self.rect.topleft[1]+10)

    def update(self):
        self.rect.y += 15

    def check_place(self):
        if self.rect.topleft[1] < 600:
            return True
        else:
            return False

class Scene_cross:
    def draw(screen):
        pygame.display.set_mode((600, 630))
        screen.fill('black')
        pygame.mixer.music.load(r'audio\X_wins.mp3')
        pygame.mixer.music.play()
        for i in range(256):
            pygame.draw.polygon(screen, (i, 0, 0), [[0, 50], [0, 0], [50, 0], [600, 550], [600, 600], [550, 600]])
            pygame.draw.polygon(screen, (i, 0, 0), [[550, 0], [600, 0], [600, 50], [50, 600], [0, 600], [0, 550]])
            pygame.display.flip()
            pygame.time.delay(10)

class Scene_zero:
    def draw(screen):
        pygame.display.set_mode((600, 630))
        screen.fill('black')
        pygame.mixer.music.load(r'audio\Zero_wins.mp3')
        pygame.mixer.music.play()
        for i in range(256):
            pygame.draw.circle(screen, (0, 0, i), (300,300), 300, 30)
            pygame.display.flip()
            pygame.time.delay(10)

class Scene_draw:
    def draw(screen):
        pygame.display.set_mode((600, 630))
        screen.fill('black')
        for i in range(256):
            pygame.draw.circle(screen, (0, 0, i), (150, 150), 100, 10)
            pygame.draw.line(screen, (i, 0, 0), (350, 350), (550, 550), 10)
            pygame.draw.line(screen, (i, 0, 0), (550, 350), (350, 550), 10)
            pygame.display.flip()
            pygame.time.delay(10)

map = []
with open(r'results_of_game\results.txt', 'r') as f:
    m = f.readlines()
winner = m[1]
for i in range(0, 9, 3):
    if m[0][i] != '\n':
        map.append([m[0][i], m[0][i+1], m[0][i+2]])
number_of_crosses, number_of_zeros = 0, 0
array_of_symbols = []
first = ""
for i in range(3):
    for j in range(3):
        if map[i][j] == "x":
            if number_of_crosses == 0:
                cross = Cross_sprite((j*200, i*200))
                number_of_crosses += 1
                array_of_symbols.append(cross)
                if first == "":
                    first = "x"
            elif number_of_crosses == 1:
                cross1 = Cross_sprite((j*200, i*200))
                array_of_symbols.append(cross1)
                number_of_crosses += 1
            elif number_of_crosses == 2:
                cross2 = Cross_sprite((j*200, i*200))
                number_of_crosses += 1
                array_of_symbols.append(cross2)
            elif number_of_crosses == 3:
                cross3 = Cross_sprite((j*200, i*200))
                number_of_crosses += 1
                array_of_symbols.append(cross3)
            else:
                cross4 = Cross_sprite((j*200, i*200))
                number_of_crosses += 1
                array_of_symbols.append(cross4)
        if map[i][j] == "o":
            if number_of_zeros == 0:
                zero = Zero_sprite((j*200, i*200))
                number_of_zeros += 1
                array_of_symbols.append(zero)
                if first == "":
                    first = 'o'
            elif number_of_zeros == 1:
                zero1 = Zero_sprite((j*200, i*200))
                number_of_zeros += 1
                array_of_symbols.append(zero1)
            elif number_of_zeros == 2:
                zero2 = Zero_sprite((j*200, i*200))
                number_of_zeros += 1
                array_of_symbols.append(zero2)
            elif number_of_zeros == 3:
                zero3 = Zero_sprite((j*200, i*200))
                number_of_zeros += 1
                array_of_symbols.append(zero3)
            else:
                zero4 = Zero_sprite((j*200, i*200))
                number_of_zeros += 1
                array_of_symbols.append(zero4)

fps = 60  # количество кадров в секунду
clock = pygame.time.Clock()
running = True
f = False
n = 0
fend = False
while running:  # главный игровой цикл
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if fend and (event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN):
            os.startfile("start.pyw")
            sys.exit()
    # формирование кадра
    # ...
    screen.fill("black")
    if not fend:
        pygame.draw.line(screen, 'white', (200, 0), (200, 600))
        pygame.draw.line(screen, 'white', (400, 0), (400, 600))
        pygame.draw.line(screen, 'white', (0, 200), (600, 200))
        pygame.draw.line(screen, 'white', (0, 400), (600, 400))
    for e in array_of_symbols:
        e.render(screen)
    if not f and n == 30:
        for e in array_of_symbols:
            e.rotate()
        f = True
    if f:
        for e in array_of_symbols:
            e.update()
        if not fend:
            if first == "x":
                if cross.check_place() == False:
                    screen.fill('black')
                    if winner == 'cross':
                        Scene_cross.draw(screen)
                        fend = True
                    elif winner == 'zero':
                        Scene_zero.draw(screen)
                        fend = True
                    else:
                        Scene_draw.draw(screen)
                        fend = True
            elif first == "o":
                if zero.check_place() == False:
                    if winner == 'cross':
                        Scene_cross.draw(screen)
                        fend = True
                    elif winner == 'zero':
                        Scene_zero.draw(screen)
                        fend = True
                    else:
                        Scene_draw.draw(screen)
                        fend = True
    if fend:
        if winner == 'cross':
            pygame.draw.polygon(screen, (255, 0, 0), [[0, 50], [0, 0], [50, 0], [600, 550], [600, 600], [550, 600]])
            pygame.draw.polygon(screen, (255, 0, 0), [[550, 0], [600, 0], [600, 50], [50, 600], [0, 600], [0, 550]])
        elif winner == 'zero':
            pygame.draw.circle(screen, (0, 0, 255), (300, 300), 300, 30)
        else:
            pygame.draw.circle(screen, (0, 0, 255), (150, 150), 100, 10)
            pygame.draw.line(screen, (255, 0, 0), (350, 350), (550, 550), 10)
            pygame.draw.line(screen, (255, 0, 0), (550, 350), (350, 550), 10)
        font = pygame.font.Font(None, 30)
        string_rendered = font.render("Нажмите любую кнопку, чтобы вернуться на главный экран", 1, "white")
        screen.blit(string_rendered, (0, 600))
    pygame.display.flip()  # смена кадра
    clock.tick(fps)
    n += 1
pygame.quit()