"""
@author: Saksham Goel
@description: Creates the optimal keyboard layout for a given text.
@version: 0.1
@date: 2024-05-09
"""

# Imports
import random
import math

# Print the keyboard in a readable format. Shift is optional.
def printBoard(board, shift: bool = False):
    outputs = ["", ""]
    for row in range(len(board)):
        outputs[0] += "\n" + " " * (row + row//len(board))
        for key in board[row][0]:
            outputs[0] += key + " "
        if shift:
            outputs[1] += "\n" + " " * (row + row//len(board))
            for key in board[row][1]:
                outputs[1] += key + " "
    print("-"*10)
    print("NON-SHIFT")
    print(outputs[0])
    print("-"*10)
    if shift:
        print("SHIFT")
        print(outputs[1])
        print("-"*10)


# Calculate the distance between two keys on a keyboard.
def charDistance(board, startKey, endKey) -> int:
    x1 = -1
    y1 = -1
    x2 = -1
    y2 = -1
    # Find the x and y coordinates of the start key and end key
    for row in range(len(board)):
        if x1 + y1 != -2 and x2 + y2 != -2:
            break
        if startKey in board[row][0]:
            x1 = board[row][0].index(startKey)
            y1 = row
        elif startKey in board[row][1]:
            x1 = board[row][1].index(startKey)
            y1 = row
        if endKey in board[row][0]:
            x2 = board[row][0].index(endKey)
            y2 = row
        elif endKey in board[row][1]:
            x2 = board[row][1].index(endKey)
            y2 = row
    AOS = .3 # Average Offset Size
    if y1 > 0:
        x1 += 0.5
        x1 += (y1 - 1) * AOS
    if y2 > 0:
        x2 += 0.5
        x2 += (y2 - 1) * AOS
    return round(math.dist([x1, y1], [x2, y2]), bitLearning)


# Calculate the total distance to type out a string on a keyboard.
def calcDistance(board, text: str, home_keys: list = ["a", "s", "d", "f", "j", "k", "l", ";"]) -> int:
    distance = 0
    cur_keys = home_keys.copy()

    for letter in text:
        smallest = [1000000, -1]
        for cur_key in range(len(cur_keys)):
            new_smallest = charDistance(board=board, startKey=home_keys[cur_key], endKey=letter)
            if new_smallest < smallest[0]:
                smallest[0] = new_smallest
                smallest[1] = cur_key
        smallest[0] = charDistance(board=board, startKey=cur_keys[smallest[1]], endKey=letter)
        print(cur_keys[smallest[1]], " finger is now on ", letter, ". Distance: ", smallest[0])
        cur_keys[smallest[1]] = letter
        distance += smallest[0]

    return round(distance, bitLearning)


# the keyboard tensor with shift
keyboard = [[['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '='], list("~!@#$%^&*()_+")],
            [list("qwertyuiop[]\\"), list("QWERTYUIOP{}|")],
            [list("asdfghjkl;'"), list("ASDFGHJKL:\"")],
            [list("zxcvbnm,./"), list("ZXCVBNM<>?")]]

bitLearning = 5

printBoard(keyboard, shift=True) # Prints the entire QWERTY keyboard
print(charDistance(board=keyboard, startKey="q", endKey="a"))
print(calcDistance(board=keyboard, text="qqqwqqq")) # Prints the distance to type out "qwertyuiop" with a QWERTY keyboard
