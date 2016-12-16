# 2048 Game - Recreated by Shiny Ranjan (13/02/2016)
# Note: Only works on Windows

import sys, time, os
from random import randint, choice
from msvcrt import getch

c = '.' # ·
grid = [[c]*4,[c]*4,[c]*4,[c]*4]
sp = ' '
rndNoProbability = [2]*9 + [4]
score = 0

def init(grid):
    os.system('cls')

    availRows = list(range(0,4))
    availColumns = list(range(0,4))

    rndRow = choice(availRows)
    rndColumn = choice(availColumns)
    rndSpawnNo = choice(rndNoProbability)

    grid[rndRow][rndColumn] = str(rndNoProbability[rndSpawnNo])
    randCoord = scanArray(grid, c)
    grid[randCoord[0]][randCoord[1]] = randCoord[2]

    prtGrid(grid)

def prtGrid(grid):
    print(sp*13 + '2048 Game' + '\n')
    print(sp*4 + 'Score:', score, '\n')
    for i in range(4):
        for j in range(4):
            if j < 3:
                print(sp*4 + grid[i][j], end=sp*(5-len(grid[i][j])))
            else:
                print(sp*4 + grid[i][j], end='\n'*2)

def scanArray(grid, c):
    availRows = list(range(4))
    availColumns = list(range(4))
    unavailRows = []
    unavailColumns = [[],[],[],[]]

    for i in range(4):
        counter = 0
        for j in range(4):
            if grid[i][j] != c:
                counter += 1
                unavailColumns[i].append(j)
        if counter == 4:
            unavailRows.append(i)

    if len(unavailRows) != 4:
        for y in unavailRows:
            if y != '':
                availRows.remove(y)

    rndRow = choice(availRows)
    for x in unavailColumns[rndRow]:
        if x != '':
            availColumns.remove(x)
    rndColumn = choice(availColumns)
    rndSpawnNo = choice(rndNoProbability)

    return[rndRow,rndColumn,str(rndSpawnNo)]

def keypress():
    # http://stackoverflow.com/questions/12175964/python-method-for-reading-keypress
    key = ord(getch())
    if key == 224:
        key = ord(getch())
        return {
        80: 'down', # down arrow
        72: 'up', # up arrow
        75: 'left', # left arrow
        77: 'right'  # right arrow
        }[key]
    elif key == 115:
        return 'down'
    elif key == 119:
        return 'up'
    elif key == 97:
        return 'left'
    elif key == 100:
        return 'right'
    elif key == 114:
        return 'rules'
    elif key == 27:
        return 'exit'
    else:
        return 'error'

def takeInput():
    keyPressed = keypress()
    if keyPressed == 'error':
        print('Please use WASD or arrow keys!', end='\r')
    elif keyPressed == 'up' or keyPressed == 'down':
        swipeVertical(keyPressed, grid, c)
    elif keyPressed == 'left' or keyPressed == 'right':
        swipeHorizontal(keyPressed, grid, c)
    elif keyPressed == 'exit':
        print('Press ESC again to exit.')
        keyPressed = keypress()
        if keyPressed == 'exit':
            exit()
    # else:
    #     print(sp*31, end='\r')
    #     print('Key Press:', keyPressed, end='\r')
    checkGameOver()

def swipeHorizontal(direction, grid, c):
    oldGrid = tuple(tuple(x) for x in grid)
    if direction == 'left':
        order, step = [0,1,2], 1
    else:
        order, step = [3,2,1], -1
    counter = [0,0,0,0]
    for x in range(3):
        for i in range(4):
            initialVal = ''.join(grid[i])
            noC = initialVal.count(c)
            if initialVal.isalnum():
                if (len(set(grid[i])) == 1 and set(grid[i]).pop() != c) or \
                (grid[i][0] == grid[i][1] and grid[i][2] == grid[i][3]):
                    counter[i] = -1
            for j in order:
                if grid[i][j] == c and grid[i][j+step] != c:
                    grid[i][j] = grid[i][j+step]
                    grid[i][j+step] = c
                elif grid[i][j] == grid[i][j+step] and grid[i][j] != c and counter[i] <= 0:
                    grid[i][j] = str(int(grid[i][j])*2)
                    grid[i][j+step] = c
                    global score
                    score += int(grid[i][j])
                    counter[i] += 1

        if x == 2:
            if oldGrid != tuple(tuple(x) for x in grid):
                randCoord = scanArray(grid, c)
                grid[randCoord[0]][randCoord[1]] = randCoord[2]
        updateArray(grid)

def swipeVertical(direction, grid, c):
    oldGrid = tuple(tuple(x) for x in grid)
    if direction == 'up':
        order, step = [0,1,2], 1
    else:
        order, step = [3,2,1], -1
    counter = [0,0,0,0]
    for x in range(3):
        for j in range(4): # i = row, j = column
            initialVal = ''.join([nth[j] for nth in grid])
            # http://stackoverflow.com/questions/25050311/extract-first-item-of-each-sublist-in-python
            noC = initialVal.count(c)
            if initialVal.isalnum():
                currList = [nth[j] for nth in grid]
                if (len(set(currList)) == 1 and set(currList).pop() != c) or \
                (currList[0] == currList[1] and currList[2] == currList[3]):
                    counter[j] = -1
            for i in order:
                if grid[i][j] == c and grid[i+step][j] != c:
                    grid[i][j] = grid[i+step][j]
                    grid[i+step][j] = c
                elif grid[i][j] == grid[i+step][j] and grid[i][j] != c and counter[j] <= 0:
                    grid[i][j] = str(int(grid[i][j])*2)
                    grid[i+step][j] = c
                    global score
                    score += int(grid[i][j])
                    counter[j] += 1

        if x == 2:
            if oldGrid != tuple(tuple(x) for x in grid):
                randCoord = scanArray(grid, c)
                grid[randCoord[0]][randCoord[1]] = randCoord[2]
        updateArray(grid)

def updateArray(grid): # refreshing command prompt interface
    time.sleep(0.05)
    os.system('cls')
    prtGrid(grid)

def checkArray():
    for i in range(0,4):
        for j in range(0,3):
            if (grid[i][j] == grid[i][j+1]) or (grid[j][i] == grid[j+1][i]):
                return False
    return True

def checkGameOver():
    if (''.join(val for list in grid for val in list)).isalnum():
        if checkArray():
            print('Game Over!')
            time.sleep(1)
            print('Created by Shiny Ranjan')
            time.sleep(5)
            exit()

def main():
    init(grid)

    while True:
        takeInput()

main()
