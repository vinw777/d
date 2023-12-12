import random
import os
import time

GAME_BOARD = [[" " for _ in range(7)] for _ in range(7)]
VISIBLE_BOARD = [[" " for _ in range(7)] for _ in range(7)]
LETTERS_TO_NUMBERS = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6}

ships_amount = {1: 3, 2: 2}

def is_already_shot(cord):
    x = int(cord[1]) - 1
    y = LETTERS_TO_NUMBERS[cord[0]]
    return VISIBLE_BOARD[x][y] in {"m", "X"}

def display_interface(board):
    print("   A B C D E F G")
    print("  --------------")
    for i, row in enumerate(board, 1):
        print(f"{i}| {' '.join(row)}")

def make_hit(cord):
    x = int(cord[1]) - 1
    y = LETTERS_TO_NUMBERS[cord[0]]
    VISIBLE_BOARD[x][y] = "X" if GAME_BOARD[x][y] == "O" else "m"

def generate_single_ship():
    x, y = random.randint(0, 6), random.randint(0, 6)
    if not got_interruption(x, y):
        GAME_BOARD[x][y] = "O"
    else:
        generate_single_ship()

def got_interruption(x, y):
    for i in range(x - 1, x + 2):
        for j in range(y - 1, y + 2):
            if i == x and j == y:
                continue
            elif 0 <= i <= 6 and 0 <= j <= 6 and ship_exists(i, j):
                return True
    return False

def ship_exists(x_cord, y_cord):
    return GAME_BOARD[x_cord][y_cord] == "O"

def generate_big_ship(length):
    x_cord, y_cord = random.randint(0, 6), random.randint(0, 6)
    directions = []

    if not got_interruption(x_cord, y_cord):
        directions.extend(["down", "right", "up", "left"])
        directions = [dir for dir in directions if can_place_ship(x_cord, y_cord, length, dir)]

    if directions:
        place_ship(x_cord, y_cord, length, random.choice(directions))
        return True
    return False

def can_place_ship(x, y, length, direction):
    if direction == "left" and y - length >= -1:
        return all(not ship_exists(x, y - i) for i in range(length))
    elif direction == "right" and y + length <= 6:
        return all(not ship_exists(x, y + i) for i in range(length))
    elif direction == "up" and x - length >= -1:
        return all(not ship_exists(x - i, y) for i in range(length))
    elif direction == "down" and x + length <= 6:
        return all(not ship_exists(x + i, y) for i in range(length))
    return False

def place_ship(x, y, length, direction):
    for i in range(length):
        if direction == "left":
            GAME_BOARD[x][y - i] = "O"
        elif direction == "right":
            GAME_BOARD[x][y + i] = "O"
        elif direction == "up":
            GAME_BOARD[x - i][y] = "O"
        elif direction == "down":
            GAME_BOARD[x + i][y] = "O"

# Place big ships
for elem in ships_amount.items():
    c = 0
    while c != elem[0]:
        if generate_big_ship(elem[1]):
            c += 1

# Place small ships
for _ in range(4):
    generate_single_ship()

# Game loop
while True:
    print("Missed shots are marked as 'm'.\nHitting shots are marked as 'X'.")
    display_interface(board=VISIBLE_BOARD)
    hit_coordinate = input("Enter a coordinate in 'letter/digit' form: ")
    if not is_already_shot(hit_coordinate):
        make_hit(hit_coordinate)
    else:
        os.system("cls")
        print("You've already shot in this point!")
        time.sleep(2.0)
    os.system("cls")
