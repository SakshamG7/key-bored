"""
@author: Saksham Goel
@description: Creates the optimal keyboard layout for a given text.
@version: 0.1
@date: 2024-05-11
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
    entireBoard = set([keys for row in board for keys in row[0]] + [keys for row in board for keys in row[1]])
    for letter in text:
        if letter not in entireBoard:
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


# the keyboard tensor with shift, also an important global variable
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


# Creates a random keyboard layout based on the given parameters
def createRandomKeyboard(shiftedOptimal: bool = False, shapeOptimal: bool = False, shape: list=[13, 13, 11, 10], keyboard: list = [[list("`1234567890-="), list("~!@#$%^&*()_+")], [list("qwertyuiop[]\\"), list("QWERTYUIOP{}|")],[list("asdfghjkl;'"), list("ASDFGHJKL:\"")], [list("zxcvbnm,./"), list("ZXCVBNM<>?")]], home_keys_cordinates: list = [[2, 0], [2, 1], [2, 2], [2, 3], [2, 6], [2, 7], [2, 8], [2, 9]], mutation_rate: float = -1):
    # Initialize the keyboard layout and the 2d array of the keyboard layout
    board = [[], [], []]
    keyboard_2d = []
    keyboard_2d_shift = []

    # breaks the given keyboard shape and creates a 2d array of the keyboard layout, [defaults to QWERTY if not given]
    for row in range(len(keyboard)):
        keyboard_2d += keyboard[row][0]
        keyboard_2d_shift += keyboard[row][1]

    if shiftedOptimal: # If we want to optimize the shifted layout as well, we shuffle both the non-shifted and shifted layout
        if mutation_rate == -1:
            random.shuffle(keyboard_2d)
            random.shuffle(keyboard_2d_shift)
        else:
            for _ in range(len(keyboard_2d) - 1):
                if random.random() < mutation_rate:
                    # swaps two random keys for both shifted and non-shifted layout
                    keyboard_2d[random.randint(0, len(keyboard_2d) - 1)], keyboard_2d[random.randint(0, len(keyboard_2d) - 1)] = keyboard_2d[random.randint(0, len(keyboard_2d) - 1)], keyboard_2d[random.randint(0, len(keyboard_2d) - 1)]
                    keyboard_2d_shift[random.randint(0, len(keyboard_2d_shift) - 1)], keyboard_2d_shift[random.randint(0, len(keyboard_2d_shift) - 1)] = keyboard_2d_shift[random.randint(0, len(keyboard_2d_shift) - 1)], keyboard_2d_shift[random.randint(0, len(keyboard_2d_shift) - 1)]
                        
    else: # If we don't want to optimize the shifted layout and keep it aligned with the non-shifted layout
        if mutation_rate == -1:
            temp_non_shift = keyboard_2d.copy() # Create a temporary copy of the non-shifted layout
            temp_shift = keyboard_2d_shift.copy() # Create a temporary copy of the shifted layout
            random.shuffle(keyboard_2d) # Shuffle the non-shifted layout
            for key in range(len(keyboard_2d)): # Align the shifted layout with the non-shifted layout
                temp_shift[key] = keyboard_2d_shift[temp_non_shift.index(keyboard_2d[key])]
            keyboard_2d_shift = temp_shift.copy() # Update the shifted layout with the aligned layout
        else:
            for _ in range(len(keyboard_2d) - 1):
                if random.random() < mutation_rate:
                    # swaps two random keys for both shifted and non-shifted layout
                    randSwapKey1 = random.randint(0, len(keyboard_2d) - 1)
                    randSwapKey2 = random.randint(0, len(keyboard_2d) - 1)
                    keyboard_2d[randSwapKey1], keyboard_2d[randSwapKey2] = keyboard_2d[randSwapKey2], keyboard_2d[randSwapKey1]
                    keyboard_2d_shift[randSwapKey1], keyboard_2d_shift[randSwapKey2] = keyboard_2d_shift[randSwapKey2], keyboard_2d_shift[randSwapKey1]

    # Creates a random shape of the keyboard layout
    if shapeOptimal: # TODO: Optimize the creation of the shape of the keyboard layout to be more efficient (lazy implementation_
        total = sum(shape) # Calculate the total number of keys in the keyboard layout
        shapeXs = []
        if mutation_rate == -1:
            # Starting values for the shape of the keyboard layout
            shapeY = random.randint(1, total)
            shapeX = 0

            # Figure out the number of keys in each row of the keyboard layout
            for _ in range(shapeY):
                if shapeX > total or (total - shapeX) <= 1:
                    shapeXs.append(1)
                    shapeX += 1
                else:
                    shapeXs.append(random.randint(1, total - shapeX))
                    shapeX += shapeXs[-1]
            # Make sure the shape of the keyboard layout is correct
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
        else:
            # Creates a new shape according to the mutation rate
            shapeXs = []
            # Make sure the shape of the keyboard layout is correct and all values are greater than 0
            while True:
                if sum(shapeXs) == total:
                    stop = True
                    for i in shapeXs:
                        if i <= 0:
                            stop = False
                    if stop:
                        break
                shapeXs = []
                for _ in range(random.randint(1, total)):
                    if random.random() < mutation_rate:
                        if total - sum(shapeXs) <= 1:
                            shapeXs.append(1)
                        else:
                            shapeXs.append(random.randint(1, total - sum(shapeXs)))
        # Update the shape of the keyboard layout from the given/default shape
        shape = shapeXs.copy()
        # Updates the home keys cordinates based on the new shape randomly
        home_keys_cordinates = []
        for _ in range(len(shape)):
            x2 = random.randint(0, _)
            home_keys_cordinates.append([x2, random.randint(0, shape[x2] - 1)])

    # Update the shape of the board
    board[1] = shape.copy()

    # Reconstruct the keyboard layout in to shape form
    y = 0 # Row index
    for x in shape:
        board[0].append([[], []]) # Add a new row to the keyboard layout, [<non-shifted-list>, <shifted-list>]
        for _ in range(x):
            board[0][y][0].append(keyboard_2d[0]) # Add the non-shifted key to the keyboard layout
            keyboard_2d.pop(0)
            board[0][y][1].append(keyboard_2d_shift[0]) # Add the shifted key to the keyboard layout
            keyboard_2d_shift.pop(0)
        # Update the row index
        y += 1
    
    # Convert home keys cordinates to home keys of the keyboard layout
    for key in home_keys_cordinates:
        board[2].append(board[0][key[0]][0][key[1]]) # Add the home key to the home keys of the keyboard layout

    return board # Return the keyboard layout with its shape


# Mutates the given keyboard layout based on the mutation rate
def mutateKeyboard(board, mutation_rate: float = 0.05, mutateShape: bool = False, mutateShifted: bool = False):
    mutation_rate = round(mutation_rate, bitLearning) # Round the mutation rate to the bit learning value to adjust precision
    # Convert home keys cordinates to home keys of the keyboard layout
    home_keys_cordinates = []
    a = None
    b = None
    for key in board[2]:
        for row in range(len(board[0])):
            if key in board[0][row][0]:
                b = board[0][row][0].index(key)
                a = row
                home_keys_cordinates.append([a, b])
            elif key in board[0][row][1]:
                b = board[0][row][1].index(key)
                a = row
                home_keys_cordinates.append([a, b])

    return createRandomKeyboard(keyboard=board[0], shape=board[1], home_keys_cordinates=home_keys_cordinates, mutation_rate=mutation_rate, shapeOptimal=mutateShape, shiftedOptimal=mutateShifted) # Return new the mutated keyboard layout


# The genetic algorithm to find the optimal keyboard layout
# TODO: Add penalty for 2 hands not alternating. - Complicated but possible
def geneticAlgorithm(shiftedOptimal: bool = False, shapeOptimal: bool = False, shape: list=[13, 13, 11, 10], population_size: int = 10, generations: int = 10, mutation_rate: float = 0.05): # TODO: Implement the genetic algorithm soon
    population = []
    performance = [] # The lower cost in distance the better the performance
    mutation_rate = round(mutation_rate, bitLearning) # Round the mutation rate to the bit learning value to adjust precision

    bestBoard = [[], [], []]
    bestBoardIndex = -1
    bestScore = -1

    # Create and print the initial population based on selected parameters
    for _ in range(population_size):
        population.append(createRandomKeyboard(shiftedOptimal=shiftedOptimal, shapeOptimal=shapeOptimal, shape=shape))
        printBoard(population[-1][0], shift=True)

    # Initial test of the population
    print("Initial Population")
    for boardNumber in range(population_size):
        board = population[boardNumber]
        performance.append(calcDistance(board=board[0], home_keys=board[2], text=readDatasets(), debug=False))
        print("Keyboard #", boardNumber + 1, ":", performance[-1])
        # Update the best board
        if performance[boardNumber] < bestScore or bestScore == -1:
            bestBoard = board
            bestBoardIndex = boardNumber
            bestScore = performance[boardNumber]

    # Run a basic genetic algorithm for the given number of generations
    for generation in range(generations):
        print("Generation #", generation + 1)
        for boardNumber in range(len(population)):
            population[boardNumber] = mutateKeyboard(population[boardNumber], mutation_rate=mutation_rate)
            # printBoard(population[boardNumber][0], shift=True)
        print("Performance")
        for boardNumber in range(len(population)):
            board = population[boardNumber]
            performance[boardNumber] = calcDistance(board=board[0], home_keys=board[2], text=readDatasets(), debug=False)
            print("Keyboard #", boardNumber + 1, ":", performance[boardNumber])
            # Update the best board
            if performance[boardNumber] < bestScore or bestScore == -1:
                bestBoard = board
                bestBoardIndex = boardNumber
                bestScore = performance[boardNumber]
    
    # Print the best board
    print("-"*20)
    print("Best Keyboard Found #" + str(bestBoardIndex + 1) + ":")
    print("Performance / Distance:", bestScore)
    printBoard(bestBoard[0], shift=True)
    print("-"*20)


geneticAlgorithm() # Run the genetic algorithm to find the optimal keyboard layout
