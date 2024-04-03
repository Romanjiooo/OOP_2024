'''from array import *
import random
def create_maze(min=5,max=10):

    N = random.randint(min,max)
    M = random.randint(min,max)

    meze = []

'''
    '''for i in range(N):
        row = []
        for j in range(M):
            row.append('+')
        meze.append(row)
'''
'''
    maze = [array('u', ['+']*M) for i in range(N)]

    return maze

print(create_maze())

#def go_out_maze():
'''