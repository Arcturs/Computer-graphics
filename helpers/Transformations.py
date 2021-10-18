import math
import numpy as np


def scaling(scale):
    s = np.identity(4)
    s[0, 0] = scale[0]
    s[1, 1] = scale[1]
    s[2, 2] = scale[2]
    s[3, 3] = 1
    return s


def translation(move):
    t = np.identity(4)
    t[0, 3] = move[0]
    t[1, 3] = move[1]
    t[2, 3] = move[2]
    return t


def rotate(matrix):
    r = np.identity(4)
    theta = math.pi / 180
    n = math.sqrt(math.pow(matrix[0], 2) + math.pow(matrix[1], 2) + math.pow(matrix[2], 2))
    if n != 0:
        n1 = float(matrix[0] / n)
        n2 = float(matrix[1] / n)
        n3 = float(matrix[2] / n)
    else:
        return 1

    r[0, 0] = math.cos(theta) + (1 - math.cos(theta)) * math.pow(n1, 2)
    r[1, 1] = math.cos(theta) + (1 - math.cos(theta)) * math.pow(n2, 2)
    r[2, 2] = math.cos(theta) + (1 - math.cos(theta)) * math.pow(n3, 2)

    r[0, 1] = n1 * n2 * (1 - math.cos(theta)) - n3 * math.sin(theta)
    r[1, 0] = n1 * n2 * (1 - math.cos(theta)) + n3 * math.sin(theta)
    r[2, 0] = n1 * n3 * (1 - math.cos(theta)) - n2 * math.sin(theta)
    r[0, 2] = n1 * n3 * (1 - math.cos(theta)) + n2 * math.sin(theta)
    r[2, 1] = n2 * n3 * (1 - math.cos(theta)) + n1 * math.sin(theta)
    r[1, 2] = n2 * n3 * (1 - math.cos(theta)) - n1 * math.sin(theta)
    r[3, 3] = 1
    return r
