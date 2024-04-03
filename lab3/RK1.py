from random import *

maze = [['+','+','+','.','+','+'],['+','+','+','.','.','+'],['+','+','+','.','+','+'],['+','.','.','.','.','+'],['.','.','.','.','.','+'],['+','+','+','.','+','.']]
def make_labyrinth(n, m):
    return maze


def starters(labyrinth, n, m):
    start_x, start_y =  2,4
    labyrinth[start_x][start_y] = 'O'
    return labyrinth, start_x, start_y

def search_for_path(labyrinth, start_x, start_y, n, m):
    next = [(start_x, start_y, 0)]
    visited = []
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    while next:
        x, y, distance = next.pop(0)
        if (x, y) in visited:
            continue
        visited.append((x, y))

        if x == 0 or x == n - 1 or y == 0 or y == m - 1:
            if (x, y) != (start_x, start_y):
                return True, distance, (x + 1, y + 1)

        for move_x, move_y in directions:
            next_x, next_y = x + move_x, y + move_y
            if 0 <= next_x < n and 0 <= next_y < m and labyrinth[next_x][next_y] == '.' and (next_x, next_y) not in visited:
                next.append((next_x, next_y, distance + 1))

    return False, None, None

n, m = 6,6
labyrinth = make_labyrinth(n, m)
labyrinth, start_x, start_y = starters(labyrinth, n, m)

res = search_for_path(labyrinth, start_x, start_y, n, m)
print("Размер лабиринта: ", n, "x", m)
print("Лабиринт:")
for i in range(n):
    for j in range(m):
        print(labyrinth[i][j], end=" ")
    print()
print("Начальная позиция:", (start_x + 1, start_y + 1))
print("Ответ:", res)