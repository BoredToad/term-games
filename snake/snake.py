from os import system, name
from random import choice

right_key = ["l", "d"]
left_key = ["h", "a"]
up_key = ["k", "w"]
down_key = ["j", "s"]


# returnerer retning baserk på keypress
def get_direction(direction, key):
    if key in right_key and direction != "left":
        return "right"
    elif key in left_key and direction != "right":
        return "left"
    elif key in up_key and direction != "down":
        return "up"
    elif key in down_key and direction != "up":
        return "down"
    else:
        return direction


def move_snake(snake, direction):
    # Hver element i slangen utenom hodet blir
    # flyttet til elementet før dem
    for i in range(len(snake) - 1, 0, -1):
        snake[i]["x"] = snake[i - 1]["x"]
        snake[i]["y"] = snake[i - 1]["y"]

    # Hodet blir flyttet basert på retning
    match direction:
        case "right":
            snake[0]["x"] += 1
        case "left":
            snake[0]["x"] -= 1
        case "down":
            snake[0]["y"] += 1
        case "up":
            snake[0]["y"] -= 1
    return snake


def detect_collision(snake, BOARD_WIDTH, BOARD_HEIGHT):
    # Ser om hodet er i en annen del av slangen
    head = snake[0]
    if head in snake[1:]:
        return True
    # ser om hodet er i en vegg
    if head["x"] < 0 or head["x"] >= BOARD_WIDTH:
        return True
    if head["y"] < 0 or head["y"] >= BOARD_HEIGHT:
        return True
    return False


# bruker ansi koder for farge
# ellers er en ganske basic 2d loop som printer
# ut slangen eller eplet hvis den er der
def print_board(BOARD_WIDTH, BOARD_HEIGHT, snake, apple, score, time):
    system("cls" if name == "nt" else "clear")
    print("\033[0;100m", end="")
    for i in range(BOARD_HEIGHT):
        for j in range(BOARD_WIDTH):
            if {"x": j, "y": i} in snake:
                print("\033[0;42m  ", end="\033[0;100m")
            elif {"x": j, "y": i} == apple:
                print("\033[0;41m  ", end="\033[0;100m")
            else:
                print("  ", end="")
        print()
    print(f"\033[0mSCORE: {score}\nTIME: {'{:.2f}'.format(time)}")
    return


def spawn_apple(BOARD_WIDTH, BOARD_HEIGHT, snake):
    # eplet for en koordinat som ikke er brukt av slangen
    x = choice([i for i in range(BOARD_WIDTH) if i not in [j["x"] for j in snake]])
    y = choice(
        [
            i
            for i in range(BOARD_HEIGHT)
            if {"x": x, "y": i} not in [j["y"] for j in snake]
        ]
    )
    return {"x": x, "y": y}
