import random
import pygame
import copy


WINDOW = pygame.display.set_mode([400, 400])
BOARD_IMAGE = pygame.image.load("board.png").convert()
PIECES_IMAGE = pygame.image.load("pieces.png").convert_alpha()
PIECE_SPRITES = []
for i in range(0, 12):
    PIECE_SPRITES.append(PIECES_IMAGE.subsurface([i % 6 * 50, int(i/6)*50, 50, 50]))

class Piece:
    def __init__(self, color, position):
        self.position = position
        self.color = color
        self.available_moves = []

    def add_move(self, position):
        self.available_moves.append(Move(self, new_position(self.position, position)))

    def check_move(self, position):
        return check_square(new_position(self.position, position))

    def add_cardinal_moves(self):
        own_color = self.color
        enemy_color = 1 if self.color == 0 else 0
        for x in range(0, 4):
            for i in range(1, 8):
                directions = [[0, i], [0, -i], [i, 0], [-i, 0]]
                current_dir = directions[x]
                current_move = self.check_move(current_dir)
                if current_move is None:
                    break
                if current_move == -1:
                    self.add_move(current_dir)
                    continue
                if current_move == enemy_color:
                    self.add_move(current_dir)
                    break
                if current_move == own_color:
                    break

    def add_diagonal_moves(self):
        own_color = self.color
        enemy_color = 1 if self.color == 0 else 0
        for x in range(0, 4):
            for i in range(1, 8):
                directions = [[i, i], [i, -i], [-i, i], [-i, -i]]
                current_dir = directions[x]
                current_move = self.check_move(current_dir)
                if current_move is None:
                    break
                if current_move == -1:
                    self.add_move(current_dir)
                    continue
                if current_move == enemy_color:
                    self.add_move(current_dir)
                    break
                if current_move == own_color:
                    break




class Pawn(Piece):
    def __init__(self):
        self.id = 0
        self.already_moved = False

    def get_moves(self):
        self.available_moves = []
        y = 1 if self.color == 0 else -1

        if self.check_move([0, y]) == -1:
            self.add_move([0, y])

        if not self.already_moved:
            if self.check_move([0, y * 2]) == -1 and self.check_move([0, y]) == -1:
                self.add_move([0, y * 2])

        if self.check_move([1, y]) == 1 and self.color == 0 or self.check_move([1, y]) == 0 and self.color == 1:
            self.add_move([1, y])

        if self.check_move([-1, y]) == 1 and self.color == 0 or self.check_move([-1, y]) == 0 and self.color == 1:
            self.add_move([-1, y])


class Rook(Piece):
    def __init__(self):
        self.id = 1

    def get_moves(self):
        self.available_moves = []
        self.add_cardinal_moves()


class Knight(Piece):
    def __init__(self):
        self.id = 2

    def get_moves(self):
        self.available_moves = []
        moves = [[1, -2], [2, -1], [2, 1], [1, 2], [-1, 2], [-2, 1], [-2, -1], [-1, -2]]
        own_color = self.color
        enemy_color = 1 if self.color == 0 else 0
        for i in moves:
            current_move = self.check_move(i)
            if current_move is None:
                continue
            if current_move == -1:
                self.add_move(i)
                continue
            if current_move == enemy_color:
                self.add_move(i)
                continue
            if current_move == own_color:
                continue



class Bishop(Piece):
    def __init__(self):
        self.id = 3

    def get_moves(self):
        self.available_moves = []
        self.add_diagonal_moves()


class Queen(Piece):
    def __init__(self):
        self.id = 4

    def get_moves(self):
        self.available_moves = []
        self.add_diagonal_moves()
        self.add_cardinal_moves()


class King(Piece):
    def __init__(self):
        self.id = 5

    def get_moves(self):
        self.available_moves = []
        own_color = self.color
        enemy_color = 1 if self.color == 0 else 0
        for y in range(0, 2):
            for x in range(0, 2):
                if y == 1 and x == 1:
                    continue
                current_move = self.check_move([x, y])
                if current_move is None:
                    continue
                if current_move == -1:
                    self.add_move([x, y])
                    continue
                if current_move == enemy_color:
                    self.add_move([x, y])
                    continue
                if current_move == own_color:
                    continue


class Move:
    def __init__(self, piece, end_position):
        self.piece = piece
        self.init_position = piece.position
        self.end_position = end_position

    def move(self, board):
        board[self.init_position[1]][self.init_position[0]] = -1
        board[self.end_position[1]][self.end_position[0]] = self.piece
        self.piece.position = self.end_position
        if self.piece.id == 1:
            self.piece.already_moved = True
        if self.piece.id == 0 and self.piece.color == 0 and self.piece.position[1] == 7:
            board[self.end_position[1]][self.end_position[0]] = Queen()
            board[self.end_position[1]][self.end_position[0]].color = 0
            board[self.end_position[1]][self.end_position[0]].position = [self.end_position[1], self.end_position[0]]
            print("PROMOTE")
        if self.piece.id == 0 and self.piece.color == 1 and self.piece.position[1] == 0:
            board[self.end_position[1]][self.end_position[0]] = Queen()
            board[self.end_position[1]][self.end_position[0]].color = 1
            board[self.end_position[1]][self.end_position[0]].position = [self.end_position[1], self.end_position[0]]


def draw_board():
    print("***")
    for y in range(0, 8):
        line = ""
        for x in range(0, 8):
            v = board[y][x]
            symbol = "." if v == -1 else SYMBOLS[v.id]
            if v != -1 and v.color == 1:
                symbol = symbol.lower()
            line += symbol + " "
        print(line)
    print("***")


def check_square(position):
    x, y = position
    if x > 7 or x < 0 or y > 7 or y < 0:
        return None
    if board[y][x] == -1:
        return -1
    else:
        return board[y][x].color


def new_position(position, movement):
    return [position[0] + movement[0], position[1] + movement[1]]


def get_all_moves(color):
    move_list = []
    for y in range(0, 8):
        for x in range(0, 8):
            if board[y][x] != -1 and board[y][x].color == color:
                board[y][x].get_moves()
                move_list.extend(board[y][x].available_moves)
    return move_list


def draw_board2():
    WINDOW.blit(BOARD_IMAGE, [0, 0])
    for y in range(0, 8):
        for x in range(0, 8):
            v = board[y][x]
            if v == -1:
                continue
            b = 0
            if v.color == 1:
                b = 6

            WINDOW.blit(PIECE_SPRITES[v.id + b], [x * 50, y * 50])


def board_after_move(temp_board, move):
    new_board = copy.deepcopy(temp_board)
    board = copy.deepcopy(new_board)


def is_check(temp_board, color):
    move_list = get_all_moves(color)
    for move in move_list:
        x = move.end_position[0]
        y = move.end_position[1]
        v = temp_board[y][x]
        if v != -1:
            if v.id == 5:
                return True
    return False


board = []
for _ in range(0, 8):
    board.append(list([-1] * 8))

CLASSES = [Pawn, Rook, Knight, Bishop, Queen, King]
SYMBOLS = ["P", "R", "K", "B", "Q", "X"]
INIT_BOARD = [
    [1, 2, 3, 4, 5, 3, 2, 1],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [-1] * 8,
    [-1] * 8,
    [-1] * 8,
    [-1] * 8,
    [6, 6, 6, 6, 6, 6, 6, 6],
    [7, 8, 9, 11, 10, 9, 8, 7]
]

for y in range(0, 8):
    for x in range(0, 8):
        v = INIT_BOARD[y][x]
        if v == -1:
            continue
        board[y][x] = CLASSES[v if 0 >= v < 6 else v - 6]()
        board[y][x].color = 0 if 0 <= v < 6 else 1
        board[y][x].position = [x, y]

print(get_all_moves(0))
print(len(get_all_moves(0)))
draw_board()
turn = 0

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
        if e.type == pygame.KEYDOWN:
            turn = 1 if turn == 0 else 0
            print(is_check(board, 0))
            move = random.choice(get_all_moves(turn))
            move.move(board)
            board_after_move(board, move)


    draw_board2()
    pygame.display.update()