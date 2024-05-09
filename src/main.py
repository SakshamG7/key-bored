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
def charDistance(board, startKey, endKey):
    x = 0
    y = 0
    for row in range(len(board)):
        tempX = 0
        tempY = 0
        for key in board[row][0]:
            if endKey == key:
                break

    return math.sqrt((x - tempX)**2 + (y - tempY)**2)


# Calculate the total distance to type out a string on a keyboard.
def calcDistance(board, text: str):
    distance = 0
    return distance


# the keyboard tensor with shift
keyboard = [[['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '='], list("~!@#$%^&*()_+")],
            [list("qwertyuiop[]\\"), list("QWERTYUIOP{}|")],
            [list("asdfghjkl;'"), list("ASDFGHJKL:\"")],
            [list("zxcvbnm,./"), list("ZXCVBNM<>?")]]

printBoard(keyboard, shift=True) # Prints the entire QWERTY keyboard
print(calcDistance(board=keyboard, text="qwertyuiop")) # Prints the distance to type out "qwertyuiop" with a QWERTY keyboard