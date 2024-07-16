# Imports som brukes i programmet
from time import sleep
from pynput.keyboard import Listener, Key
from snake import get_direction, move_snake, print_board, detect_collision, spawn_apple

# definerer variabler
FPS = 8
time = 0.0
BOARD_WIDTH = 20
BOARD_HEIGHT = 20
# Slangen er en liste med koordinater
snake = [
    {"x": 2, "y": 0},
    {"x": 1, "y": 0},
    {"x": 0, "y": 0},
]
apple = {"x": 2, "y": 2}
# Jeg har en input queue fordi
# det leder til enklere svinging
direction_queue = []
direction = "right"
score = 0


# Når du trykker en knapp
def on_press(key):
    global direction
    global direction_queue
    # Legger til retningen til direction queue
    direction_queue.append(get_direction(direction, key.char))
    # Kan ikke ha 2 like retninger i queue en etter hverandre
    if direction_queue[len(direction_queue) - 1] == direction:
        del direction_queue[len(direction_queue) - 1]
    # Direction queue kan ikke være større en 3
    if len(direction_queue) > 3:
        del direction_queue[0]


# Lytter etter tastatur
listener = Listener(on_press=on_press)
# Listener blir om til en thread så den ikke stopper andre deler av programmet
listener.start()
# main loop
while True:
    # direction blir den første retningen i queue
    if len(direction_queue) > 0:
        direction = direction_queue.pop(0)
    snake = move_snake(snake, direction)
    if detect_collision(snake, BOARD_WIDTH, BOARD_HEIGHT):
        print("You lose!")
        break

    print_board(BOARD_WIDTH, BOARD_HEIGHT, snake, apple, score, time)

    if snake[0] == apple:
        score += 1
        # Skjekker om du har fylt alt
        if score + 3 == BOARD_WIDTH * BOARD_HEIGHT:
            print("VICTORY!!!")
            break
        # Legger til en koordinat i halen, hvor den er er ikke viktig, men jeg bare
        # putter den bak forrige ende
        snake.append({"x": snake[len(snake) - 1]["x"], "y": snake[len(snake) - 1]["y"]})
        apple = spawn_apple(BOARD_WIDTH, BOARD_HEIGHT, snake)
    # Game clock
    sleep(1 / FPS)
    time += 1 / FPS
listener.stop
