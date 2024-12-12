import pygame
import random
import tkinter as tk
from tkinter import messagebox


screen_width = 300
screen_height = 600
block_size = 30  #  размер одного блока в пикселях

board_width = screen_width // block_size  # количество столбцов на экране в данном случае 10
board_height = screen_height // block_size  # количество строк на экране в данном случае 20

# цвета
colors = [
    (0, 0, 0),  # черный
    (255, 0, 0),  # красный
    (0, 255, 0),  # зеленый
    (0, 0, 255),  # синий
    (255, 255, 0),  # желтый
    (255, 165, 0),  # оранжевый
    (128, 0, 128)  # фиолетовый
]

# формы фигурок, которые падают в тетрисе
shapes = [
    [[1], [1], [1], [1]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 1], [0, 1, 0]]
]

class Tetromino:
    def __init__(self):
        self.shape = random.choice(shapes)  # выбирается случайная фигура из списка
        self.color = random.randint(1, len(colors) - 1)
        self.x = board_width // 2 - len(self.shape[0]) // 2  # тетромины должны спускаться сверху экрана по середине
        self.y = 0

    # поворот фигурок tetromino
    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]


class Tetris():
    def __init__(self):
        self.board = [[0]*board_width for _ in range(board_height)]  # инициализируется двумерный список состоящиий
        # из нулей по 10 в строке и строк 20
        self.current_tetromino = Tetromino()
        self.next_tetromino = Tetromino()
        self.score = 0
        self.game_over = False

    def collide(self):
        for y in range(len(self.current_tetromino.shape)):
            for x in range(len(self.current_tetromino.shape[y])):
                if self.current_tetromino.shape[y][x]:  # есть ли блок в текущей позиции тетромино, т.е. равно 1
                    if (self.current_tetromino.x + x < 0 or
                    self.current_tetromino.x + x >= board_width or
                    self.current_tetromino.y + y >= board_height or
                    self.board[self.current_tetromino.y + y][self.current_tetromino.x + x]):  # проверяет занята ли
                        # ячейка на игровом поле, куда будет помещен блок текущего тетромино
                        return True
        return False

    # фиксация текущего тетромино на игровом поле и окрашивается в определенный цвет
    def merge(self):
        for y in range(len(self.current_tetromino.shape)):
            for x in range(len(self.current_tetromino.shape[y])):
                if self.current_tetromino.shape[y][x]:
                    self.board[self.current_tetromino.y + y][
                        self.current_tetromino.x + x] = self.current_tetromino.color  #здесь присваивается рандомный
                    # индекс. По какому принципу он дальше закрашивает фигуру мне не понятно????

    # очистка заполненых линий
    def clear_lines(self):
        clear_lines = []
        for y in range(board_height):
            if all(self.board[y]):  # метод all() проверяет являются ли все элементы истиными, т.е. равными 1
                clear_lines.append(y)

        for y in clear_lines:
            del self.board[y]
            self.board.insert(0, [0]*board_width)
            self.score += 100


    # появление новой фигурки тетриса. Если сразу столкновение, то игра закончена
    def new_tetromino(self):
        self.current_tetromino = self.next_tetromino
        self.next_tetromino = Tetromino()
        if self.collide():  # понимается столкновение и дальше не может появиться следующая фигурка
            print('GAME OVER')
            self.game_over = True
            show_game_over(self.score)

def draw_board(screen, board):
    for y in range(board_height):
        for x in range(board_width):
            color = colors[board[y][x]]
            pygame.draw.rect(screen, color, (x*block_size, y*block_size, block_size-1, block_size-1))

def draw_tetromino(screen, tetromino):
    for y in range(len(tetromino.shape)):
        for x in range(len(tetromino.shape[y])):
            if tetromino.shape[y][x]:
                color = colors[tetromino.color]
                pygame.draw.rect(screen, color,
                            ((tetromino.x+x)*block_size, (tetromino.y+y)*block_size,
                                  block_size-1, block_size-1))  # отрисовка блоков фигуры

def draw_next_tetromino(screen, tetromino):
    offset_x = board_width + 1
    offset_y = 2

    for y in range(len(tetromino.shape)):
        for x in range(len(tetromino.shape[y])):
            if tetromino.shape[y][x]:
                color = colors[tetromino.color]
                pygame.draw.rect(screen, color,
                            ((offset_x+x)*block_size, (offset_y+y)*block_size,
                                  block_size-1, block_size-1))  # отрисовка блоков фигуры

def show_game_over(score):
    root = tk.Tk()
    root.withdraw()  # скрыть основное окно
    messagebox.showinfo(title='GAME OVER', message=f'Игра окончена!!! Ты набрал {score} очков')
    root.destroy()


def main():
    pygame.init()
    screen = pygame.display.set_mode((screen_width + block_size*5, screen_height))
    pygame.display.set_caption('Tetris Game')
    clock = pygame.time.Clock()
    tetris = Tetris()
    running = True
    while running:

        # заполняем экран черным цветом и проводим разделяющую линию
        screen.fill(colors[0])
        line_x = screen_width
        pygame.draw.line(screen, colors[6], (line_x, 0), (line_x, screen_height), 2)

        for event in pygame.event.get():  # pygame.event.get() используется для извлечения событий с момента
            # последнего вызова
            if event.type == pygame.QUIT:
                running = False
            if not tetris.game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        tetris.current_tetromino.x -= 1
                        if tetris.collide():
                            tetris.current_tetromino.x += 1

                    elif event.key == pygame.K_RIGHT:
                        tetris.current_tetromino.x += 1
                        if tetris.collide():
                            tetris.current_tetromino.x -= 1

                    elif event.key == pygame.K_DOWN:
                        tetris.current_tetromino.y += 1
                        if tetris.collide():
                            tetris.current_tetromino.y -= 1

                    elif event.key == pygame.K_UP:
                        tetris.current_tetromino.rotate()
                        if tetris.collide():
                            tetris.current_tetromino.rotate()
        if not tetris.game_over:
            tetris.current_tetromino.y += 1

            if tetris.collide():
                tetris.current_tetromino.y -= 1
                tetris.merge()
                tetris.clear_lines()
                tetris.new_tetromino()

        draw_board(screen, tetris.board)

        if not tetris.game_over:
            draw_tetromino(screen, tetris.current_tetromino)
        draw_next_tetromino(screen, tetris.next_tetromino)

        # размещение значения переменных на экране
        font = pygame.font.Font(None, 30)
        score = font.render(f'Счет {tetris.score}', True, (0, 255, 0))
        screen.blit(score, (350, 5))

        pygame.display.flip()  # обновляет содержимое на экране
        clock.tick(2)


if __name__ == "__main__":
    main()
