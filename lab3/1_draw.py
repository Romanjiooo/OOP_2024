from array import *
from random import randint
import numpy as np
import random


def create_labyrinth(m):
    a = [["#" if random.random() < 0.4 else "." for i in range(m)] for j in range(m)]
    matr = np.array(a)
    i = randint(1, m - 1)
    j = randint(1, m - 1)

    if a[i][j] != "#":
        a[i][j] == "*"
    return matr


m = randint(3, 6)
labyrinth = create_labyrinth(m)
print(labyrinth)