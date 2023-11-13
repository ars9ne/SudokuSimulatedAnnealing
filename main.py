import random

import numpy as np

sudoku = np.array(
    [[6, 1, 0, 0, 8, 0, 0, 0, 9], [2, 0, 7, 4, 6, 0, 0, 0, 0], [0, 0, 0, 0, 5, 0, 0, 0, 0], [4, 0, 0, 0, 0, 0, 7, 0, 0],
     [3, 0, 8, 6, 9, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 2, 8], [0, 0, 6, 0, 0, 3, 2, 0, 0],
     [0, 0, 5, 1, 0, 0, 3, 9, 6], [8, 0, 2, 0, 4, 0, 0, 5, 0]])

#Costfunction
def costfunction(array):


    size = 9
    #X SUMMATOR
    xlist = []
    j = 1
    for i in range(size):
        unique, counts = np.unique(sudoku[i], return_counts=True)
        #print(np.asarray((unique, counts)).T)
        #print(len(unique)) # количество уникальных чисел в строке
        #print(counts) # выводит количество каждого уникального символа в строке
        for j in range(len(unique)):
            if counts[j] > 1:
                xlist.append(counts[j])

    print("ОСЬ Х: " + str(xlist))

    #Y SUMMATOR
    ylist = []
    rsudoku = np.rot90(sudoku) # переворачиваем по осям
    #print(rsudoku)
    for i in range(size):
        unique, counts = np.unique(rsudoku[i], return_counts=True)
        #print(np.asarray((unique, counts)).T)
        #print(len(unique)) # количество уникальных чисел в ряду
        #print(counts) # выводит количество каждого уникального символа в ряду
        for j in range(len(unique)):
            if counts[j] > 1:
                ylist.append(counts[j])
    ylist = ylist[::-1]
    print("ОСЬ Y: " + str(ylist))
    costf = sum(xlist) + sum(ylist)
    return costf


print(costfunction(sudoku))
print(sudoku)

for i in range(len(sudoku)):
    for j in range(len(sudoku)):
        if sudoku[i][j] == 0:
            sudoku[i,j] = random.randint(1, 9)
print(sudoku)
