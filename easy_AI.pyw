import pygame
import sys
import os
import random
import sqlite3

pygame.init()
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 600, 600
FPS = 30
screen = pygame.display.set_mode(WINDOW_SIZE)
map = []
winner = ''
res = ''

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

class Arm(pygame.sprite.Sprite):
    image = load_image("images\Arm2.png")

    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = Arm.image
        self.rect = self.image.get_rect()
        self.rect.topleft = position

    def render(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, direction):
        if direction == 'вниз':
            self.rect.y += 1
        else:
            self.rect.x += 1

class Pitch:
    def render_pitch(screen):
        arm = Arm((200, 0))
        arm.render(screen)
        for i in range(599):
            screen.fill('black')
            pygame.draw.line(screen, "white", (200, 0), (200, i))
            pygame.draw.line(screen, "white", (200, i), (200, i + 1))
            arm.update('вниз')
            arm.render(screen)
            pygame.display.flip()
        arm = Arm((400, 0))
        arm.render(screen)
        for i in range(599):
            screen.fill('black')
            pygame.draw.line(screen, "white", (200, 0), (200, 600))
            pygame.draw.line(screen, "white", (400, 0), (400, i))
            pygame.draw.line(screen, "white", (400, i), (400, i + 1))
            arm.update('вниз')
            arm.render(screen)
            pygame.display.flip()
        arm = Arm((0, 200))
        arm.render(screen)
        for i in range(599):
            screen.fill('black')
            pygame.draw.line(screen, "white", (200, 0), (200, 600))
            pygame.draw.line(screen, "white", (400, 0), (400, 600))
            pygame.draw.line(screen, "white", (0, 200), (i, 200))
            pygame.draw.line(screen, "white", (i, 200), (i + 1, 200))
            arm.update('вправо')
            arm.render(screen)
            pygame.display.flip()
        arm = Arm((0, 400))
        arm.render(screen)
        for i in range(599):
            screen.fill('black')
            pygame.draw.line(screen, "white", (200, 0), (200, 600))
            pygame.draw.line(screen, "white", (400, 0), (400, 600))
            pygame.draw.line(screen, "white", (0, 200), (600, 200))
            pygame.draw.line(screen, "white", (0, 400), (i, 400))
            pygame.draw.line(screen, "white", (i, 400), (i+1, 400))
            arm.update('вправо')
            arm.render(screen)
            pygame.display.flip()

class Cross:
    def __init__(self, start_position):
        self.start_position = (start_position[0], start_position[1])

    def render(self, screen):
        xo, yo = self.start_position[0]+2, self.start_position[1]+2
        for i in range(196):
            pygame.draw.line(screen, "red", (xo, yo), (xo+2, yo))
            xo += 1
            yo += 1
            pygame.display.flip()
        xo, yo = self.start_position[0] + 198, self.start_position[1]+2
        for i in range(196):
            pygame.draw.line(screen, "red", (xo, yo), (xo - 2, yo))
            xo -= 1
            yo += 1
            pygame.display.flip()

class Zero:
    def __init__(self, position):
        self.position = position

    def render(self, screen):
        xo, yo, r = self.position[0], self.position[1]+1, 99
        array_of_y = []
        for x in range(99):
            y = ((r ** 2 - x ** 2) ** 0.5)
            array_of_y.append(y)
            pygame.draw.circle(screen, "blue", (xo+x, yo-y), 1)
            pygame.display.flip()
        for x in range(98, -1, -1):
            pygame.draw.circle(screen, "blue", (xo+x, yo+array_of_y[x]), 1)
            pygame.display.flip()
        for x in range(99):
            pygame.draw.circle(screen, "blue", (xo-x, yo+array_of_y[x]), 1)
            pygame.display.flip()
        for x in range(98, -1, -1):
            pygame.draw.circle(screen, "blue", (xo-x, yo-array_of_y[x]), 1)
            pygame.display.flip()
        pygame.draw.circle(screen, "blue", (xo, yo), 99, 2)


# игра со слабым ИИ
class Easy_AI_game:
    def __init__(self):
        global current_player

        self.current_player = random.choice(['AI', 'real player'])
        current_player = self.current_player
        self.real_player_sign = random.choice(['x', 'o'])
        if self.real_player_sign == 'x':
            self.ai_sign = 'o'
        else:
            self.ai_sign = 'x'
        self.map = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]

    def action(self, position=(0, 0)):
        if self.current_player == 'real player':
            self.position = position
            if self.position[0] < 200:
                self.start_position = (0, 0)
            elif self.position[0] < 400:
                self.start_position = (200, 0)
            else:
                self.start_position = (400, 0)
            if self.position[1] < 200:
                self.start_position = (self.start_position[0], 0)
            elif self.position[1] < 400:
                self.start_position = (self.start_position[0], 200)
            else:
                self.start_position = (self.start_position[0], 400)
            self.render_position = (self.start_position[1] // 200, self.start_position[0] // 200)
            if self.map[self.render_position[0]][self.render_position[1]] == " " and not game_over:
                if self.real_player_sign == 'x':
                    cross = Cross(self.start_position)
                    cross.render(screen)
                else:
                    self.circle_render_position = (((self.start_position[0] + self.start_position[0] + 200) / 2),
                                                   ((self.start_position[1] + self.start_position[1] + 200) / 2))
                    zero = Zero(self.circle_render_position)
                    zero.render(screen)
                self.map[self.render_position[0]][self.render_position[1]] = self.real_player_sign
                self.current_player = 'AI'
                self.check_win()
                self.action()
        elif not game_over:
            self.x, self.y = -1, -1
            for i in range(3):
                if self.map[i][0] == self.map[i][1] != " " and self.map[i][2] == " ":
                    self.x, self.y = 2, i
                elif self.map[i][0] == self.map[i][2] != " " and self.map[i][1] == " ":
                    self.x, self.y = 1, i
                elif self.map[i][1] == self.map[i][2] != " " and self.map[i][0] == " ":
                    self.x, self.y = 0, i
                elif self.map[0][i] == self.map[1][i] != " " and self.map[2][i] == " ":
                    self.x, self.y = i, 2
                elif self.map[0][i] == self.map[2][i] != " " and self.map[1][i] == " ":
                    self.x, self.y = i, 1
                elif self.map[1][i] == self.map[2][i] != " " and self.map[0][i] == " ":
                    self.x, self.y = i, 0
            if self.x == -1 and self.map[1][1] != " ":
                if self.map[0][0] == self.map[1][1] and self.map[2][2] == " ":
                    self.x, self.y = 2, 2
                elif self.map[0][2] == self.map[1][1] and self.map[2][0] == " ":
                    self.x, self.y = 0, 2
                elif self.map[2][0] == self.map[1][1] and self.map[0][2] == " ":
                    self.x, self.y = 2, 0
                elif self.map[2][2] == self.map[1][1] and self.map[0][0] == " ":
                    self.x, self.y = 0, 0
            if self.x == -1:
                self.x, self.y = random.randint(0, 2), random.randint(0, 2)
                while self.map[self.y][self.x] != " ":
                    self.x, self.y = random.randint(0, 2), random.randint(0, 2)
            if self.ai_sign == "x":
                self.start_position = (self.x*200, self.y*200)
                cross = Cross(self.start_position)
                cross.render(screen)
            else:
                self.circle_render_position = (((self.x*200 + self.x*200 + 200) / 2),
                                               ((self.y*200 + self.y*200 + 200) / 2))
                zero = Zero(self.circle_render_position)
                zero.render(screen)
            self.map[self.y][self.x] = self.ai_sign
            self.current_player = 'real player'
            self.check_win()

    def check_free_places(self):
        for i in range(3):
            for j in range(3):
                if self.map[i][j] == " ":
                    return True
        return False

    def check_win(self):
        global game_over
        global map
        global winner
        global res
        if ((self.map[0][0] == 'x' and self.map[0][1] == 'x' and self.map[0][2] == 'x') or
                (self.map[1][0] == 'x' and self.map[1][1] == 'x' and self.map[1][2] == 'x') or
                (self.map[2][0] == 'x' and self.map[2][1] == 'x' and self.map[2][2] == 'x') or
                (self.map[0][0] == 'x' and self.map[1][0] == 'x' and self.map[2][0] == 'x') or
                (self.map[0][1] == 'x' and self.map[1][1] == 'x' and self.map[2][1] == 'x') or
                (self.map[0][2] == 'x' and self.map[1][2] == 'x' and self.map[2][2] == 'x') or
                (self.map[0][0] == 'x' and self.map[1][1] == 'x' and self.map[2][2] == 'x') or
                (self.map[0][2] == 'x' and self.map[1][1] == 'x' and self.map[2][0] == 'x')):
            print('X - победитель')
            winner = 'cross'
            if self.real_player_sign == 'x':
                res = 'win'
            else:
                res = 'defeat'
            game_over = True
        elif not game_over and ((self.map[0][0] == 'o' and self.map[0][1] == 'o' and self.map[0][2] == 'o') or
                (self.map[1][0] == 'o' and self.map[1][1] == 'o' and self.map[1][2] == 'o') or
                (self.map[2][0] == 'o' and self.map[2][1] == 'o' and self.map[2][2] == 'o') or
                (self.map[0][0] == 'o' and self.map[1][0] == 'o' and self.map[2][0] == 'o') or
                (self.map[0][1] == 'o' and self.map[1][1] == 'o' and self.map[2][1] == 'o') or
                (self.map[0][2] == 'o' and self.map[1][2] == 'o' and self.map[2][2] == 'o') or
                (self.map[0][0] == 'o' and self.map[1][1] == 'o' and self.map[2][2] == 'o') or
                (self.map[0][2] == 'o' and self.map[1][1] == 'o' and self.map[2][0] == 'o')):
            print('O - победитель')
            winner = 'zero'
            if self.real_player_sign == 'o':
                res = 'win'
            else:
                res = 'defeat'
            game_over = True
        elif self.check_free_places() == False:
            print('Ничья!')
            game_over = True
            winner = 'draw'
        if game_over:
            map = self.map.copy()

clock = pygame.time.Clock()
current_player = None
end = False
render = False
game = Easy_AI_game()
if current_player == "AI":
    first_move = False
game_over = False
running = True
while running:  # главный игровой цикл
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            game.action(event.pos)
    if not render:
        Pitch.render_pitch(screen)
        render = True
    elif render:
        pygame.draw.line(screen, "white", (200, 0), (200, 600))
        pygame.draw.line(screen, "white", (400, 0), (400, 600))
        pygame.draw.line(screen, "white", (0, 200), (600, 200))
        pygame.draw.line(screen, "white", (0, 400), (600, 400))
    if current_player == "AI":
        if not first_move:
            game.action()
            first_move = True
    if game_over and not end:
        for i in range(3):
            for j in range(3):
                if map[i][j] == ' ':
                    map[i][j] = 'n'
        with open(r'results_of_game\results.txt', 'w') as f:
            for e in map:
                for e2 in e:
                    f.write(e2)
            f.write('\n')
            f.write(winner)
        con = sqlite3.connect("results_of_game\progress.db")
        cur = con.cursor()
        result = cur.execute("""select * from progress""").fetchall()
        result2 = cur.execute(f"""UPDATE progress
                SET count_of_games = {result[0][0] + 1}""").fetchall()
        if res == 'win':
            result2 = cur.execute(f"""UPDATE progress
            SET count_of_wins = {result[0][1] + 1}""").fetchall()
            result2 = cur.execute(f"""UPDATE progress
            SET current_win_streak = {result[0][4] + 1}""").fetchall()
            if result[0][4]+1 > result[0][5]:
                result2 = cur.execute(f"""UPDATE progress
                            SET maximum_win_streak = {result[0][3]+1}""").fetchall()
        elif res == 'defeat':
            result2 = cur.execute(f"""UPDATE progress
                        SET count_of_defeats = {result[0][2] + 1}""").fetchall()
            result2 = cur.execute(f"""UPDATE progress
                        SET current_win_streak = 0""").fetchall()
        else:
            result2 = cur.execute(f"""UPDATE progress
                                    SET count_of_draws = {result[0][3] + 1}""").fetchall()
        con.commit()
        os.startfile('final.pyw')
        end = True
        sys.exit()
    # обновляем положение всех спрайтов
    pygame.display.flip()  # смена кадра
    clock.tick(FPS)
pygame.quit()