import random
import matplotlib.pyplot as plt
import numpy as np
import math

sudoku = np.array(
    [[6, 1, 0, 0, 8, 0, 0, 0, 9], [2, 0, 7, 4, 6, 0, 0, 0, 0], [0, 0, 0, 0, 5, 0, 0, 0, 0], [4, 0, 0, 0, 0, 0, 7, 0, 0],
     [3, 0, 8, 6, 9, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 2, 8], [0, 0, 6, 0, 0, 3, 2, 0, 0],
     [0, 0, 5, 1, 0, 0, 3, 9, 6], [8, 0, 2, 0, 4, 0, 0, 5, 0]])
size = 9


def costfunction(array):
    cost = 0
    size = 9

    # Проверка строк и столбцов
    for i in range(size):
        row_unique_count = len(set(array[i]))  # уникальные значения в строке
        col_unique_count = len(set(array[:, i]))  # уникальные значения в столбце
        cost += (size - row_unique_count) + (size - col_unique_count)

    # Проверка подквадратов 3x3
    for i in range(0, size, 3):
        for j in range(0, size, 3):
            block = array[i:i+3, j:j+3]  # извлекаем подквадрат
            block_unique_count = len(set(block.flatten()))  # уникальные значения в подквадрате
            cost += (size - block_unique_count)

    return cost


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


def generate_neighbor(sudoku, initial_sudoku):

    while True:
        # выбираем случайный блок
        block_row = 3 * random.randint(0, 2)
        block_col = 3 * random.randint(0, 2)

        # в блоке выбираем две случайной ячейки
        cell1_row = block_row + random.randint(0, 2)
        cell1_col = block_col + random.randint(0, 2)
        cell2_row = block_row + random.randint(0, 2)
        cell2_col = block_col + random.randint(0, 2)

        # убедимся что мы не меняем "статичные" ячейки
        if ((cell1_row != cell2_row or cell1_col != cell2_col) and
                initial_sudoku[cell1_row][cell1_col] == 0 and
                initial_sudoku[cell2_row][cell2_col] == 0):
            # меняем ячейки
            sudoku[cell1_row][cell1_col], sudoku[cell2_row][cell2_col] = sudoku[cell2_row][cell2_col], \
                                                                         sudoku[cell1_row][cell1_col]
            break

    return sudoku

def generate_initial_solution(sudoku):
    blocks = np.sqrt(size).astype(int)
    initial_solution = np.copy(sudoku)
    for i in range(0, size, blocks):
        for j in range(0, size, blocks):
            #берём блок 3на3
            block = initial_solution[i:i + blocks, j:j + blocks]
            missing_values = set(range(1, size + 1)) - set(block.flatten())
            missing_values = list(missing_values)

            random.shuffle(missing_values)

            # заполняем 0 на случайные числа
            for k in range(blocks):
                for l in range(blocks):
                    if block[k, l] == 0:
                        block[k, l] = missing_values.pop()
    return initial_solution


iterations = []
s = []
iteration = 1
# while True:
#     randsudoku = generate_initial_solution(sudoku)
#     costf = costfunction(randsudoku)
#     iterations.append(iteration)
#     s.append(costf)
#     if costf < 1 or len(s)>1000000:
#         print(randsudoku)
#         #print(costf)
#         break
#     else:
#         #print(randsudoku)
#         #print(costf)
#         iteration += 1
#
#
#
# # График


def simulated_annealing(sudoku, initial_temp, cooling_rate, stopping_temp, max_stagnation_iterations, max_restarts):
    best_solution = None
    best_cost = float('inf')
    stagnation_counter = 0
    restarts = 0
    temperature = initial_temp
    current_solution = generate_initial_solution(sudoku)
    current_cost = costfunction(current_solution)
    costs = []  # Для отслеживания стоимости
    temperatures = []  # Для отслеживания температуры
    iterations_list = []  # Для отслеживания итераций

    while restarts < max_restarts:
        iterations = 0
        while temperature > stopping_temp:
            neighbor = generate_neighbor(np.copy(current_solution), sudoku)
            neighbor_cost = costfunction(neighbor)
            cost_diff = neighbor_cost - current_cost

            if cost_diff < 0:
                current_solution, current_cost = neighbor, neighbor_cost
                stagnation_counter = 0
            else:
                if random.uniform(0, 1) < math.exp(-cost_diff / temperature):
                    current_solution, current_cost = neighbor, neighbor_cost
                stagnation_counter += 1

            if current_cost < best_cost:
                best_solution, best_cost = current_solution, current_cost

            temperature *= (1 - cooling_rate)
            iterations += 1

            costs.append(current_cost)
            temperatures.append(temperature)
            iterations_list.append(iterations)

            if stagnation_counter >= max_stagnation_iterations:
                break

        if stagnation_counter >= max_stagnation_iterations or temperature <= stopping_temp:
            current_solution = generate_initial_solution(sudoku)
            current_cost = costfunction(current_solution)
            temperature = initial_temp
            stagnation_counter = 0
            restarts += 1

        if restarts >= max_restarts:
            break

    # Построение графика
    plt.figure(figsize=(10, 5))
    plt.plot(iterations_list, costs, label='Cost Function', color='blue')
    plt.xlabel('Iteration')
    plt.ylabel('Cost')
    plt.title('Simulated Annealing Progress')
    plt.legend()
    plt.grid(True)
    plt.show()

    return best_solution


max_stagnation_iterations = 50  # Количество итераций без улучшения до перезапуска
max_restarts = 5  # Максимальное количество перезапусков
initial_temp = 1.0
cooling_rate = 0.01
stopping_temp = 0.0001


# Запускаем алгоритм симулированного отжига с перезапусками
solution = simulated_annealing(sudoku, initial_temp, cooling_rate, stopping_temp, max_stagnation_iterations, max_restarts)
print(solution)
