"""
Made by: Ryken Santillan
Version Started: 2022-12-28
Version Finished: 2022-12-30
Class: Solver
Description:
      - This class solves a magic square using a self-made algorithm
"""

import numpy as np

magicSum = 0  # global var to track sum consistency across rows / cols

# Converts array into a 2D int array
def convert_array(array):
    arrayNew = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    curr = 0
    for i in range(len(arrayNew)):
        for j in range(len(arrayNew)):
            if array[curr].isdigit():
                arrayNew[i][j] = (int(array[curr]))
            else:
                array[curr] = '0' # Specified int, MAGIC SQUARES DO NOT CONTAIN 0
                arrayNew[i][j] = (int(array[curr]))
            curr += 1
    return arrayNew

# Transposes Array: Done to save repetition in algo: cols --> rows vice versa
def array_transpose(array):
    transposeArray = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for i in range(len(array)):
        transposeArray[i] = [row[i] for row in array]
    return transposeArray

# Initializes an array to work with the algorithm
def init_state(array, patternRow, patternCol):
    checkArray = [0,0,0]
    checkArray[0] = array[patternRow[0]][patternCol[0]]
    checkArray[1] = array[patternRow[1]][patternCol[1]]
    checkArray[2] = array[patternRow[2]][patternCol[2]]

    # PLACES APPROPRIATE VALUES USING EXISTING CROSS ALGORITHM
    if (checkArray.count(0) == 1):
        tempLoc = checkArray.index(0)
        if tempLoc == 0:
            if (checkArray[1] > checkArray[2] and checkArray[1] - checkArray[2] == 1):
                checkArray[0] = checkArray[1] + 1
                array[patternRow[0]][patternCol[0]] = checkArray[0]
            elif (checkArray[2] > checkArray[1] and checkArray[2] - checkArray[1] == 1):
                checkArray[0] = checkArray[1] - 1
                array[patternRow[0]][patternCol[0]] = checkArray[0]
        elif tempLoc == 1:
            if (checkArray[2] > checkArray[0] and checkArray[2] - checkArray[0] == 2):
                checkArray[1] = checkArray[0] + 1
                array[patternRow[1]][patternCol[1]] = checkArray[1]
            elif (checkArray[0] > checkArray[2] and checkArray[0] - checkArray[2] == 2):
                checkArray[1] = checkArray[0] - 1
                array[patternRow[1]][patternCol[1]] = checkArray[1]
        elif tempLoc == 2:
            if (checkArray[1] > checkArray[0] and checkArray[1] - checkArray[0] == 1):
                checkArray[2] = checkArray[1] + 1
                array[patternRow[2]][patternCol[2]] = checkArray[2]
            elif (checkArray[0] > checkArray[1] and checkArray[0] - checkArray[1] == 1):
                checkArray[2] = checkArray[1] - 1
                array[patternRow[2]][patternCol[2]] = checkArray[2]
    return array

# Obtains singular magic sum to use consistently, and fills in missing square
def replace(array, replaceCall, row, colArr=[0,1,2]):
    global magicSum
    magicBase = 15
    current = array[row].index(0)
    tempMiss = array[row][colArr[0]] + array[row][colArr[1]] + array[row][colArr[2]]
    tempFactor = (int(tempMiss / magicBase)) + 1
    if replaceCall == 0:
        magicSum = (tempFactor * 15)
    tempReplacement = magicSum - tempMiss
    array[row][current] = tempReplacement
    return array

# Algorithm to solve rows / cols (diagonals don't need to be considered)
def solve_array(array):
    flipState = 0
    replaceCall = 0
    while True:
        tracker = 0
        #rows
        if array[0].count(0) == 1:
            replace(array, replaceCall, 0)
            replaceCall += 1
        if array[1].count(0) == 1:
            replace(array, replaceCall, 1)
            replaceCall += 1
        if array[2].count(0) == 1:
            replace(array, replaceCall, 2)
            replaceCall += 1
        # solve for cols, or reverse
        array = array_transpose(array)
        flipState += 1
        for i in range(len(array)):  # used to check if 0 in array, "not in" bugging out
            for j in range(len(array)):
                if array[i][j] == 0:
                    tracker += 1
        if tracker == 0:
            break
    if flipState % 2 > 0: # if array is row of cols instead of original state
        array = array_transpose(array)
    return array

# collection of commands to use the class, simplified into a method for main
def run(array):
    checkSum = 0
    arrayFinal = init_state(convert_array(array), [2, 0, 1], [1, 0, 2])  # 816
    arrayFinal = init_state(arrayFinal, [1, 0, 2], [0, 2, 1]) #438
    arrayFinal = init_state(arrayFinal, [0, 2, 1], [1, 0, 2]) #276
    arrayFinal = init_state(arrayFinal, [0, 2, 1], [1, 2, 0]) #294
    arrayFinal = solve_array(arrayFinal)
    for i in range(len(arrayFinal)):
        for j in range(len(arrayFinal)):
            checkSum += arrayFinal[i][j]

    if checkSum % 15 > 0:
        print("Not a viable magic square")
        exit()
    else:
        return np.array(arrayFinal).flatten('C') #returns 1D array


