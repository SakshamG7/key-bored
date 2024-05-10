"""
@author: Saksham Goel
@description: Creates the optimal keyboard layout for a given text.
@version: 0.1
@date: 2024-05-10
"""

# Imports
import random
import math
import os

# Print the keyboard in a readable format. Shift is optional.
def printBoard(board, shift: bool = False):
    outputs = ["", ""]
    for row in range(len(board)):
        outputs[0] += "\n" + " " * (row + row//len(board))
        if row > 0:
            outputs[0] += "  "
        for key in board[row][0]:
            outputs[0] += key + " "
        if shift:
            outputs[1] += "\n" + " " * (row + row//len(board))
            if row > 0:
                outputs[1] += "  "
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
def charDistance(board, startKey, endKey, boardCache: dict) -> int:
    if startKey == endKey:
        return 0
    if startKey + endKey in boardCache:
        return boardCache[startKey + endKey]
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
        x1 += 1
        x1 += (y1 - 1) * AOS
    if y2 > 0:
        x2 += 1
        x2 += (y2 - 1) * AOS
    dist = round(math.dist([x1, y1], [x2, y2]), bitLearning)
    boardCache[startKey + endKey] = dist
    boardCache[endKey + startKey] = dist
    return dist


# Calculate the total distance to type out a string on a keyboard.
def calcDistance(board, text: str, home_keys: list = ["a", "s", "d", "f", "j", "k", "l", ";"], debug: bool = False) -> int:
    distance = 0
    cur_keys = home_keys.copy()
    boardCache = {}
    for letter in text:
        if letter in (" ", "\t", "\n"):
            continue
        smallest = [1000000000000000, -1]
        for cur_key in range(len(cur_keys)):
            new_smallest = charDistance(board=board, startKey=home_keys[cur_key], endKey=letter, boardCache=boardCache)
            if new_smallest < smallest[0]:
                smallest[0] = new_smallest
                smallest[1] = cur_key
        smallest[0] = charDistance(board=board, startKey=cur_keys[smallest[1]], endKey=letter, boardCache=boardCache)
        if debug:
            print(cur_keys[smallest[1]], " finger is now on ", letter, ". Distance: ", smallest[0])
        cur_keys[smallest[1]] = letter
        distance += smallest[0]
    if debug:
        totalD = 0
        c = 0
        for d in boardCache.values():
            if d == 0:
                continue
            totalD += d
            c += 1
        print("Average Key Distance:", round(totalD/c, bitLearning))
        print("Total Distance:", round(distance, bitLearning))

    return round(distance, bitLearning)


# Read all the datasets in the `dataset` folder, program must be run outside the src folder.
def readDatasets() -> str:
    output = ""
    for filename in os.listdir("dataset/"):
        if filename.lower().endswith(".txt"):
            with open("dataset/" + filename, "r") as f:
                output += f.read()
            output += "\n"
    return output


# the keyboard tensor with shift
keyboard = [[['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '='], list("~!@#$%^&*()_+")],
            [list("qwertyuiop[]\\"), list("QWERTYUIOP{}|")],
            [list("asdfghjkl;'"), list("ASDFGHJKL:\"")],
            [list("zxcvbnm,./"), list("ZXCVBNM<>?")]]

dvorakBoard = [[['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '[', ']'], list("~!@#$%^&*(){}")],
                [list("',.pyfgcrl/="), list('"<.PYFGCRL?+')],
                [list("aoeuidhtns-"), list("AOEUIDHTNS_")],
                [list(";qjkxbmwvz"), list(":QJKXBMWVZ")]]
dvorakHomeKeys = list("aoeuhtns")
# Important global variables
bitLearning = 5

printBoard(keyboard, shift=True) # Prints the entire QWERTY keyboard
printBoard(dvorakBoard, shift=True) # Prints the entire Dvorak keyboard

# Calculate the distance of the datatext for both QWERTY and Dvorak
print(calcDistance(board=keyboard, home_keys=dvorakHomeKeys, text=readDatasets(), debug=False))
print(calcDistance(board=dvorakBoard, home_keys=dvorakHomeKeys, text=readDatasets(), debug=False)) # Dvorak is better than QWERTY, lets see if we can improve it further!!!


# The genetic algorithm to find the optimal keyboard layout
def geneticAlgorithm(shiftedOptimal: bool = False, shapeOptimal: bool = False, shape: list=[13, 13, 11, 10], population_size: int = 10, generations: int = 10, mutation_rate: float = 0.01): # TODO: Implement the genetic algorithm soon
    population = []
    mutation_rate = round(mutation_rate, bitLearning) # Round the mutation rate to the bit learning value to adjust precision

    # Create initial population of random keyboard layouts starting with QWERTY layout
    for _ in range(population_size):
        population.append([keyboard.copy(), shape.copy()])
        # breaks the keyboard shape and creates a 2d array of the keyboard layout
        keyboard_2d = []
        keyboard_2d_shift = []
        for row in range(len(population[-1][0])):
            keyboard_2d += population[-1][0][row][0]
            keyboard_2d_shift += population[-1][0][row][1]
        if shiftedOptimal: # If we want to optimize the shifted layout as well
            random.shuffle(keyboard_2d)
            random.shuffle(keyboard_2d_shift)
        else: # If we don't want to optimize the shifted layout and keep it aligned with the non-shifted layout
            temp_non_shift = keyboard_2d.copy()
            temp_shift = keyboard_2d_shift.copy()
            random.shuffle(keyboard_2d)
            for key in range(len(keyboard_2d)):
                temp_shift[key] = keyboard_2d_shift[temp_non_shift.index(keyboard_2d[key])]
            keyboard_2d_shift = temp_shift.copy()

        # Creates a random shape of the keyboard layout
        if shapeOptimal: # TODO: Optimize the creation of the shape of the keyboard layout to be more efficient (lazy implementation_
            total = sum(shape)
            shapeY = random.randint(1, total)
            shapeX = 0
            shapeXs = []
            for _ in range(shapeY):
                if shapeX > total or (total - shapeX) <= 1:
                    shapeXs.append(1)
                    shapeX += 1
                else:
                    shapeXs.append(random.randint(1, total - shapeX))
                    shapeX += shapeXs[-1]
            while sum(shapeXs) != total:
                shapeY = random.randint(1, total)
                shapeX = 0
                shapeXs = []
                for _ in range(shapeY):
                    if shapeX > total or (total - shapeX) <= 1:
                        shapeXs.append(1)
                        shapeX += 1
                    else:
                        shapeXs.append(random.randint(1, total - shapeX))
                        shapeX += shapeXs[-1]
            shape = shapeXs
        # Reconstruct the keyboard layout in to shape form
        population[-1][0] = []
        y = 0
        for x in shape:
            population[-1][0].append([[], []])
            for _ in range(x):
                population[-1][0][y][0].append(keyboard_2d[0])
                keyboard_2d.pop(0)
                population[-1][0][y][1].append(keyboard_2d_shift[0])
                keyboard_2d_shift.pop(0)
            y += 1

    for board in population:
        printBoard(board[0], shift=True)


geneticAlgorithm(shapeOptimal=False) # Run the genetic algorithm to find the optimal keyboard layout