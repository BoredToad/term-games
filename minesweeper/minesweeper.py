from termcolor import colored, cprint
import sys
import os
import random
from keyboard import read_key
from time import sleep

label = {
        "?": colored("?", "light_grey"),
        0: colored("0", "white"),
        1: colored("1", "blue"),
        2: colored("2", "green"),
        3: colored("3", "yellow"),
        4: colored("4", "red"),
        5: colored("5", "magenta"),
        6: colored("6", "cyan"),
        7: colored("7", "light_red"),
        8: colored("8", "black")
}

class Square:
    def __init__(self, ismine):
        self.revealed = False
        self.ismine = ismine
        self.neighbours = 0
        self.marked = False

def make_board():
    mines = 0
    for i in range(board_size):
        board.append([])
        for j in range(board_size):
            board[i].append(Square(False))
            if random.randint(1, 100) <= mine_chance:
                board[i][j].ismine = True
                mines += 1
    return mines

def board_neighbours():
    for i in range(board_size):
        for j in range(board_size):
            for y in range(-1, 2):
                for x in range(-1, 2):
                    if i + y < 0 or j + x < 0:
                        continue
                    if i + y == board_size or j + x == board_size:
                        continue
                    if board[i + y][j + x].ismine:
                        board[i][j].neighbours += 1

def print_board():
    os.system("clear")
    for i in range(board_size):
        for j in range(board_size):
            output = label["?"]
            if board[i][j].marked:
                output = colored("!", "red")
            if board[i][j].revealed:
                output = label[board[i][j].neighbours]
            if i == cursor["y"] and j == cursor["x"]:
                cprint(output, attrs=["reverse"], end=" ")
            else:
                cprint(output, end=" ")
        print()

def reveal(y, x):
    if board[y][x].ismine:
        print("That's a mine!")
        quit()
    board[y][x].revealed = True
    global revealed
    revealed += 1
    if board[y][x].neighbours != 0:
        return
    for i in range(y - 1, y + 2):
        for j in range(x - 1, x + 2):
            if i < 0 or i >= board_size or j < 0 or j >= board_size:
                continue
            if not board[i][j].revealed:
                reveal(i, j)

cursor = {
        "x": 0,
        "y": 0,
}
up = ["k", "up", "w"]
down = ["j", "down", "s"]
left = ["h", "left", "a"]
right = ["l", "right", "d"]

revealed = 0
if len(sys.argv) != 3:
    print("Bad arguments")
    quit()
mine_chance = int(sys.argv[1])
board_size = int(sys.argv[2])
board = []
mine_count = make_board()
board_neighbours()
marked = []
while True:
    print_board()
    input = read_key()
    if input in up:
        cursor["y"] -= 1
    elif input in down:
        cursor["y"] += 1
    elif input in left:
        cursor["x"] -= 1
    elif input in right:
        cursor["x"] += 1
    elif input == "space":
        if not board[cursor["y"]][cursor["x"]].revealed:
            reveal(cursor["y"], cursor["x"])
    elif input == "m":
        marked = board[cursor["y"]][cursor["x"]].marked
        if not marked:
            board[cursor["y"]][cursor["x"]].marked = True
        else:
            board[cursor["y"]][cursor["x"]].marked = False
    else:
        continue
    if cursor["x"] < 0:
        cursor["x"] = 0
    elif cursor["x"] >= board_size:
        cursor["x"] = board_size - 1
    if cursor["y"] < 0:
        cursor["y"] = 0
    elif cursor["y"] >= board_size:
        cursor["y"] = board_size - 1
    sleep(0.1)
    if revealed + mine_count == board_size**2:
        print_board()
        print("You win!")
        quit()
