# Imports
from random import choice
from os import system, name
from pynput.keyboard import Listener, Key
from copy import deepcopy

# Fargene er bare ansi koder
colors = {
    2: "\033[0;41m",
    4: "\033[0;43m",
    8: "\033[0;42m",
    16: "\033[0;44m",
    32: "\033[0;45m",
    64: "\033[0;46m",
    128: "\033[0;101m",
    256: "\033[0;102m",
    512: "\033[0;103m",
    1024: "\033[0;104m",
    2048: "\033[0;100m",
}


class Board:
    # Lager 2d arr
    def __init__(self, DIMENSIONS):
        self.DIMENSIONS = DIMENSIONS
        self.squares = []
        for i in range(self.DIMENSIONS):
            self.squares.append([])
            for j in range(self.DIMENSIONS):
                self.squares[i].append(0)

    # Finner en tom kvadrat
    def append_square(self):
        available = []
        for i in range(self.DIMENSIONS):
            for j in range(self.DIMENSIONS):
                if self.squares[i][j] == 0:
                    available.append([i, j])
        try:
            cords = choice(available)
            square = choice([2, 4])
            self.squares[cords[0]][cords[1]] = square
            return square
        # Hvis den ikke finner en,
        # er en litt meningsløs edgecase, men skader ikke
        except IndexError:
            return 0

    def __str__(self):
        out = "\033[1;30m"
        for i in range(self.DIMENSIONS):
            for k in range(3):
                for j in range(self.DIMENSIONS):
                    square = self.squares[j][i]
                    # basically, nesten alt er padding,
                    # og antal padding endres på verdien til tallet
                    if square == 0:
                        out += f"\033[0;47m{' ' * 6}\033[0m"
                    else:
                        # ehrm, sorry
                        out += f"""{colors[square]}\033[1;30m{' ' * 6 if k != 1 else 
                        ' ' + str(square) + ' ' if square > 999 else
                        ' ' + str(square) + '  ' if square > 99 else
                        '  ' + str(square) + '  ' if square > 9 else 
                        '   ' + str(square) + '  '}\033[0m"""
                out += "\n"
        return out

    # ser om det er en forskjell i brettet, og tmp
    def board_compare(self, tmp):
        for i in range(self.DIMENSIONS):
            for j in range(self.DIMENSIONS):
                if self.squares[i][j] != tmp[i][j]:
                    return True
        return False

    # mange loops og if conditions endrer seg pga. retning,
    # mer om det i README filen
    # basically, går gjennom hver firkant, og flytter den
    # helt til den møter en kant, eller en annen firkant
    def move_horisontal(self, dir):
        # lagrer tmp nå så den kan bli compared senere
        tmp = deepcopy(self.squares)
        for i in (
            range(self.DIMENSIONS - 1, -1, -1) if dir == "f" else range(self.DIMENSIONS)
        ):
            for j in range(self.DIMENSIONS):
                if self.squares[i][j] == 0:
                    continue
                for k in (
                    range(i + 1, self.DIMENSIONS)
                    if dir == "f"
                    else range(i - 1, -1, -1)
                ):
                    if self.squares[k][j] == self.squares[i][j]:
                        self.squares[k][j] *= 2
                        self.squares[i][j] = 0
                        break
                    elif self.squares[k][j] != 0:
                        self.squares[k + (-1 if dir == "f" else 1)][j] = self.squares[
                            i
                        ][j]
                        if (k + (-1 if dir == "f" else 1)) != i:
                            self.squares[i][j] = 0
                        break
                    elif k == ((self.DIMENSIONS - 1) if dir == "f" else 0):
                        self.squares[k][j] = self.squares[i][j]
                        self.squares[i][j] = 0
                        break
        return self.board_compare(tmp)

    # se move_horisontal
    def move_vertical(self, dir):
        tmp = deepcopy(self.squares)
        for i in (
            range(self.DIMENSIONS - 1, -1, -1) if dir == "f" else range(self.DIMENSIONS)
        ):
            for j in range(self.DIMENSIONS):
                if self.squares[j][i] == 0:
                    continue
                for k in (
                    range(i + 1, self.DIMENSIONS)
                    if dir == "f"
                    else range(i - 1, -1, -1)
                ):
                    if self.squares[j][k] == self.squares[j][i]:
                        self.squares[j][k] *= 2
                        self.squares[j][i] = 0
                        break
                    elif self.squares[j][k] != 0:
                        self.squares[j][k + (-1 if dir == "f" else 1)] = self.squares[
                            j
                        ][i]
                        if (k + (-1 if dir == "f" else 1)) != i:
                            self.squares[j][i] = 0
                        break
                    elif k == ((self.DIMENSIONS - 1) if dir == "f" else 0):
                        self.squares[j][k] = self.squares[j][i]
                        self.squares[j][i] = 0
                        break
        return self.board_compare(tmp)

    # ser om 2048 er i brettet
    def check_win(self):
        if 2048 in [
            self.squares[i][j]
            for i in range(self.DIMENSIONS)
            for j in range(self.DIMENSIONS)
        ]:
            return True
        return False


# ser om brettet den får flytter seg
# i hvilken som helst retning
def check_loss(board):
    if board.move_horisontal("f"):
        return False
    if board.move_horisontal("b"):
        return False
    if board.move_vertical("f"):
        return False
    if board.move_vertical("b"):
        return False
    return True


# se snake, men denne gangen kan bruke piltast
# hvis du ser etter key.char til en tast som
# ikke er en char får du en AttributeError
# hvis du returnerer True vil listener spørre
# etter en ny input
def on_press(key):
    try:
        if key.char in ["l", "d"]:
            moved = board.move_horisontal("f")
        elif key.char in ["h", "a"]:
            moved = board.move_horisontal("b")
        elif key.char in ["j", "s"]:
            moved = board.move_vertical("f")
        elif key.char in ["k", "w"]:
            moved = board.move_vertical("b")
        else:
            return True
    except AttributeError:
        match key:
            case Key.down:
                moved = board.move_vertical("f")
            case Key.up:
                moved = board.move_vertical("b")
            case Key.right:
                moved = board.move_horisontal("f")
            case Key.left:
                moved = board.move_horisontal("b")
            case _:
                return True
    return not moved


# init
board = Board(4)
score = 0
board.append_square()
# main loop
while True:
    score += board.append_square()
    system("cls" if name == "nt" else "clear")
    print(board)
    print(score)
    if check_loss(deepcopy(board)):
        print("Lose")
        break
    if board.check_win():
        print("Win")
        break
    # key listener
    with Listener(on_press=on_press) as listener:
        listener.join()
