from random import choice
from pieces import pieces
import colors
from os import system, name
from time import sleep
from pynput.keyboard import Listener, Key


# basically samme som i 2048
def print_game():
    out_str = ""
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if {"x": x, "y": y} in current:
                out_str += colors.bg["blue"] + "  "
            elif occupied[y][x]:
                out_str += colors.bg["red"] + "  "
            else:
                out_str += colors.bg["black"] + "  "
            out_str += colors.reset

        out_str += "\n"
    system("cls" if name == "nt" else "clear")
    print(out_str)
    print(f"STORED: {stored}\nSCORE: {score}")


def detect_collision(current, next, occupied, WIDTH):
    # ser om occupied clasher med current hvis den fortsetter til next
    for i in range(WIDTH):
        for j in range(HEIGHT):
            if occupied[j][i]:
                if {"x": i - next["x"], "y": j - next["y"]} in current:
                    return True
    # ser om den går ut veggene
    for i in current:
        # I wish this worked
        # ------------------------------------------------------
        # if occupied[i["y"] + next["y"]][i["x"] + next["x"]]: |
        #     return True                                      |
        # ------------------------------------------------------
        if i["x"] + next["x"] > WIDTH - 1 or i["x"] + next["x"] < 0:
            return True
    return False


def check_loss(occupied):
    # ser i den høyeste raden om den finner noe
    for i in occupied[0]:
        if i:
            return True
    return False


def line_clear(HEIGHT, WIDTH):
    global occupied
    removal = []
    points = 0

    for i in range(HEIGHT):
        count = 0
        # ser om antall plassert == WIDTH, og legger indexen av raden
        # til de som skal slettes
        for j in range(WIDTH):
            if occupied[i][j]:
                count += 1
        if count == WIDTH:
            removal.append(i)
    # sletter alle som skal slettes, og legger til en ny rad på toppen
    # for hver rad som ble slettet
    for i in removal:
        del occupied[i]
        occupied.insert(0, [False for i in range(WIDTH)])
        points += 100
    return points


def on_press(key):
    # basically en kombinasjon av 2048 og snake on_press funksjonen
    global switched
    global switch_locked
    global hard_drop
    global rotation
    global pointer
    global current
    # try er fordi Listener krasher om du ser etter
    # key.char hvis den ikke har en char
    try:
        input = key.char
        if input in ["c", "r", "j"]:
            # lager en rotert kopi og ser om den kolliderer
            tmp_rotation = rotation + 1
            if tmp_rotation > 4:
                tmp_rotation = 1
            tmp = [
                {"x": i["x"] + pointer["x"], "y": i["y"] + pointer["y"]}
                for i in piece[tmp_rotation]
            ]
            if not detect_collision(tmp, {"x": 0, "y": 0}, occupied, WIDTH):
                rotation = tmp_rotation
                current = tmp

        elif input in ["x", "k"]:
            if not switch_locked:
                switched = True
                switch_locked = True

        # samme som rotasjon, men trenger ikke en kopi
        # og flytter tingtangen over til siden
        elif input in ["a", "h"]:
            if not detect_collision(current, {"x": -1, "y": 0}, occupied, WIDTH):
                current = [{"x": i["x"] - 1, "y": i["y"]} for i in current]
                pointer["x"] -= 1
        elif input in ["d", "l"]:
            if not detect_collision(current, {"x": 1, "y": 0}, occupied, WIDTH):
                current = [{"x": i["x"] + 1, "y": i["y"]} for i in current]
                pointer["x"] += 1
        print_game()

    except AttributeError:
        if key == key.space:
            hard_drop = True
        elif key == key.left:
            if not detect_collision(current, {"x": -1, "y": 0}, occupied, WIDTH):
                current = [{"x": i["x"] - 1, "y": i["y"]} for i in current]
        elif key == key.right:
            if not detect_collision(current, {"x": 1, "y": 0}, occupied, WIDTH):
                current = [{"x": i["x"] + 1, "y": i["y"]} for i in current]
                pointer["x"] += 1
        print_game()


# starter keyboard.Listener i en ny thread
listener = Listener(on_press=on_press)
listener.start()

# lager basic variabler som brukes i programmet
WIDTH, HEIGHT = 10, 20
FPS = 5

occupied = [[False for j in range(WIDTH)] for i in range(HEIGHT)]
score = 0
stored = "long"
switched = False
switch_locked = False

while True:
    # resetter variabler
    # piece er ikke random om du switchet
    if not switched:
        piece = pieces[choice(list(pieces))]
    hard_drop = False
    rotation = 1
    pointer = {"x": 4, "y": 0}
    current = [
        {"x": i["x"] + pointer["x"], "y": i["y"] + pointer["y"]}
        for i in piece[rotation]
    ]
    switched = False

    # looper helt til den treffer bunnen
    for i in range(HEIGHT - 1):
        # switcher tingtang
        if switched:
            tmp = list(pieces.keys())[list(pieces.values()).index(piece)]
            piece = pieces[stored]
            stored = tmp
            break
        # printer ikke og venter ikke om du hard dropper
        if not hard_drop:
            print_game()
            sleep(1 / (FPS * (1 + (score / 1000))))
        # slutter tidlig hvis den møter på noe
        if detect_collision(current, {"x": 0, "y": 1}, occupied, WIDTH):
            break

        # flytter tingtangen ned med et steg
        current = [{"x": i["x"], "y": i["y"] + 1} for i in current]
        pointer["y"] += 1

    # resetter ikke switched og legger ikke til occupied om
    # du switcher
    if switched:
        continue

    switch_locked = False
    # legger current koordinater til occupied
    for i in current:
        occupied[i["y"]][i["x"]] = True
    if check_loss(occupied):
        break
    score += line_clear(HEIGHT, WIDTH)
