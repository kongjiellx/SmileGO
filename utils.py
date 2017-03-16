import numpy as np

def one_hot(num, depth):
    a = np.zeros((depth,))
    a[int(num)] = 1
    return a.astype(dtype='int8')
