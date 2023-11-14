import random
import matplotlib.pyplot as plt
import numpy as np

sudoku = np.array(
    [[6, 1, 0, 0, 8, 0, 0, 0, 9], [2, 0, 7, 4, 6, 0, 0, 0, 0], [0, 0, 0, 0, 5, 0, 0, 0, 0], [4, 0, 0, 0, 0, 0, 7, 0, 0],
     [3, 0, 8, 6, 9, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 2, 8], [0, 0, 6, 0, 0, 3, 2, 0, 0],
     [0, 0, 5, 1, 0, 0, 3, 9, 6], [8, 0, 2, 0, 4, 0, 0, 5, 0]])


# Costfunction
def costfunction(array):
    size = 9
    # X SUMMATOR
    xlist = []
    j = 1
    for i in range(size):
        unique, counts = np.unique(sudoku[i], return_counts=True)
        checkx = (np.asarray((unique, counts)).T)
        # print(len(unique)) # количество уникальных чисел в строке
        # print(counts) # выводит количество каждого уникального символа в строке
        for j in range(len(checkx)):
            #print(str(checkx[j][1]))
            if checkx[j][1] > 1:
                xlist.append(checkx[j][1])

    #print("ОСЬ Х: " + str(xlist))

    # Y SUMMATOR
    ylist = []
    rsudoku = np.rot90(array)  # переворачиваем по осям
    # print(rsudoku)
    for i in range(size):
        unique, counts = np.unique(rsudoku[i], return_counts=True)
        checky = (np.asarray((unique, counts)).T)
        # print(len(unique)) # количество уникальных чисел в ряду
        # print(str(unique))
        # print(str(counts)) # выводит количество каждого уникального символа в ряду
        for j in range(len(checky)):
            if checky[j][1] > 1:
                ylist.append(checky[j][1])
    ylist = ylist[::-1]
    #print("ОСЬ Y: " + str(ylist))
    costf = sum(xlist) + sum(ylist)
    return costf


print(costfunction(sudoku))
print(str(sudoku) + '\n')
print(sudoku)


def randomize():
    array = np.copy(sudoku)
    for i in range(len(array)):
        for j in range(len(array)):
            if array[i][j] == 0:
                array[i, j] = random.randint(1, 9)
    return array


iterations = []
s = []
iteration = 1
while True:
    randsudoku = randomize()
    costf = costfunction(randsudoku)
    iterations.append(iteration)
    s.append(costf)
    if costf < 30 or len(s)>1000:
        #print(randsudoku)
        #print(costf)
        break
    else:
        #print(randsudoku)
        #print(costf)
        iteration += 1



# График
fig, ax = plt.subplots()
ax.set(xlabel='Iteration (№)', ylabel='Costf (Sum of x and y)',
       title='Sudoku')
ax.plot(iterations, s)
plt.grid(True)
plt.show()